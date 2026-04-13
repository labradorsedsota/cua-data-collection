#!/bin/bash
# =============================================================================
# BugHunt Worker 一键装机脚本
# 用法: ./setup-worker.sh --id <编号>
# 示例: ./setup-worker.sh --id 03
# =============================================================================

set -e

# ── 参数解析 ──────────────────────────────────────────────────────────────────

WORKER_ID=""
BOT_TOKEN=""
while [[ $# -gt 0 ]]; do
  case $1 in
    --id) WORKER_ID="$2"; shift 2 ;;
    --token) BOT_TOKEN="$2"; shift 2 ;;
    *) echo "未知参数: $1"; echo "用法: ./setup-worker.sh --id <编号> --token <botToken>"; exit 1 ;;
  esac
done

if [ -z "$WORKER_ID" ]; then
  echo "❌ 请指定 Worker 编号"
  echo "用法: ./setup-worker.sh --id 03 --token bf_xxxxxxxxxxxxx"
  exit 1
fi

if [ -z "$BOT_TOKEN" ]; then
  echo "❌ 请指定 DMWork botToken"
  echo "用法: ./setup-worker.sh --id 03 --token bf_xxxxxxxxxxxxx"
  exit 1
fi

WORKER_NAME="worker-${WORKER_ID}"
echo "🚀 开始配置 ${WORKER_NAME}"
echo "=================================================="

# ── 1. Homebrew ───────────────────────────────────────────────────────────────

echo ""
echo "📦 [1/7] 安装 Homebrew..."
if command -v brew &>/dev/null; then
  echo "  ✅ Homebrew 已安装: $(brew --version | head -1)"
else
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  # Apple Silicon 路径
  echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
  eval "$(/opt/homebrew/bin/brew shellenv)"
  echo "  ✅ Homebrew 安装完成"
fi

# ── 2. 基础环境 ───────────────────────────────────────────────────────────────

echo ""
echo "📦 [2/7] 安装基础环境（Node.js, Python, Git, gh CLI）..."

brew install node python@3.13 python-tk@3.13 gh 2>/dev/null || true
npm install -g pnpm yarn 2>/dev/null || true

echo "  Node.js:  $(node --version)"
echo "  npm:      $(npm --version)"
echo "  pnpm:     $(pnpm --version)"
echo "  yarn:     $(yarn --version)"
echo "  Python:   $(python3 --version)"
echo "  Git:      $(git --version)"
echo "  gh:       $(gh --version | head -1)"

# ── 3. GitHub CLI 登录 ────────────────────────────────────────────────────────

echo ""
echo "📦 [3/7] GitHub CLI 认证..."
if gh auth status &>/dev/null; then
  echo "  ✅ 已登录 GitHub"
else
  echo "  ⚠️ 需要手动登录 GitHub，请执行: gh auth login"
  echo "  （装机完成后再手动执行即可）"
fi

# ── 4. mano-cua ───────────────────────────────────────────────────────────────

echo ""
echo "📦 [4/7] 安装 mano-cua..."
brew tap hanningwang/tap 2>/dev/null || true
brew install mano-cua 2>/dev/null || brew upgrade mano-cua 2>/dev/null || true

if command -v mano-cua &>/dev/null; then
  echo "  ✅ mano-cua 已安装: $(which mano-cua)"
else
  echo "  ❌ mano-cua 安装失败，请手动检查"
fi

# ── 5. OpenClaw ───────────────────────────────────────────────────────────────

echo ""
echo "📦 [5/7] 安装 OpenClaw..."
npm install -g openclaw 2>/dev/null || true

if command -v openclaw &>/dev/null; then
  echo "  ✅ OpenClaw 已安装: $(openclaw --version 2>/dev/null || echo 'unknown')"
else
  echo "  ❌ OpenClaw 安装失败，请手动检查"
fi

# 初始化 workspace
openclaw setup 2>/dev/null || true

# ── 6. DMWork 插件 ────────────────────────────────────────────────────────────

echo ""
echo "📦 [6/7] 安装 DMWork 插件..."

EXTENSIONS_DIR="$HOME/.openclaw/extensions/dmwork"
mkdir -p "$EXTENSIONS_DIR"

# 从 npm 下载并解包
cd /tmp
rm -rf openclaw-channel-dmwork-*.tgz dmwork-package
npm pack openclaw-channel-dmwork@0.5.19 2>/dev/null
mkdir -p dmwork-package
tar xzf openclaw-channel-dmwork-*.tgz -C dmwork-package

