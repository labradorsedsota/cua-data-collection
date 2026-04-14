# Worker 装机清单

本文档定义每台 Mac mini Worker 的完整配置要求。周三(4/16)到货后按此清单执行。

---

## 〇、前置准备

### 0.1 安装 VPN

按团队统一配置安装 VPN，确保能访问 GitHub、npm registry 等外部资源。后续所有步骤均需 VPN 已连接。

### 0.2 安装 Google Chrome

从官网下载安装：https://www.google.com/chrome/

或通过 Homebrew 安装（需先完成 2.1）：
```bash
brew install --cask google-chrome
```

mano-cua 依赖 Chrome 进行 GUI 自动化操作，必须安装。

---

## 一、系统要求

- macOS Sequoia 15.x（新机器默认）
- 已联网（需要访问 GitHub、npm registry、DMWork API）
- 已登录 Apple ID（如需要）
- VPN 已安装并连接
- Google Chrome 已安装

## 二、基础环境

### 2.1 Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装后确认：
```bash
brew --version
```

### 2.2 Node.js

```bash
brew install node
```

验证：
```bash
node --version   # >= 20.x
npm --version
```

### 2.3 包管理器

```bash
npm install -g pnpm yarn
```

验证：
```bash
pnpm --version
yarn --version
```

### 2.4 Python（mano-cua 依赖）

```bash
brew install python@3.13 python-tk@3.13
```

验证：
```bash
python3 --version  # >= 3.13
```

### 2.5 Git & GitHub CLI

```bash
brew install gh
gh auth login
```

验证：
```bash
git --version
gh auth status
```

## 三、mano-cua

```bash
brew tap hanningwang/tap
brew install mano-cua
```

验证：
```bash
which mano-cua
# 应输出 /opt/homebrew/bin/mano-cua
```

**当前最新版本：1.0.6**

### mano-cua 调用 SOP

> 完整执行规范见 README.md「mano-cua 测试执行规范（SOP）」，以下为 Worker 快速参考。

Worker 拿到任务卡后的标准执行流程：

```bash
# 1. Clone 并部署 buggy 版本
gh repo clone ${repo}
cd ${repo_dir}
git checkout ${buggy_commit}
${deploy_commands}  # 如 npm install && npm run dev

# === Pre-flight ===

# 2. 部署验证（确认服务跑起来再开测）
curl -s -o /dev/null -w '%{http_code}' ${dev_url}  # 期望返回 200
# 如果 120 秒内不返回 200 → 排查或上报

# 3. 打开 Chrome 到目标页面
open -a "Google Chrome" "${dev_url}${test_page}"
sleep 2

# 4. 窗口最大化
osascript -e '
tell application "Finder"
    set _b to bounds of window of desktop
    tell application "Google Chrome"
        set bounds of front window to {0, 0, item 3 of _b, item 4 of _b}
    end tell
end tell'

# === In-flight ===

# 5. 拼接任务描述并执行（日志本地落盘）
mano-cua run "当前Chrome浏览器已打开{app_name}网站，地址是{dev_url}。{test_description_zh}" \
  --expected-result "{expected_result_zh}" \
  2>&1 | tee logs/${task_id}.log
# 注意：--expected-result 为可选增强，报错时去掉重跑

# 首步 URL 校验：确认第一步 screenshot 指向 dev server
# 双层超时：软 10min（标 WARN）/ 硬 15min（强制终止）

# === Post-flight ===

# 6. 从输出中提取 sess-id
# 7. 日志完整性确认（行数 > 20、包含 Session ID）
# 8. 判定是否复现（必须引用具体观测事实）
# 9. 关闭测试标签页
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

**注意事项：**
- `mano-cua run` 只接一个参数：拼接后的任务描述字符串
- 不需要传 URL 参数，任务描述里已包含上下文
- 轨迹数据自动记录在 mano 服务端，通过 sess-id 查看
- `mano-cua stop` 可强制停止异常 session
- `test_page` 只用于 Chrome 打开初始页面，不拼进任务描述
- 同项目的多个 bug 共享部署，不需要重复 clone/install
- 日志路径命名规范：`logs/{task_id}.log`

### macOS 权限

mano-cua 需要控制桌面 GUI，首次运行时需授权：
- 系统设置 → 隐私与安全性 → 辅助功能 → 允许 Terminal / mano-cua
- 系统设置 → 隐私与安全性 → 屏幕录制 → 允许 Terminal / mano-cua

## 四、OpenClaw

```bash
npm install -g openclaw
openclaw setup
```

验证：
```bash
openclaw --version  # 2026.3.28
openclaw status
```

### 4.1 Gateway 配置

编辑 `~/.openclaw/openclaw.json`：

```json5
{
  // TODO: 补充具体配置
  // - 模型 provider 和 API key
  // - DMWork 插件配置（botToken、apiUrl）
  // - Agent 配置
}
```

> ⚠️ 待周二跑通流程后，从验证机器导出完整配置模板。

### 4.2 DMWork 插件

```bash
# TODO: 确认安装方式
# 方案1: npm 安装
npm install -g openclaw-channel-dmwork

# 方案2: 手动部署到 extensions 目录
# 将插件文件复制到 ~/.openclaw/extensions/dmwork/
```

验证：
```bash
openclaw plugins list | grep dmwork
# 应显示 loaded, 版本 0.5.19
```

### 4.3 Worker Agent 配置

每台机器的 workspace（`~/.openclaw/workspace/`）需要配置：

**SOUL.md** — Worker 身份和行为规则：
```markdown
# TODO: 周二验证后定稿
# 内容包括：
# - 你是 BugHunt Worker，负责部署 buggy 版本并执行 mano-cua 测试
# - 任务包格式说明
# - 部署失败时的排查策略
# - 超时处理规则
# - 结果上报格式和方式
```

**AGENTS.md** — 执行规范：
```markdown
# TODO: 周二验证后定稿
# 内容包括：
# - 收到任务后的标准执行流程
# - 异常处理规则
# - 汇报规范
```

## 五、环境验证脚本

装机完成后，运行以下命令逐项验证：

```bash
echo "=== 基础环境 ==="
node --version
npm --version
pnpm --version
yarn --version
python3 --version
git --version
gh auth status

echo "=== mano-cua ==="
which mano-cua
mano-cua --help 2>&1 | head -3

echo "=== OpenClaw ==="
openclaw --version
openclaw gateway status
openclaw plugins list | grep dmwork

echo "=== 网络连通性 ==="
curl -s -o /dev/null -w "%{http_code}" https://github.com
curl -s -o /dev/null -w "%{http_code}" https://im.deepminer.com.cn/api/v1/bot/groups
```

全部通过 = 装机完成 ✅

## 六、待补充（周二验证后）

- [ ] 每台 Worker 的 Bot ID（类似 `lynx_bot` 的标识，待告知提供方式）
- [ ] 每台 Worker 的 Bot Token（独立的 DMWork botToken）
- [ ] `openclaw.json` 完整配置模板（模型 provider + API key 部分）
- [ ] DMWork apiUrl 确认
- [ ] DMWork 插件安装步骤（确认最佳方式）
- [ ] SOUL.md / AGENTS.md 定稿内容
- [ ] mano-cua 运行参数（超时时间等）
- [ ] 辅助功能/屏幕录制权限的精确授权步骤
- [ ] Worker 编号命名规范（worker-01 ~ worker-10）

---

*文档版本：v1.0 | 2026-04-13 | Pichai*
*周二验证后更新为 v2.0*
