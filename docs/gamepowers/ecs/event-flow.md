# 事件流

## 核心事件
- `SkillCastRequested`
- `SkillCastResolved`
- `DamageApplied`
- `EntityDefeated`
- `RewardGranted`

## 规则
- 事件不可直接修改外部状态。
- 状态变更必须由对应系统消费事件后执行。
