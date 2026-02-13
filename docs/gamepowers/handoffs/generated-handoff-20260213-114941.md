# GamePowers 自动交接包

生成时间: 2026-02-13T03:52:13.308400+00:00

## 输入来源
- 任务映射: `/Users/ymr/github/gamepowers/docs/gamepowers/index/task-doc-map.yaml`
- 任务清单: `docs/gamepowers/tasks/executable-task-list.md`
- 执行状态: `bd` 任务图

## 任务与文档关联
| TaskKey | bd ID | 架构 | 文档 |
|---|---|---|---|
| GP-001 | gamepowers-64z.1 | DESIGN | `docs/gamepowers/gameplay/gameplay-vision.md` |
| GP-002 | gamepowers-64z.2 | DESIGN | `docs/gamepowers/gameplay/core-loop-spec.md` |
| GP-003 | gamepowers-64z.3 | DESIGN | `docs/gamepowers/gameplay/mechanics-spec.md` |
| GP-004 | gamepowers-64z.4 | DESIGN | `docs/gamepowers/characters/character-roster.md` |
| GP-005 | gamepowers-64z.5 | DESIGN | `docs/gamepowers/levels/level-design-framework.md` |
| GP-006 | gamepowers-64z.6 | DESIGN | `docs/gamepowers/equipment/equipment-framework.md`, `docs/gamepowers/items/item-system-spec.md` |
| GP-007 | gamepowers-64z.7 | DESIGN | `docs/gamepowers/economy/economy-model.md` |
| GP-008 | gamepowers-64z.8 | DESIGN | `docs/gamepowers/liveops/season-event-framework.md` |
| GP-009 | gamepowers-64z.9 | DESIGN | `docs/gamepowers/telemetry/kpi-and-events.md` |
| GP-010 | gamepowers-64z.10 | ECS | `docs/gamepowers/ecs/ecs-principles.md`, `docs/gamepowers/ecs/entity-component-catalog.md` |
| GP-011 | gamepowers-64z.11 | ECS | `docs/gamepowers/ecs/system-schedule.md`, `docs/gamepowers/ecs/event-flow.md`, `docs/gamepowers/ecs/performance-budget.md` |
| GP-012 | gamepowers-64z.12 | ECS | `docs/gamepowers/handoffs/design-handoff-to-superpowers.md` |

## ECS 实现契约
- 技术任务必须使用 `ECS` 架构。
- 必须遵守系统调度顺序和事件流文档。
- 关键参考文档:
  - `docs/gamepowers/ecs/system-schedule.md`
  - `docs/gamepowers/ecs/event-flow.md`
  - `docs/gamepowers/ecs/performance-budget.md`

## 进入 superpowers
1. 调用 `superpowers:writing-plans`。
2. 按 `superpowers:test-driven-development` 实施。
3. 出现问题时使用 `superpowers:systematic-debugging`。
