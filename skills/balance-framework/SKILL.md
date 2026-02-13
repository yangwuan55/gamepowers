---
name: balance-framework
description: Use when 需要建立数值平衡框架、调参与回归机制，保障玩法与经济长期稳定
---

# 平衡框架（严格流程）

## 适用条件
- 需要定义跨玩法、角色、经济的统一平衡策略。
- 需要建立调参、回归与发布门禁流程。

## 输入契约
必填输入：
- 机制与角色文档：`docs/gamepowers/gameplay/mechanics-spec.md`、`docs/gamepowers/characters/character-roster.md`
- 经济文档：`docs/gamepowers/economy/economy-model.md`
- KPI 与监控指标定义。

可选输入：
- 历史版本调参记录、对局胜率分布、经济波动数据。

输入缺失处理：一次只问一个问题，不并发追问。

## 设计步骤
1. 变量字典定义：梳理核心平衡变量及其影响范围。
完成定义：变量命名统一且依赖关系明确。
2. 基线公式建立：建立伤害、收益、成长等基础公式。
完成定义：每个公式有边界区间与异常处理。
3. 调参杠杆设计：定义可调参数与优先级顺序。
完成定义：调参不破坏核心体验边界。
4. 回归检查机制：定义版本前后对比指标与报警阈值。
完成定义：关键指标具备自动回归检查规则。
5. 发布门禁固化：定义上线前必须通过的平衡检查项。
完成定义：不满足门禁的版本不可进入交接。

## 输出工件
- 主文档：`docs/gamepowers/economy/balance-framework.md`
- 审查输入：`docs/gamepowers/gameplay/mechanics-spec.md`、`docs/gamepowers/economy/economy-model.md`（建议区）
- 任务映射证据：`docs/gamepowers/index/task-doc-map.yaml`

## 质量门禁
- 变量字典、公式基线、调参杠杆、回归门禁齐备。
- 每个关键指标有阈值与失败处置策略。
- 平衡任务可映射并同步到 `bd`。

## 风险与缓解
- 风险：单点调参引发跨系统连锁失衡。
缓解：引入跨域影响评估并执行回归门禁。
- 风险：调参口径漂移导致结论不可复现。
缓解：固定变量字典和基线公式版本号。

## 与 ECS/协调层联动
- 将关键平衡检查点映射到 ECS 系统观测任务。
- 由 `game-design-orchestrator` 协调平衡变更的优先级与发布窗口。
- 与 `ecs-architecture-designer` 对齐性能与事件采样成本。

## 反模式（禁止）
- 只给“感觉平衡”，不提供量化指标。
- 直接覆盖经济模型主结论。
- 不做回归检查就发布调参方案。

## 完成判定
- 平衡框架可支撑持续调参与版本发布。
- 回归门禁可执行且有明确失败处理。
- 与任务映射、ECS 约束保持一致。
