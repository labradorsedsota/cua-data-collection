# Mycroft 派发操作手册

> 本文档是 Mycroft 执行任务派发的唯一参考。Mycroft 只负责发送消息，不做选卡、排产、状态判断等业务决策。

---

## 一、你的职责

**读 dispatch-log.json → 找待发送的卡 → 发消息给 Worker**

你不需要：
- 决定哪个 Worker 跑哪些卡（Pichai 决定）
- 判断 Worker 状态或异常（Pichai 处理）
- 理解任务卡内容（你只是搬运）
- **修改 dispatch-log.json**（所有状态变更由 Pichai 操作）

---

## 二、触发条件

当 Pichai 告诉你"dispatch-log 有新任务待发送"，或你发现 dispatch-log.json 中有 `status: assigned` 的卡时，执行发送。

---

## 三、操作步骤

### 步骤 1：拉取最新 repo

```bash
cd /tmp && rm -rf bughunt-dispatch
git clone --depth 1 https://github.com/labradorsedsota/bughunt.git bughunt-dispatch
cd bughunt-dispatch
```

### 步骤 2：读取待发送任务

读 `pm-template/dispatch-log.json`，找出所有 `status: "assigned"` 的卡。

按 `worker` 分组，每个 Worker 的卡作为一批。

### 步骤 3：向每个 Worker 发送 2 条消息

**严格按顺序，每条间隔 200-300ms。**

#### 消息 1：派发指令（不需要 mention）

```
📋 第 {batch} 批任务（共 {N} 张）

任务列表：
1. {task_id_1}
2. {task_id_2}
...

执行手册：worker-config/worker-execution-guide.md（repo 里 pull 最新版）
任务卡位置：tasks/pool-clean/ 下对应 JSON 文件（不含 ground_truth）
结果输出：results/{worker-XX}/

同项目多张卡共享 clone + install，只需切换 buggy_commit。
```

#### 消息 2：汇报规则（必须 @Worker，payload 带 mention 字段）

```
@{worker名} ⚠️ 汇报规则（必须遵守）：

1. 收到任务 → @Pichai 回复"收到，开始执行第 {batch} 批"
2. 每完成 1 个 case → @Pichai 发状态（✅/❌/⚠️ task_id | 耗时 | 判定 | 摘要）
3. 遇异常超 10 分钟解决不了 → @Pichai 报异常
4. 全批完成 → @Pichai 报"第 {batch} 批完成，X✅ Y❌ Z⚠️，结果已 push，请派下一批"
5. ⚠️ 每个 case 完成 mano-cua 后，先发状态信号再开始下一个 case
6. 所有汇报消息必须 @Pichai（带 mention 字段），否则 PM 收不到

⚠️ 执行节奏要求（必须遵守）：
- 每个 case 必须在独立的 turn 中完成
- 正确节奏：部署 case 1 → mano-cua → 写结果 → @Pichai 发状态信号 → 结束当前 turn → 下一个 turn 开始 case 2
- 禁止在一个 turn 里连续执行多个 case
- 这是为了确保每个 case 之间都有消息发送的"呼吸点"，避免长时间无汇报

现在请先 @Pichai 回复 ACK。
```

payload **必须** 带 mention 字段：
```json
{"mention": {"uids": ["{worker_uid}"]}}
```

**不需要逐张发任务卡 JSON。** Worker 自行从 repo 的 `tasks/pool-clean/` 读取。

### 步骤 4：清理

```bash
rm -rf /tmp/bughunt-dispatch
```

---

## 四、Worker 通道表

| Worker | Channel ID | UID |
|--------|-----------|-----|
| worker-01 | c7b092f81af944a286e1dd631038c4aa | worker01_bot |
| worker-02 | c6288de9437d4dbaa5d6a66573578b95 | worker02_bot |
| worker-03 | f72274d28dc740efb7805f70fd5bb3b3 | worker03_bot |
| worker-04 | 6d7d933c594044a688484ca815c06433 | worker04_bot |
| worker-05 | d94fe49dfeec4d52b491eb6b0479256b | worker05_bot |
| worker-06 | fcb1cd72ae25476ab713568df49fe2db | worker06_bot |
| worker-07 | 13aea54f953c4a53bac98d995a33c111 | worker07_bot |
| worker-08 | 1147ef05c926437ab28936d92fcc0590 | worker08_bot |
| worker-09 | 5c49656f14114b6285b0c32e6e6bff4e | worker09_bot |
| worker-fabrice | 44998d9add6d40b287a38332cbaf61ca | hermes_bot |

---

## 五、发送 API

```bash
curl -s -X POST "https://im.deepminer.com.cn/api/v1/bot/sendMessage" \
  -H "Authorization: Bearer bf_f44080a9a3d4b527b2ab93c42dc9571c" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "{channel_id}",
    "channel_type": 2,
    "payload": {
      "type": 1,
      "content": "消息内容",
      "mention": {"uids": ["{worker_uid}"]}
    }
  }'
```

- `channel_type` 固定为 2（群聊）
- `mention` 字段只在消息 1（@Worker）时需要，其他消息不带

---

## 六、⚠️ 红线

1. **绝对不读 `tasks/pool/`** — 那里有 ground_truth，只用 `tasks/pool-clean/`
2. **不自行决定派发哪些卡** — 只发 dispatch-log.json 中 `status: assigned` 的
3. **不修改任务卡内容** — 原样发送 JSON
4. **不修改 dispatch-log.json** — 所有状态变更由 Pichai 操作