# 部署到 extensions 目录
cp -r dmwork-package/package/* "$EXTENSIONS_DIR/"
cd "$EXTENSIONS_DIR"
npm install --production 2>/dev/null

# 清理
rm -rf /tmp/openclaw-channel-dmwork-*.tgz /tmp/dmwork-package

echo "  ✅ DMWork 插件已安装到 $EXTENSIONS_DIR"

# ── 7. Worker 配置 ────────────────────────────────────────────────────────────

echo ""
echo "📦 [7/7] 写入 Worker 配置..."

# 设置机器名
sudo scutil --set ComputerName "$WORKER_NAME"
sudo scutil --set HostName "$WORKER_NAME"
sudo scutil --set LocalHostName "$WORKER_NAME"
echo "  机器名: $WORKER_NAME"

# OpenClaw 配置
cat > "$HOME/.openclaw/openclaw.json" << OCEOF
{
  "agent": {
    "workspace": "~/.openclaw/workspace"
  },
  "plugins": {
    "entries": {
      "openclaw-channel-dmwork": {
        "enabled": true,
        "config": {
          "accounts": {
            "default": {
              "apiUrl": "https://im.deepminer.com.cn/api",
              "botToken": "${BOT_TOKEN}"
            }
          }
        }
      }
    }
  }
}
OCEOF
echo "  openclaw.json: 已写入（botToken: ${BOT_TOKEN:0:10}...）"

# Worker SOUL.md
cat > "$HOME/.openclaw/workspace/SOUL.md" << 'SOULEOF'
# SOUL.md - BugHunt Worker

你是 BugHunt 项目的执行 Worker，负责部署 buggy 版本的开源项目并执行 mano-cua 测试。

## 核心职责

1. 接收任务包（含项目信息、buggy commit、部署命令、测试任务描述）
2. 部署 buggy 版本到本地
3. 执行 mano-cua 测试
4. 上报结果（项目名称 | 测试内容 | sess-id | 是否复现）

## 执行流程

收到任务后按以下步骤执行：

1. **部署**
   - `git clone <repo>` → `git checkout <buggy_commit>`
   - 执行任务包中的 deploy_command
   - 确认服务在 expected_url 可访问

2. **测试**
   - 调用 mano-cua，传入测试任务描述和 URL
   - 等待执行完成

3. **上报**
   - 收集 sess-id
   - 判断是否复现了 Bug
   - 按格式上报结果

## 异常处理

- **部署失败**：自行排查（检查 Node 版本、依赖冲突、端口占用等），尝试 2-3 种方案。连续失败 3 次 → 上报 PM，跳到下一个任务
- **mano-cua 超时**：TODO（待定义超时时间和处理策略）
- **mano-cua 崩溃**：重试 1 次，仍失败 → 记录为异常，跳到下一个任务

## 汇报规范

每完成一个 case 上报一次结果。格式：
```
项目名称 | 测试内容 | sess-id | 是否复现
```

每完成 10 个 case 发一次批量进度。
SOULEOF
echo "  SOUL.md: 已写入"

# Worker IDENTITY.md
cat > "$HOME/.openclaw/workspace/IDENTITY.md" << IDEOF
# IDENTITY.md

- **Name:** BugHunt Worker ${WORKER_ID}
- **Role:** CUA 数据采集执行 Worker
- **Type:** AI Agent
IDEOF
echo "  IDENTITY.md: 已写入"

# ── 验证 ──────────────────────────────────────────────────────────────────────

echo ""
echo "=================================================="
echo "🔍 装机验证"
echo "=================================================="

PASS=0
FAIL=0

check() {
  if eval "$2" &>/dev/null; then
    echo "  ✅ $1"
    PASS=$((PASS + 1))
  else
    echo "  ❌ $1"
    FAIL=$((FAIL + 1))
  fi
}

check "Node.js"     "node --version"
check "npm"         "npm --version"
check "pnpm"        "pnpm --version"
check "yarn"        "yarn --version"
check "Python 3.13" "python3 --version"
check "Git"         "git --version"
check "gh CLI"      "gh --version"
check "mano-cua"    "which mano-cua"
check "OpenClaw"    "which openclaw"
check "DMWork 插件"  "test -f $HOME/.openclaw/extensions/dmwork/dist/index.js || test -f $HOME/.openclaw/extensions/dmwork/index.ts"
check "SOUL.md"     "test -f $HOME/.openclaw/workspace/SOUL.md"
check "GitHub 连通"  "curl -s -o /dev/null -w '%{http_code}' https://github.com | grep -q 200"

echo ""
echo "=================================================="
echo "  通过: ${PASS} | 失败: ${FAIL}"
if [ "$FAIL" -eq 0 ]; then
  echo "  🎉 ${WORKER_NAME} 装机完成！"
else
  echo "  ⚠️ 有 ${FAIL} 项未通过，请手动检查"
fi
echo "=================================================="

echo ""
echo "📋 后续手动步骤："
echo "  1. gh auth login（如未登录）"
echo "  2. 系统设置 → 隐私与安全性 → 辅助功能 → 允许 Terminal"
echo "  3. 系统设置 → 隐私与安全性 → 屏幕录制 → 允许 Terminal"
echo "  4. 补充 ~/.openclaw/openclaw.json 中的模型 provider 配置"
echo "  5. openclaw gateway start"
