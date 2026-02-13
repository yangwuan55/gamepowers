# 设计交接包（示例）

## 输入来源
- 任务清单：`docs/gamepowers/tasks/executable-task-list.md`
- 任务映射：`docs/gamepowers/index/task-doc-map.yaml`
- 执行状态：`bd` 任务图

## 任务与 bd ID 对照
| TaskKey | bd ID | 主要文档 |
|---|---|---|
| GP-001 | gamepowers-629.1 | `docs/gamepowers/gameplay/gameplay-vision.md` |
| GP-002 | gamepowers-629.2 | `docs/gamepowers/gameplay/core-loop-spec.md` |
| GP-003 | gamepowers-629.3 | `docs/gamepowers/gameplay/mechanics-spec.md` |
| GP-004 | gamepowers-629.4 | `docs/gamepowers/characters/character-roster.md` |
| GP-005 | gamepowers-629.5 | `docs/gamepowers/levels/level-design-framework.md` |
| GP-006 | gamepowers-629.6 | `docs/gamepowers/equipment/equipment-framework.md`, `docs/gamepowers/items/item-system-spec.md` |
| GP-007 | gamepowers-629.7 | `docs/gamepowers/economy/economy-model.md` |
| GP-008 | gamepowers-629.8 | `docs/gamepowers/liveops/season-event-framework.md` |
| GP-009 | gamepowers-629.9 | `docs/gamepowers/telemetry/kpi-and-events.md` |
| GP-010 | gamepowers-629.10 | `docs/gamepowers/ecs/ecs-principles.md`, `docs/gamepowers/ecs/entity-component-catalog.md` |
| GP-011 | gamepowers-629.11 | `docs/gamepowers/ecs/system-schedule.md`, `docs/gamepowers/ecs/event-flow.md`, `docs/gamepowers/ecs/performance-budget.md` |
| GP-012 | gamepowers-629.12 | `docs/gamepowers/handoffs/design-handoff-to-superpowers.md` |

## ECS 实现契约
- 架构必须为 `ECS`
- 系统调度顺序参考：`docs/gamepowers/ecs/system-schedule.md`
- 事件流参考：`docs/gamepowers/ecs/event-flow.md`
- 性能预算参考：`docs/gamepowers/ecs/performance-budget.md`
- 技术任务必须包含 `architecture: ECS` 与 `ecs_refs[]`

## 多文档依赖约束
- 实现任务允许依赖多个文档，必须在任务描述中明确列出全部文档路径。
- 任一文档变更后，应回查关联任务并评估是否需要重新计划。

## 交接动作
1. 调用 `superpowers:writing-plans`
2. 实施时遵循 `superpowers:test-driven-development`
3. 问题排查使用 `superpowers:systematic-debugging`
