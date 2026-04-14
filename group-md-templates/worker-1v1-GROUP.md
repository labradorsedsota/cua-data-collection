# GROUP.md - BugHunt 工作群 (PM ↔ Worker)

## 群定位
PM 与该 Worker 的专属工作通道。**Worker 的唯一信息源。**
任务分发、状态上报、异常处理、方案变更通知——所有影响执行的信息都从这里获取。

## 成员
- **PM (Pichai)**：任务分发、巡检、干预指令、方案变更推送
- **Worker ({worker名})**：执行任务、上报状态

## 通信协议

### PM → Worker：任务分发
PM 发任务批次，Worker 回复 ACK 后开始执行。
```
📋 新任务批次
执行: tasks/pool/luxesite-253.json, luxesite-258.json, cleaningsvc-18.json
顺序: 按列表顺序逐个执行
repo: git pull origin main 后读取 tasks/pool/ 下对应文件
执行手册: worker-execution-guide.md
```

### PM → Worker：方案变更
全局方案变更由 PM 在本群直接推送（不从其他群获取）。
```
⚠️ 方案变更
内容: 结果 JSON 新增 repo 字段，从任务卡原样复制
生效: 立即，下一个 case 开始执行
影响: completed 和 failed 两种格式都要加
```

### PM → Worker：干预指令
```
🛑 暂停执行（取消当前任务，等待新指令）
▶️ 恢复执行（继续之前的任务列表）
⏭️ 跳过当前 case（标 failed + other，进入下一个）
```

### Worker → PM：状态上报
**每完成一个 case，立刻发一行状态信号：**
```
✅ luxesite-253 | 4m32s | abnormal | 404页面无返回链接
❌ cleaningsvc-18 | deploy_failed | npm install node-gyp 编译错误
⚠️ lumen-300 | 12m10s | unclear | mano-cua 未走到关键步骤
```

**异常时紧跟状态信号发完整诊断：**
- 失败现象
- 已尝试的方案
- 建议

### Worker → Repo：结果持久化
- 每完成 5 个 case，批量 git push 结果 JSON 到 `results/{worker名}/`
- 异常 case 立刻 push，不等凑批

## Worker 行为规范
1. 收到任务 → 回复"收到，开始执行"
2. 每完成一个 case → 主动发状态信号（不等 PM 来问）
3. 遇到异常 → 立即上报 + 诊断，不要自己卡着不说
4. 超过 15 分钟没产出 → 主动说明原因（部署慢 / mano-cua 执行中 / 卡住了）
5. 收到 PM 的暂停/跳过/切换任务等指令 → 回复 ACK + 执行
6. 收到方案变更 → 回复"收到，已更新" + 从下一个 case 生效

## PM 行为规范
1. 分发任务时给明确列表，不说模糊的"继续跑"
2. 巡检时如果 Worker 超过 20 分钟没信号 → 主动询问
3. 干预指令必须明确：作废旧指令 + 新指令内容
4. 全局方案变更 → 在每个 1v1 群逐个推送（不依赖广播群）

## 禁止
- Worker 不在此群讨论与自己任务无关的内容
- PM 不在此群发与该 Worker 无关的其他 Worker 信息
