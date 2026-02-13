# 可执行任务清单（人读）

> 说明：本文件用于人类审阅，实际执行状态以 `bd` 为准。

## 任务树

- `GP-001` 定义玩法愿景与边界
  - docs: `docs/gamepowers/gameplay/gameplay-vision.md`
- `GP-002` 定义核心循环与状态机
  - deps: `GP-001`
  - docs: `docs/gamepowers/gameplay/core-loop-spec.md`
- `GP-003` 编写机制规格与冲突优先级
  - deps: `GP-002`
  - docs: `docs/gamepowers/gameplay/mechanics-spec.md`
- `GP-004` 设计角色与战斗定位
  - deps: `GP-002`
  - docs: `docs/gamepowers/characters/character-roster.md`
- `GP-005` 设计关卡框架与难度曲线
  - deps: `GP-002`
  - docs: `docs/gamepowers/levels/level-design-framework.md`
- `GP-006` 设计装备与物品框架
  - deps: `GP-003`
  - docs: `docs/gamepowers/equipment/equipment-framework.md`, `docs/gamepowers/items/item-system-spec.md`
- `GP-007` 设计经济与平衡框架
  - deps: `GP-003`, `GP-006`
  - docs: `docs/gamepowers/economy/economy-model.md`
- `GP-008` 设计 LiveOps 活动节奏
  - deps: `GP-007`
  - docs: `docs/gamepowers/liveops/season-event-framework.md`
- `GP-009` 定义埋点与指标口径
  - deps: `GP-002`, `GP-007`
  - docs: `docs/gamepowers/telemetry/kpi-and-events.md`
- `GP-010` ECS 架构蓝图（技术）
  - deps: `GP-003`, `GP-004`, `GP-005`
  - architecture: `ECS`
  - docs: `docs/gamepowers/ecs/ecs-principles.md`, `docs/gamepowers/ecs/entity-component-catalog.md`
- `GP-011` ECS 调度与性能预算（技术）
  - deps: `GP-009`, `GP-010`
  - architecture: `ECS`
  - docs: `docs/gamepowers/ecs/system-schedule.md`, `docs/gamepowers/ecs/event-flow.md`, `docs/gamepowers/ecs/performance-budget.md`
- `GP-012` 交接 superpowers 的实现包
  - deps: `GP-008`, `GP-009`, `GP-011`
  - architecture: `ECS`
  - docs: `docs/gamepowers/handoffs/design-handoff-to-superpowers.md`

## 交接门槛
- 技术任务必须满足 `architecture: ECS`。
- 任一任务可关联多个文档。
- 执行前必须已同步到 `bd` 并校验依赖图。
