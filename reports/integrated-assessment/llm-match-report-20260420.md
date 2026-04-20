# BugHunt 轨迹匹配报告（LLM 判定）

> 生成时间：2026-04-20 16:32
> 模型：claude-haiku-4-5
> 范围：completed + mano_cua.status=COMPLETED（共 379 张）

## 统计

| 结果 | 数量 | 占比 |
|------|------|------|
| ✅ 匹配 | 364 | 96.0% |
| ❌ 不匹配 | 10 | 2.6% |
| ⚠️ 无数据 | 2 | 0.5% |
| 🔴 错误 | 3 | 0.8% |

## 不匹配卡明细

| task_id | worker | confidence | reason |
|---------|--------|------------|--------|
| Semantic-UI-React-3750 | worker-02 | 0.85 | 任务卡重点测试嵌套shorthand props设置input ref的属性保留行为，而轨迹任务重点测试搜索功能的完整流程，两者测试焦点和验证目标不同。 |
| open5e-622 | worker-02 | 0.85 | 轨迹中的任务在第5步额外增加了'用DevTools检查逗号元素的CSS属性'的要求，而任务卡描述中明确禁止打开Terminal或其他应用程序，DevTools检查违反了此约束。 |
| open5e-716 | worker-02 | 0.85 | 任务卡禁止打开DevTools，但轨迹中第4步要求打开DevTools检查Console错误，这是核心差异。 |
| cboard-1752 | worker-03 | 0.85 | 任务卡要求验证开关状态持久化（切换后离开再重新进入应显示相同状态），而轨迹任务仅要求验证切换时的即时状态变更，两者验证重点不同。 |
| beercss-532 | worker-05 | 0.85 | 轨迹描述中button测试目标是'观察是否保持高亮'，与任务卡要求的'恢复到正常未聚焦外观'存在矛盾，说明两者测试预期结果不一致。 |
| tailwindcss-987 | worker-08 | 0.85 | 轨迹中要求按F12打开Console检查安全策略错误，与任务卡禁止打开Terminal或其他应用程序的要求存在矛盾，表明两者对测试方法的理解存在偏差。 |
| multiple-select-407 | worker-09 | 0.85 | 任务卡仅要求测试Basic example的多选功能，而轨迹中的实际任务扩展了测试范围，额外包含了With OptGroups和Single Select部分的测试，超出了原始任务描述的范围。 |
| openclaw-nerve-27 | worker-09 | 0.92 | 任务卡要求测试Memory查看功能的基本流程（导航、查看列表、点击查看详情），而轨迹任务额外要求执行DevTools Console命令修改DOM状态，这是完全不同的操作路径和测试目标。 |
| website-4366 | worker-09 | 0.99 | 两段文本描述的是完全不同的功能测试：任务卡描述的是Newsletter邮件订阅功能，而轨迹中的实际任务是搜索功能测试，两者在测试目标、操作步骤和验证点上都没有重叠。 |
| vcal-350 | worker-fabrice | 0.85 | 任务卡要求检查选中和悬停两种状态的高亮效果，而轨迹中的实际任务仅描述了选中状态的检查，缺少悬停状态的验证要求。 |

## 无数据卡

| task_id | worker | 原因 |
|---------|--------|------|
| open5e-622 | worker-07 | no_trajectory |
| org-chart-290 | worker-07 | no_trajectory |