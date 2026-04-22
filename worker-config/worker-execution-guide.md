# BugHunt Worker 执行手册（POC 版）

> 本文档是 Worker（Moss / Fabrice）的唯一执行参考。拿到任务卡后按此文档逐步操作。

---

## 零、装机前置

> 首次部署 Worker 时，按 [worker-setup.md](worker-setup.md) 完成软件安装（VPN、Homebrew、Chrome、Node.js、Git、mano-cua）。

---

## 一、任务卡格式

每个任务卡是一个 JSON 文件，关键字段：

| 字段 | 说明 |
|------|------|
| `task_id` | 任务唯一标识（如 `luxesite-253`） |
| `repo` | GitHub 仓库（如 `ivegamsft/luxesite`） |
| `buggy_commit` | 需要 checkout 的 commit hash |
| `deploy_commands` | 部署命令列表（如 `["npm install", "npm run dev"]`） |
| `deploy_verify` | 部署验证方式（curl 检查返回 200） |
| `app_name` | 应用名称 |
| `dev_url` | 开发服务器地址（如 `http://localhost:3000`） |
| `test_page` | Chrome 打开的初始页面路由 |
| `test_description_zh` | 中文测试任务描述 |
| `expected_result_zh` | 预期结果描述（可选） |
| `timeout` | 超时设置 |

---

## 二、执行流程（逐步操作）

### ⚠️ 执行节奏：每个 case 一个 turn

**每完成一个 case 的 mano-cua 后，必须先 @Pichai 发状态信号，再开始下一个 case。**

不要在一个 turn 里连续执行多个 case。正确节奏：

```
Turn 1: 部署 case 1 → mano-cua → 写结果 JSON → @Pichai 发状态信号
Turn 2: 部署 case 2 → mano-cua → 写结果 JSON → @Pichai 发状态信号
...
```

错误做法：一口气跑完所有 case 最后才汇报。这会导致 PM 长时间收不到进度，触发巡检告警。

---

### 第 1 步：清理端口 + Clone 并部署

**启动新项目前，必须先清理目标端口上的残留进程。** 93 个项目共用 :3000，41 个项目共用 :5173——不清理会导致新项目启动失败（端口占用）。

```bash
# 从任务卡 dev_url 提取端口号（如 http://localhost:3000 → 3000）
PORT=$(echo "${dev_url}" | grep -oE ':[0-9]+' | tr -d ':')

# 清理该端口上的残留进程
lsof -ti:${PORT} | xargs kill -9 2>/dev/null
sleep 1

# 确认端口已释放
lsof -i:${PORT} && echo "⚠️ 端口 ${PORT} 仍被占用，请手动排查" || echo "✅ 端口 ${PORT} 已释放"
```

**同项目不同 bug 切换时**（只换 commit，不换项目）：也需要先 kill 服务再 checkout 新 commit 重新启动。

```bash
# 首次执行该项目时 clone（同项目多个 bug 共享部署，不需重复 clone）
gh repo clone ${repo}
cd ${repo_dir}
git checkout ${buggy_commit}

# 按任务卡执行部署命令
npm install    # 或 pnpm install / yarn，看任务卡标注
npm run dev    # 或任务卡指定的启动命令
```

### 第 2 步：部署验证

```bash
# 确认服务跑起来（120 秒内返回 200）
curl -s -o /dev/null -w '%{http_code}' ${dev_url}
```

- 返回 200 → 继续
- 120 秒内不返回 200 → 自行排查（端口占用、依赖缺失等），排查失败 → 上报 PM

### 第 3 步：打开 Chrome + 窗口最大化

```bash
# 打开目标页面
open -a "Google Chrome" "${dev_url}${test_page}"
sleep 2

# 窗口最大化（确保 mano-cua 截图完整）
osascript -e '
tell application "Finder"
    set _b to bounds of window of desktop
    tell application "Google Chrome"
        set bounds of front window to {0, 0, item 3 of _b, item 4 of _b}
    end tell
end tell'
```

### 第 4 步：执行 mano-cua

```bash
# 拼接任务描述并执行，日志本地落盘
mano-cua run "当前Chrome浏览器已打开${app_name}网站，地址是${dev_url}。${test_description_zh}" \
  --expected-result "${expected_result_zh}" \
  2>&1 | tee logs/${task_id}.log
```

**注意：**
- `--expected-result` 如果导致 mano-cua 报错 → 去掉该参数重跑，不阻塞
- `test_page` 只用于打开 Chrome，不拼进任务描述
- 确保 `logs/` 目录存在：`mkdir -p logs`

**浏览器边界约束（必须遵守）：**

Worker 调用 mano-cua 时，在任务描述末尾统一附加以下约束文本：

> "请始终在浏览器内操作，禁止打开 Terminal、Finder 或其他应用程序。如果在浏览器中找不到目标功能，直接标记 result 为 unclear，result_summary 写明'未在页面中找到目标功能入口'。"

即实际拼接的完整描述为：
```
"当前Chrome浏览器已打开${app_name}网站，地址是${dev_url}。${test_description_zh} 请始终在浏览器内操作，禁止打开 Terminal、Finder 或其他应用程序。如果在浏览器中找不到目标功能，直接标记 result 为 unclear，result_summary 写明'未在页面中找到目标功能入口'。"
```

