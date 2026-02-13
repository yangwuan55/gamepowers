# GamePowers 设计文档（全量版）

## 1. 目标与定位
- `GamePowers` 是 `superpowers` 的游戏领域扩展，不替代 `superpowers`。
- 主职责是把游戏设计从想法变成“可执行任务集合”，并通过 `bd` 管理生命周期。
- 编码、测试、调试阶段交给 `superpowers` 执行（如 `writing-plans`、`test-driven-development`、`systematic-debugging`）。

## 2. 核心原则
- 所有提示词、模板、默认输出使用中文。
- 任务执行来源是 `bd`，Markdown 任务清单只做人类可读视图。
- 设计资产必须文档化并可追溯到任务。
- 技术实现任务必须强制 `ECS` 架构。

## 3. 输出物模型

### 3.1 文档树（事实源）
路径：`docs/gamepowers/`

- `gameplay/`：玩法总则、核心循环
- `levels/`：关卡结构、关卡规则
- `characters/`：角色与职业体系
- `equipment/`：装备体系
- `skills/`：技能体系
- `items/`：物品体系
- `economy/`：货币与经济系统
- `liveops/`：活动与赛季
- `telemetry/`：埋点与指标
- `anti-cheat/`：反作弊与风控
- `ecs/`：ECS 架构规范
- `index/`：索引与映射
- `tasks/`：任务清单

### 3.2 任务清单（人读）
路径：`docs/gamepowers/tasks/executable-task-list.md`

- 提供可读任务列表、优先级、依赖、文档引用。
- 不作为状态源，仅用于沟通与审阅。

### 3.3 任务映射（机读）
路径：`docs/gamepowers/index/task-doc-map.yaml`

每个任务必须包含：
- `id`
- `title`
- `type`
- `priority`
- `architecture`（技术任务必须为 `ECS`）
- `docs[]`（可多个）
- `ecs_refs[]`（技术任务必填）
- `deps[]`
- `acceptance[]`

### 3.4 执行状态（bd）
- `bd` 是唯一执行状态源。
- 映射文件同步后，任务在 `bd` 中以父子关系与依赖关系管理。
- 每个 `bd` 任务必须带文档路径引用，确保实现时可回溯设计依据。

## 4. 角色设计

### 4.1 协调角色（必选）
新增技能：`game-design-orchestrator`

职责：
- 统一接收需求并路由到领域技能。
- 维护中文术语一致性与输出结构一致性。
- 验证任务-文档映射完整性。
- 在进入实现前生成交接包并调用 `superpowers` 工作流。

### 4.2 领域技能（全量）
- `game-vision-alignment`
- `core-loop-architect`
- `mechanic-spec-writer`
- `combat-and-roles-designer`
- `progression-structure-designer`
- `economy-model-designer`
- `balance-framework`
- `content-pipeline-planner`
- `liveops-event-designer`
- `anti-cheat-and-exploit-review`
- `telemetry-kpi-designer`
- `ecs-architecture-designer`
- `design-handoff-to-superpowers`

## 5. ECS 强约束

### 5.1 ECS 专业技能
新增：`ecs-architecture-designer`

必须产出：
- 实体边界
- 组件数据模型
- 系统职责与接口
- 系统调度顺序
- 事件流与状态同步
- 性能预算（帧耗时、批处理、内存）

### 5.2 交接前校验
进入 `superpowers` 前，技术任务必须满足：
- `architecture: ECS`
- 有 `ecs_refs[]`
- 引用了 ECS 文档组

不满足则阻塞交接。

## 6. 与 superpowers 的协作边界

### 6.1 GamePowers 负责
- 领域设计产出
- 文档树建设
- 任务定义与依赖图
- `bd` 任务同步
- ECS 技术约束前置

### 6.2 superpowers 负责
- 具体实现计划细化（`writing-plans`）
- 测试驱动开发（`test-driven-development`）
- 调试排障（`systematic-debugging`）
- 代码评审与分支收尾

## 7. 交接包定义
由 `design-handoff-to-superpowers` 生成：
- 人读任务清单（Markdown）
- 机读任务映射（YAML）
- `bd` 任务 ID 清单
- 文档引用矩阵
- ECS 实现契约

## 8. 验收标准
- 文档树完整：核心目录与文档存在。
- 任务可执行：任务可同步到 `bd` 且依赖可解。
- 追溯完整：每个任务至少关联一个文档；复杂任务可关联多个文档。
- ECS 合规：所有技术任务满足 ECS 字段与引用要求。
- 中文合规：技能提示词与模板输出为中文。
- 交接合规：交接包齐全后才可进入 superpowers 实现流程。

## 9. 风险与缓解
- 风险：文档树变大后维护成本上升。
  - 缓解：引入索引与映射校验脚本。
- 风险：任务与文档逐步失联。
  - 缓解：同步脚本执行前后做完整性检查。
- 风险：ECS 约束被实现阶段弱化。
  - 缓解：交接前强校验，缺失即阻塞。

## 10. 下一步
1. 生成实现计划文档（writing-plans 格式）。
2. 创建 GamePowers 技能目录与中文技能文件。
3. 建立文档树模板与任务映射模板。
4. 实现 `task-doc-map.yaml -> bd` 同步脚本。
5. 生成首批示例任务并同步到 `bd`。
6. 产出 `design-handoff` 示例供 superpowers 接管实现。
