---
name: game-design-orchestrator
description: Use when 需要组织多个游戏设计技能协同工作，并确保文档树、任务映射、ECS约束和交接流程一致
---

# 游戏设计协调器（严格流程）

## 适用条件
- 需求跨多个领域（玩法、关卡、角色、经济、埋点等）。
- 需要把设计输出沉淀为文档树并映射到 `bd` 任务。
- 需要统一仲裁 skill 间冲突。

## 阶段状态机
1. `需求澄清`：确认目标、范围、约束。
2. `领域产出`：路由到领域 skill 生成主文档。
3. `架构审查`：ECS 约束审查与技术门禁。
4. `映射收敛`：更新 `task-doc-map.yaml` 与 `bd`。
5. `交接封板`：生成 handoff 并转入 superpowers。

未通过当前阶段门禁，不得进入下一阶段。

## 输入契约
必填输入：
- 游戏类型与目标平台。
- 当前版本目标（设计/实现/交接）。
- 文档输出范围（必须落到 `docs/gamepowers/`）。

可选输入：
- 商业目标、用户画像、已有资产。

输入缺失处理：一次只问一个问题，不并发提问。

## 路由规则
- 愿景类：`game-vision-alignment`
- 循环与机制：`core-loop-architect`、`mechanic-spec-writer`
- 角色与成长：`combat-and-roles-designer`、`progression-structure-designer`
- 经济与平衡：`economy-model-designer`、`balance-framework`
- 内容与运营：`content-pipeline-planner`、`liveops-event-designer`
- 可观测与风控：`telemetry-kpi-designer`、`anti-cheat-and-exploit-review`
- 技术约束：`ecs-architecture-designer`
- 交接：`design-handoff-to-superpowers`

## 阶段门禁

### 需求澄清门禁
- 有明确目标和边界。
- 目录落点明确。

### 领域产出门禁
- 文档主结论遵循单一主写原则。
- 关键域文档齐备（愿景、循环、机制至少具备）。

### 架构审查门禁
- 技术任务已标记 `architecture: ECS`。
- 关键 ECS 文档已引用。

### 映射收敛门禁
- `task-doc-map.yaml` 无缺字段。
- `bd` 任务与文档引用一致。

### 交接封板门禁
- handoff 文档包含任务、文档、bd ID、ECS 契约。

## 文档索引更新规则
- 新增或迁移文档时，同步更新 `docs/gamepowers/index/domain-index.md`。
- 变更主文档 owner 时，同步更新 `docs/gamepowers/index/skill-doc-ownership.yaml`。

## bd 同步规则
- 任务状态以 `bd` 为准，Markdown 仅做人读。
- 每次阶段完成必须写 `bd comments` 记录证据文档路径。
- 如父任务阻塞子任务，允许自动关闭父 epic 以释放依赖图。

## 冲突仲裁与升级
- 一般冲突由本 skill 仲裁。
- 涉及技术实现与 ECS 的冲突升级给 `ecs-architecture-designer`。
- 仲裁结果必须记录 ADR（`docs/gamepowers/adr/`）。

## 反模式（禁止）
- 未完成门禁直接进入实现。
- 多个 skill 覆盖同一文档主结论。
- 未更新映射就同步 `bd`。

## 完成判定
- 文档树完整且可追溯。
- 映射与 `bd` 同步一致。
- handoff 可直接驱动 superpowers 实施。

## 最小输出示例
- 阶段状态：`映射收敛完成`。
- 证据：`docs/gamepowers/index/task-doc-map.yaml`、`docs/gamepowers/index/bd-task-map-*.json`。