**背景：** POC 中 3 张卡因 mano-cua 逃逸到 Terminal 分析源码（打开 Terminal 执行 ls/find/cat），消耗 50-86 步但产出无效 GUI 轨迹数据。此约束与任务卡 `test_description_zh` 中的引导语形成双保险。

### 第 5 步：首步 URL 校验

mano-cua 启动后，检查第一步 screenshot 中的 URL 是否指向 dev server。
- 偏离 → 终止（`mano-cua stop`）并重启
- 连续 3 次偏离 → 标 BLOCKED

### 第 6 步：超时 & 步数监控

- **步数上限 80 步**：监控 log 输出的 `[step N]`，当 N ≥ 80 时立即执行 `mano-cua stop`
- **软超时 10 分钟**：标 WARN，继续等待
- **硬超时 15 分钟**：强制终止（`mano-cua stop`），标 BLOCKED

> 步数和超时哪个先到哪个生效，双重保护。超过 80 步视为 timeout 类型失败。

### 第 7 步：提取结果

执行完成后：
1. 从输出中提取 **sess-id**
2. 确认日志完整性：文件存在、行数 > 20、包含 Session ID
3. 判定是否复现 Bug（**必须引用具体观测事实**）

### 第 8 步：关闭测试标签页

```bash
osascript -e '
tell application "Google Chrome"
    set matchPath to "localhost"
    set closedCount to 0
    repeat with w in windows
        set tabList to tabs of w
        repeat with i from (count of tabList) to 1 by -1
            if URL of item i of tabList contains matchPath then
                delete item i of tabList
                set closedCount to closedCount + 1
            end if
        end repeat
    end repeat
    return closedCount
end tell'
```

确认 closedCount > 0。然后进入下一个任务。

---

## 三、结果上报（双通道）

每完成一个 case，**同时做两件事**：

### 通道 1：群聊状态信号（实时，PM 监控用）

在群里发一条一行状态信号：

```
✅ worker-fabrice | luxesite-253 | 4m32s
```
```
❌ worker-fabrice | luxesite-258 | 6m15s
```
```
⚠️ BLOCKED worker-fabrice | cleaningsvc-18 | 部署失败
```

### 通道 2：结果 JSON 写入 repo（持久化，统计和交付用）

将完整结果写入 `results/{worker名}/` 目录，文件名 = `{task_id}.json`。

status 只有两个值：`completed`（mano-cua 跑完）或 `failed`（没跑完）。

**正常 case（completed）：**
```json
{
  "task_id": "luxesite-253",
  "repo": "ivegamsft/luxesite",
  "worker": "worker-fabrice",
  "status": "completed",
  "sess_id": "sess-20260414xxxxx-xxxxxxxxx",
  "expected_result_used": true,
  "duration_seconds": 272,
  "timestamp": "2026-04-14T15:23:45+08:00",
  "mano_cua": {
    "status": "COMPLETED",
    "total_steps": 12,
    "last_action": "DONE",
    "result": "abnormal",
    "result_summary": "404 页面仅显示错误信息，无返回首页链接",
    "last_reasoning": "（原样复制 log 末尾 Last reasoning 的完整文本）"
  }
}
```

**mano_cua 字段说明：**
- `status` / `total_steps` / `last_action` / `last_reasoning`：从 log 末尾汇总区直接提取
- `result`：Worker 读 last_reasoning 后判断功能表现
  - `normal` — reasoning 说功能正常、符合预期
  - `abnormal` — reasoning 报告了异常、缺失、报错等
  - `unclear` — 无法判断（reasoning 模糊或没走到关键步骤）
- `result_summary`：一句话概括 reasoning 里的关键发现

**异常 case（failed）：**
```json
{
  "task_id": "cleaningsvc-18",
  "repo": "owner/cleaningsvc",
  "worker": "worker-moss",
  "status": "failed",
  "expected_result_used": false,
  "sess_id": null,
  "duration_seconds": 0,
  "timestamp": "2026-04-14T15:30:00+08:00",
  "mano_cua": null,
  "failure": {
    "type": "deploy_failed",
    "symptom": "npm install 报 node-gyp 编译错误",
    "attempted": [
      "清缓存重装（同一错误）",
      "--ignore-scripts（服务启动缺 sass 模块）"
    ],
    "recommendation": "跳过，需 nvm 降级 Node 14"
  }
}
```

failure.type 取值：`deploy_failed` | `timeout` | `mano_cua_error` | `url_deviation` | `other`

**熔断跳过 case（fuse_deploy_failed）：**

同 buggy_commit 连续 2 张 deploy_failed 后，剩余卡不再实际部署，直接写如下 result：
```json
{
  "task_id": "luxesite-260",
  "repo": "ivegamsft/luxesite",
  "worker": "worker-fabrice",
  "status": "failed",
  "expected_result_used": false,
  "sess_id": null,
  "duration_seconds": 0,
  "timestamp": "2026-04-23T10:05:00+08:00",
  "mano_cua": null,
  "failure": {
    "type": "deploy_failed",
    "symptom": "fuse_deploy_failed",
    "attempted": ["fuse_trigger: luxesite-253, luxesite-258"],
    "recommendation": "同 buggy_commit 前 2 张已确认 deploy_failed"
  }
}
```

