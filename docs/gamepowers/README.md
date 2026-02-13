# GamePowers 文档总览

本目录是 GamePowers 的设计事实源。

## 目录说明
- `gameplay/`：玩法总则、核心循环。
- `levels/`：关卡结构、关卡规则。
- `characters/`：角色定位与成长。
- `equipment/`：装备分层与掉落规则。
- `skills/`：技能系统与连招规则。
- `items/`：物品分类与用途。
- `economy/`：资源产消与货币体系。
- `liveops/`：赛季节奏与活动设计。
- `telemetry/`：埋点与指标体系。
- `anti-cheat/`：风险模型与对抗策略。
- `ecs/`：ECS 设计与性能预算。
- `tasks/`：人读任务清单。
- `index/`：索引与任务映射。
- `handoffs/`：交接 superpowers 的输入文档。

## 约束
- 主叙述与提示词必须使用中文。
- 技术任务必须声明 `architecture: ECS`。
- 每个可实现任务必须关联至少一个文档路径。
