---
name: design-handoff-to-superpowers
description: Use when 设计阶段已完成并需要生成可执行交接包，驱动 superpowers 进入实现流程
---

# 设计交接到 Superpowers（严格流程）

## 适用条件
- 设计文档与任务映射已完成。
- 需要进入 superpowers 的实现链路。

## 阶段状态机
1. `交接准备`：收集映射、bd、ECS 证据。
2. `交接校验`：执行结构与一致性门禁。
3. `交接发布`：生成交接包与执行入口。
4. `回执闭环`：记录交接结果并回写任务状态。

未通过当前阶段门禁，不得进入下一阶段。

## 输入契约
必填输入：
- `task-doc-map.yaml`
- 最新 `bd-task-map*.json`
- ECS 关键文档路径

可选输入：
- 版本目标、实施优先级、外部约束。

输入缺失处理：一次只问一个问题，不并发追问。

## 路由规则
- 映射缺失或结构问题：回退 `game-design-orchestrator` 修复。
- ECS 契约冲突：升级 `ecs-architecture-designer` 仲裁。
- `bd` 数据异常：回退 `game-design-orchestrator` 重新同步。

## 阶段门禁

### 交接准备门禁
- `task-doc-map.yaml` 可读取且结构完整。
- 最新 `bd-task-map*.json` 存在且可解析。
- ECS 关键文档引用齐全。

### 交接校验门禁
- `validate_task_map` 通过。
- `bd` 任务存在且依赖关系可解。
- 技术任务均为 `architecture: ECS` 且有 `ecs_refs`。

### 交接发布门禁
- 输出工件三件套生成成功。
- 任务表、文档引用表、bd ID、ECS 契约齐备。

### 回执闭环门禁
- 交接结果已写回任务说明。
- 失败原因已记录并指向修复路径。

## 交接流程
1. 汇总任务-文档-bd ID 三向关系。
2. 注入 ECS 契约与参考文档。
3. 生成 kickoff 文档和执行摘要。
4. 给出 superpowers 调用入口提示词。

## 输出工件
- `generated-handoff-*.md`
- `superpowers-execution-kickoff-*.md`
- `superpowers-execution-summary-*.md`

## 文档索引更新规则
- 生成交接包后，更新 `docs/gamepowers/index/domain-index.md` 的交接入口引用。
- 若输出命名变化，必须同步记录到 `docs/gamepowers/index/task-doc-map.yaml` 关联字段。

## bd 同步规则
- 交接前后均以 `bd` 状态为准，Markdown 仅做人读。
- 交接完成后必须在对应任务写 `bd comments`，附交接文档路径证据。
- 交接失败时不得关闭任务，必须写入失败原因与修复入口。

## 冲突仲裁与升级
- 任务与文档不一致：回退协调层修复映射。
- 技术口径冲突：升级至 `ecs-architecture-designer`。
- `bd` 数据缺失：禁止交接并先完成同步修复。
- ECS 门禁不通过：禁止调用 superpowers 实施。

## 与 superpowers 联动
按顺序调用：
1. `superpowers:writing-plans`
2. `superpowers:test-driven-development`
3. `superpowers:systematic-debugging`

## 反模式（禁止）
- 只交 Markdown 不交 `bd` 映射。
- 跳过 ECS 契约直接交接。
- 未记录文档证据就关闭任务。

## 完成判定
- 交接包可独立被 superpowers 使用。
- `bd` 与文档引用一致。
- 执行入口文档可直接复制运行。
