# BugHunt Worker 执行手册（POC 版）

> 本文档是 Worker（Moss / Fabrice）的唯一执行参考。拿到任务卡后按此文档逐步操作。

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

### 第 1 步：Clone 并部署

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

### 第 5 步：首步 URL 校验

mano-cua 启动后，检查第一步 screenshot 中的 URL 是否指向 dev server。
- 偏离 → 终止（`mano-cua stop`）并重启
- 连续 3 次偏离 → 标 BLOCKED

### 第 6 步：超时监控

- **软超时 10 分钟**：标 WARN，继续等待
- **硬超时 15 分钟**：强制终止（`mano-cua stop`），标 BLOCKED

### 第 7 步：提取结果

执行完成后：
1. 从输出中提取 **sess-id**
2. 确认日志完整性：文件存在、行数 > 20、包含 Session ID
3. 判定是否复现 Bug（**必须引用具体观测事实**）

### 第 8 步：关闭测试标签页

```bash
osascript -e '
tell application "Google Chrome"
    set matchPath to "localhost:3000"
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
  "worker": "worker-fabrice",
  "status": "completed",
  "sess_id": "sess-20260414xxxxx-xxxxxxxxx",
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
  "worker": "worker-moss",
  "status": "failed",
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

**push 频率：**
- 正常：每完成 5 个 case 批量 git push 一次
- 异常/failed：立刻 push + 群里通知 PM

---

## 四、异常处理速查

| 场景 | 处理 |
|------|------|
| 部署失败 | 自行排查一次（端口、依赖、版本），仍失败 → 上报 PM |
| 同项目连续 3 个 case 部署失败 | 标 PROJECT_BLOCKED，整批跳过 |
| mano-cua 软超时（>10min） | 标 WARN，继续等 |
| mano-cua 硬超时（>15min） | `mano-cua stop`，标 BLOCKED + 诊断 |
| mano-cua 崩溃 | 重试 1 次，仍失败 → 记录异常跳过 |
| 首步 URL 偏离 | 终止重启，连续 3 次 → BLOCKED + 诊断 |
| `--expected-result` 报错 | 去掉该参数重跑 |

**BLOCKED 必须附诊断：** 失败现象 + 根因判断 + 至少 2 种解决方案 + 建议方案。

---

## 五、Checklist（每个 case 打勾）

```
启动前：
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

*文档版本：v1.0 | 2026-04-14 | Pichai*
