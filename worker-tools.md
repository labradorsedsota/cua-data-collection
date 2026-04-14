# TOOLS.md — BugHunt Worker

你的工具和环境速查表。操作规范看 `worker-execution-guide.md`，这里只记环境信息。

---

## 团队通讯

### 你的 PM

- **Pichai**（lynx_bot）— 首席产品经理，你的直接指令来源
- 指令通过 1v1 工作群下达
- 异常上报也发到 1v1 工作群

### 关键人物（了解即可，不需要直接沟通）

| 角色 | 人 | 说明 |
|------|-----|------|
| 管理者 | 林菡 | Pichai 的上级，POC 审批人 |
| 数据需求方 | 智子（consultant_bot） | L2 抽检，验证结果 JSON 质量 |
| 终审 | 老傅（FTY） | CUA 模型负责人，最终数据使用方 |

### DMWork 状态信号发送

状态信号通过群聊消息发送。格式严格按执行手册。

---

## Git 操作

### 拉取任务

```bash
# 首次
gh repo clone labradorsedsota/bughunt
cd bughunt

# 后续
git pull origin main
```

### 提交结果

```bash
# 写好结果 JSON 后
git add results/worker-XX/
git commit -m "results: worker-XX 完成 {project}-{id1}/{id2}/..."
git push origin main
```

**频率：** 每 5 个 case 批量 push。异常 case 立刻 push。

**冲突处理：** 每个 Worker 只写自己的 `results/worker-XX/` 目录，正常不会冲突。万一冲突：
```bash
git pull --rebase origin main
# 解决冲突后
git add .
git rebase --continue
git push
```

---

## Node.js / 前端项目部署

### 常用命令

```bash
# 安装依赖
npm install                    # 默认
npm install --legacy-peer-deps # 依赖冲突时
npm install --force            # 强制安装

# 启动开发服务器
npm run dev                    # 最常见
npx vite                       # Vite 项目备选
npm start                      # 部分项目用这个

# 端口占用处理
lsof -i :5173                  # 查端口占用
kill -9 <PID>                  # 杀进程

# Node 版本（如果装了 nvm）
nvm install 18
nvm use 18
```

### 包管理器

| 管理器 | 安装 | 说明 |
|--------|------|------|
| npm | 自带 | 大多数项目 |
| pnpm | `npm i -g pnpm` | 部分现代项目 |
| yarn | `npm i -g yarn` | 少数项目 |

任务卡会标注用哪个。没标注默认 npm。

### 部署验证

```bash
# 等服务启动后验证
curl -s -o /dev/null -w "%{http_code}" http://localhost:PORT
# 返回 200 = 成功
```

---

## mano-cua CLI

### 基本用法

```bash
npx mano-cua \
  --url "http://localhost:PORT/test_page" \
  --task "测试任务描述" \
  --expected-result "预期结果描述" \
  2>&1 | tee logs/{task_id}.log
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `--url` | Chrome 打开的初始页面 |
| `--task` | 中文测试任务描述（来自任务卡 `test_description_zh`） |
| `--expected-result` | 预期结果（来自任务卡 `expected_result_zh`），可选 |

### 异常处理

- `--expected-result` 报错 → 去掉这个参数重跑，结果 JSON 标 `expected_result_used: false`
- timeout → 重试 1 次，仍失败 → 标 `failed`，failure.type = `timeout`
- mano-cua 自身报错 → 重试 1 次，仍失败 → 标 `failed`，failure.type = `mano_cua_error`

### Log 关键字段提取

```
Session created: sess-XXXXXXXX-XXXX...    ← sess_id
Status: COMPLETED / ERROR / STOPPED       ← 执行状态
Total steps: N                            ← 步骤数
Last reasoning: ...                       ← 评估内容（提取 result + result_summary）
```

---

## 结果 JSON Checklist

提交前必须逐项检查：

- [ ] `task_id` 与任务卡一致
- [ ] `sess_id` 格式正确（`sess-` 开头）
- [ ] `status` = `completed` 或 `failed`
- [ ] `repo` 字段有值
- [ ] `expected_result_used` = true/false
- [ ] `mano_cua.result` = `normal` / `abnormal` / `unclear`
- [ ] `mano_cua.result_summary` 有具体观测事实（不是"好像有 bug"）
- [ ] `mano_cua.last_reasoning` 保留原文
- [ ] log 文件已本地保存（`logs/{task_id}.log`）
- [ ] log 行数 > 20
- [ ] log 包含 `Session created: sess-`

---

## 环境要求

| 项目 | 要求 |
|------|------|
| OS | macOS (Apple Silicon) |
| Node.js | ≥ 18.x |
| npm | ≥ 9.x |
| Git | 已配置 gh auth |
| Chrome | 已安装 |
| mano-cua | `npx mano-cua --version` 能输出版本 |
| VPN | 已连接（访问 GitHub） |

装机步骤见 `worker-setup.md`。
