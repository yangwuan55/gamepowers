---
name: progression-structure-designer
description: Use when 需要设计长期成长、装备与物品解锁结构，并形成稳定的成长节奏
---

# 成长结构设计（严格流程）

## 适用条件
- 需要规划长期成长路径、解锁树、里程碑奖励。
- 需要定义装备与物品系统的成长作用。

## 输入契约
必填输入：
- 循环与机制文档：`docs/gamepowers/gameplay/core-loop-spec.md`、`docs/gamepowers/gameplay/mechanics-spec.md`
- 角色体系文档：`docs/gamepowers/characters/character-roster.md`
- 目标成长周期与版本节奏要求。

可选输入：
- 用户分层付费行为、流失点数据。

输入缺失处理：一次只问一个问题，不并发追问。

## 设计步骤
1. 成长阶段划分：定义新手期、成长期、深度期目标。
完成定义：每阶段有可达目标和退出条件。
2. 解锁树设计：定义装备、物品、能力解锁路径。
完成定义：解锁依赖明确且无闭环死锁。
3. 里程碑奖励规划：定义关键节点激励与回报强度。
完成定义：里程碑奖励与阶段目标一一对应。
4. 防卡关机制设计：定义失败兜底与补偿路径。
完成定义：高风险卡点均有可执行缓解策略。
5. 任务映射固化：把成长结构映射到可实现任务。
完成定义：关键解锁链路具备任务与验收条目。

## 输出工件
- 主文档：`docs/gamepowers/equipment/equipment-framework.md`
- 主文档：`docs/gamepowers/items/item-system-spec.md`
- 审查输入：`docs/gamepowers/characters/character-roster.md`（建议区）
- 任务映射证据：`docs/gamepowers/index/task-doc-map.yaml`

## 质量门禁
- 成长阶段、解锁树、奖励策略、兜底机制齐备。
- 所有关键依赖可追溯，无循环依赖。
- 相关任务可同步到 `bd` 且验收标准明确。

## 风险与缓解
- 风险：成长曲线过陡造成中期流失。
缓解：引入阶段补偿与可替代成长路径。
- 风险：装备与物品增长失控。
缓解：与经济/平衡技能联审关键阈值。

## 与 ECS/协调层联动
- 技术落地任务统一标注 `architecture: ECS` 并补充 `ecs_refs`。
- 由 `game-design-orchestrator` 管理成长任务排序与 `bd` 依赖。
- 与 `ecs-architecture-designer` 对齐成长状态持久化与系统职责边界。

## 反模式（禁止）
- 只给“长期成长目标”，不给阶段路径和依赖。
- 在角色文档中直接覆盖角色主结论。
- 成长任务未映射就推进实现。

## 完成判定
- 成长结构可稳定驱动长期内容生产。
- 装备与物品文档可直接支持实施拆分。
- 与 ECS 约束和任务映射一致。
