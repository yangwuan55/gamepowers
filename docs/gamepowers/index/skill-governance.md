# Skill 治理规范（严格流程型）

## 1. 目标
本规范用于约束 GamePowers 的 skill 协作方式，确保：
- 输出稳定可复现
- 文档组织结构清晰
- skill 间不产生冲突结论

## 2. 文档树组织

### 2.1 固定层级
- `docs/gamepowers/index/`：索引、映射、治理规则。
- `docs/gamepowers/domains/<domain>/`：领域主文档（逐步迁移目标）。
- `docs/gamepowers/cross-cutting/`：跨域约束（ECS、经济、平衡、埋点、风控）。
- `docs/gamepowers/tasks/`：任务清单与执行分解。
- `docs/gamepowers/handoffs/`：交接包与执行入口。
- `docs/gamepowers/adr/`：冲突仲裁记录。

### 2.2 兼容策略
当前已有 `gameplay/levels/characters/...` 目录继续生效。迁移期间由 `index/domain-index.md` 维护新旧路径映射。

## 3. 所有 skill 通用硬约束
- 主叙述与模板必须中文。
- 输入缺失时一次只问一个问题。
- 每个结论必须可追溯到文档路径。
- 每个任务必须可映射到 `task-doc-map.yaml`。
- 任何技术任务必须满足 `architecture: ECS`。

## 4. 单一主写原则

### 4.1 定义
- 一个文档仅允许一个 `owner_skill` 写入主结论。
- 其他 skill 只能写建议区或审查意见。

### 4.2 禁止行为
- 非 owner_skill 直接覆盖主结论。
- 同一字段被两个 skill 定义为不同含义。

## 5. 冲突仲裁流程
1. 发现冲突：记录冲突点与涉及文档。
2. 临时冻结：冲突字段停止继续扩写。
3. 仲裁归口：
   - 一般冲突：`game-design-orchestrator`
   - 技术冲突：`ecs-architecture-designer`（拥有否决权）
4. 记录 ADR：写入 `docs/gamepowers/adr/`。
5. 同步映射：更新 `task-doc-map.yaml` 与 `bd` 任务说明。

## 6. 分层协作协议

### 6.1 协调层
- 负责阶段编排、门禁、路由、交接。
- 负责冲突治理与任务追溯闭环。

### 6.2 架构层
- 负责 ECS 约束落地与技术一致性。
- 负责调度/事件流/性能预算校验。

### 6.3 领域层
- 负责本域工件生产。
- 负责本域风险识别与缓解策略。
- 遵守协调层和架构层门禁。

## 7. 质量门禁
- 结构完整性：必填章节齐全。
- 一致性：术语与口径不冲突。
- 可执行性：能映射成任务并关联文档。
- 可验证性：有验收标准与失败处理。

## 8. 发布前检查
1. 运行 `python3 tools/validate_skills_contract.py`。
2. 运行 `python3 tools/validate_task_map.py --map docs/gamepowers/index/task-doc-map.yaml`。
3. 若有冲突条目，必须先完成 ADR 才可交接。
