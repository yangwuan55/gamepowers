# Superpowers 执行入口（Kickoff）

## 使用目标
基于 GamePowers 产出的任务图和文档树，进入 superpowers 实现链路：
- `writing-plans`
- `test-driven-development`
- `systematic-debugging`

## 输入文件
- 任务映射：`docs/gamepowers/index/task-doc-map.yaml`
- bd 映射：`docs/gamepowers/index/bd-task-map-20260213-114941.json`
- 交接包：`docs/gamepowers/handoffs/generated-handoff-20260213-114941.md`

## 建议执行顺序
1. 从 `bd ready` 获取当前可执行任务（当前为 `gamepowers-64z.1`）。
2. 按任务依赖顺序推进，保证每个实现任务都引用对应文档。
3. 技术任务强制遵守 ECS 契约：
   - `docs/gamepowers/ecs/system-schedule.md`
   - `docs/gamepowers/ecs/event-flow.md`
   - `docs/gamepowers/ecs/performance-budget.md`

## 可直接使用的提示词（给 superpowers）
```text
请基于以下交接输入开始实现阶段：
1) /Users/ymr/github/gamepowers/docs/gamepowers/handoffs/generated-handoff-20260213-114941.md
2) /Users/ymr/github/gamepowers/docs/gamepowers/index/task-doc-map.yaml
3) /Users/ymr/github/gamepowers/docs/gamepowers/index/bd-task-map-20260213-114941.json

要求：
- 先调用 superpowers:writing-plans 生成实现计划
- 实施时严格遵守 superpowers:test-driven-development
- 遇到问题使用 superpowers:systematic-debugging
- 技术任务必须使用 ECS 架构，遵守调度与事件流文档
- 每完成一个任务后更新 bd 状态并保留文档引用
```

## 本地命令参考
```bash
cd /Users/ymr/github/gamepowers
bd ready --limit 20
bd show gamepowers-64z.1
```
