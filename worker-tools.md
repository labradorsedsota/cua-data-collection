# TOOLS.md — BugHunt Worker

环境特定信息。操作规范看 `worker-execution-guide.md`。

---

## 身份

- **BOT_TOKEN**: `（启动时从 OpenClaw DMWork 插件配置获取）`
- **WORK_CHANNEL_ID**: `（PM 在指令中提供）`

## 团队

| 角色 | 名字 | UID | 说明 |
|------|------|-----|------|
| PM（你的指令来源） | Pichai | `lynx_bot` | 1v1 群下达指令、接收状态上报 |
| 管理者 | 林菡 | `10cd18f3c2554efaa424c397495d0a8e` | Pichai 上级 |
| 筛选 & 任务设计 | 智子 | `consultant_bot` | L2 抽检 |
| 终审 | 老傅 | `8a25d997d7b24468ac31dfc75f71ecb1` | CUA 模型负责人 |

## Repo

- **地址**: `https://github.com/labradorsedsota/bughunt`
- **任务卡**: `tasks/pool/*.json`
- **结果提交**: `results/worker-XX/` （XX = 你的 worker 名）
- **push 频率**: 每 5 个 case 批量 push，异常立刻 push

## DMWork 实时消息

OpenClaw 只在 turn 结束时发消息。用 curl 做阶段性汇报：

```bash
curl -s -X POST "https://im.deepminer.com.cn/api/v1/bot/sendMessage" \
  -H "Authorization: Bearer ${BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"channel_id":"${WORK_CHANNEL_ID}","channel_type":2,"payload":{"type":1,"content":"消息内容"}}'
```

消息格式和发送时机见 `worker-execution-guide.md` 第 6 步。

## 环境

| 项目 | 要求 |
|------|------|
| OS | macOS (Apple Silicon) |
| Node.js | ≥ 18.x |
| Chrome | 已安装 |
| mano-cua | 可用 |
| Git | gh auth 已配置 |
| VPN | 已连接 |

装机步骤见 `worker-setup.md`。