- `symptom: fuse_deploy_failed` 区分真实失败和熔断跳过
- `attempted` 记录触发熔断的 2 张卡的 task_id，用于追溯

**push 频率：**
- 正常：每完成 5 个 case 批量 git push 一次
- 异常/failed：立刻 push + 群里通知 PM

**新增字段说明：**
- `repo`：从任务卡 `repo` 字段原样复制（`owner/name` 格式）
- `expected_result_used`：本次执行是否使用了 `--expected-result` 参数（true/false）。如果因报错去掉了该参数重跑，填 false

**【POC 后评估】log 文件上传：**
目前 log 仅本地落盘（`logs/{task_id}.log`）。POC 结束后评估是否需要 push 到 repo `logs/{worker名}/{task_id}.log`，供 L2 抽检查看中间步骤 reasoning。

---

## 四、异常处理速查

| 场景 | 处理 |
|------|------|
| 端口被占用 | `lsof -ti:${PORT} \| xargs kill -9`，确认释放后重新启动 |
| 部署失败 | 自行排查一次（端口、依赖、版本），仍失败 → 上报 PM |
| **需要数据库/认证/OAuth** | **正常尝试部署。** 如果部署因缺少后端依赖而失败，标 deploy_failed，symptom 写明原因（如"需要 OAuth 登录"/"需要 PostgreSQL"）。不要花时间自行搭建后端环境（不创建用户、不配数据库、不模拟登录），尝试部署失败即可上报 |
| Node 版本不兼容 | 用 nvm 切版本：先查 `package.json` 的 `engines` 字段；没有则根据框架年代判断（老 Angular → Node 14，一般项目 → Node 18/20）。最多试 2 个版本，还不行就标 deploy_failed |
| **同 buggy_commit 连续 2 张 deploy_failed** | **熔断：该 commit 剩余卡全部跳过，不再尝试部署。** 跳过的卡写 result JSON（status: failed, failure.type: deploy_failed, symptom: fuse_deploy_failed，详见§三熔断格式）。同 repo 不同 buggy_commit 的卡不受影响，继续正常执行 |
| mano-cua 软超时（>10min） | 标 WARN，继续等 |
| mano-cua 硬超时（>15min） | `mano-cua stop`，标 BLOCKED + 诊断 |
| mano-cua 崩溃 | 重试 1 次，仍失败 → 记录异常跳过 |
| 首步 URL 偏离 | 终止重启，连续 3 次 → BLOCKED + 诊断 |
| `--expected-result` 报错 | 去掉该参数重跑 |
| 任务描述要求打开 DevTools / 执行 JS | mano-cua 无法操作浏览器控制台，自然报 unclear → 正常跳过，不算异常 |

**BLOCKED 必须附诊断：** 失败现象 + 根因判断 + 至少 2 种解决方案 + 建议方案。

**控制台 JS 类任务卡说明：** 少量任务卡（约 5 张，占比 ~2%）的测试步骤包含"在浏览器控制台执行 JS 代码"（如调用 `editor.render()`、`player.configure()` 等）。mano-cua 只能操作 GUI，无法打开 DevTools 执行 JS。这类卡排产时放在最后，Worker 正常执行即可——mano-cua 走不到控制台操作步骤时会自然报 `unclear`，不产生垃圾轨迹，不需要特殊处理。

---

## 五、Checklist（每个 case 打勾）

```
启动前：
[ ] 目标端口已清理（无残留进程）
[ ] 部署验证通过（curl 返回 200）
[ ] Chrome 打开目标页面 + 窗口最大化
[ ] logs/ 目录存在

执行中：
[ ] 首步 URL 正确
[ ] 未超软超时 10min / 硬超时 15min

完成后：
[ ] 日志已落盘，行数 > 20，包含 Session ID
[ ] sess-id 已提取
[ ] 复现判定已引用具体观测事实
[ ] 测试标签页已关闭（closedCount > 0）
[ ] 结果已在群里上报
```

---

*文档版本：v2.1 | 2026-04-22 | Pichai*
*v2.1 变更：熔断规则从「同项目连续 3 case → PROJECT_BLOCKED」改为「同 buggy_commit 连续 2 张 deploy_failed → 该 commit 剩余卡跳过」；新增熔断 result JSON 格式（fuse_deploy_failed）；DB/OAuth 处理改为正常尝试部署后按实际结果判定*
*v2.0 变更：新增 turn 拆分规则（每个 case 完成后必须先发状态再继续下一个）+ Node 版本兼容处理规则*
*v1.9 变更：新增端口清理步骤（第 1 步前置）+ 异常处理表新增端口占用 + Checklist 新增端口检查项*
*v1.8 变更：新增控制台 JS 类任务卡处理说明（约 5 张，排产末尾，mano-cua 自然兜底）*
*v1.7 变更：装机章节拆分为独立文件 worker-setup.md，执行手册改为引用*
