# GamePowers Skill Hardening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将 14 个 GamePowers 专业 skill 升级为严格流程型规范，确保稳定输出、无跨 skill 冲突、文档树组织可治理。

**Architecture:** 采用分层模板（协调层/架构层/领域层）统一重写技能文档，再引入治理文件（归属、审查、冲突处理）与自动校验脚本（章节完整性检查）。通过测试验证改造可持续运行。

**Tech Stack:** Markdown、Python 3、unittest、bd CLI

---

### Task 1: 新增技能治理文件

**Files:**
- Create: `docs/gamepowers/index/skill-governance.md`
- Create: `docs/gamepowers/index/skill-doc-ownership.yaml`

**Step 1: Write the failing test**

```bash
cd /Users/ymr/github/gamepowers && test -f docs/gamepowers/index/skill-governance.md && test -f docs/gamepowers/index/skill-doc-ownership.yaml
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/ymr/github/gamepowers && test -f docs/gamepowers/index/skill-governance.md && test -f docs/gamepowers/index/skill-doc-ownership.yaml; echo $?`
Expected: `1`

**Step 3: Write minimal implementation**

- 写入文档树规范、单一主写原则、冲突仲裁规则。
- 写入每个 skill 的 owner/reviewer 关系。

**Step 4: Run test to verify it passes**

Run: `cd /Users/ymr/github/gamepowers && test -f docs/gamepowers/index/skill-governance.md && test -f docs/gamepowers/index/skill-doc-ownership.yaml; echo $?`
Expected: `0`

**Step 5: Commit**

```bash
git add docs/gamepowers/index/skill-governance.md docs/gamepowers/index/skill-doc-ownership.yaml
git commit -m "docs: add skill governance and ownership contract"
```

### Task 2: 重写协调层 skill

**Files:**
- Modify: `skills/game-design-orchestrator/SKILL.md`
- Modify: `skills/design-handoff-to-superpowers/SKILL.md`

**Step 1: Write the failing test**

```bash
cd /Users/ymr/github/gamepowers && rg -n "阶段状态机|阶段门禁|冲突仲裁|bd 同步规则|完成判定" skills/game-design-orchestrator/SKILL.md skills/design-handoff-to-superpowers/SKILL.md
```

**Step 2: Run test to verify it fails**

Run: 同上命令
Expected: 缺少若干关键章节。

**Step 3: Write minimal implementation**

- 引入协调层强模板。
- 增加路由优先级、门禁、冲突处理、失败升级、bd 联动。

**Step 4: Run test to verify it passes**

Run: 同上命令
Expected: 两个文件都能匹配全部关键章节。

**Step 5: Commit**

```bash
git add skills/game-design-orchestrator/SKILL.md skills/design-handoff-to-superpowers/SKILL.md
git commit -m "docs: harden orchestrator-layer skills"
```

### Task 3: 重写架构层 skill

**Files:**
- Modify: `skills/ecs-architecture-designer/SKILL.md`

**Step 1: Write the failing test**

```bash
cd /Users/ymr/github/gamepowers && rg -n "强制校验清单|禁止项|验证与回滚|否决权|系统调度|事件流|性能预算" skills/ecs-architecture-designer/SKILL.md
```

**Step 2: Run test to verify it fails**

Run: 同上命令
Expected: 缺少若干关键章节。

**Step 3: Write minimal implementation**

- 增加 ECS 强校验矩阵与回滚策略。
- 明确技术冲突否决机制。

**Step 4: Run test to verify it passes**

Run: 同上命令
Expected: 所有关键章节存在。

**Step 5: Commit**

```bash
git add skills/ecs-architecture-designer/SKILL.md
git commit -m "docs: harden ecs architecture skill with strict gates"
```

### Task 4: 重写 11 个领域层 skill

**Files:**
- Modify: `skills/game-vision-alignment/SKILL.md`
- Modify: `skills/core-loop-architect/SKILL.md`
- Modify: `skills/mechanic-spec-writer/SKILL.md`
- Modify: `skills/combat-and-roles-designer/SKILL.md`
- Modify: `skills/progression-structure-designer/SKILL.md`
- Modify: `skills/economy-model-designer/SKILL.md`
- Modify: `skills/balance-framework/SKILL.md`
- Modify: `skills/content-pipeline-planner/SKILL.md`
- Modify: `skills/liveops-event-designer/SKILL.md`
- Modify: `skills/telemetry-kpi-designer/SKILL.md`
- Modify: `skills/anti-cheat-and-exploit-review/SKILL.md`

**Step 1: Write the failing test**

```bash
cd /Users/ymr/github/gamepowers && for f in skills/game-vision-alignment/SKILL.md skills/core-loop-architect/SKILL.md skills/mechanic-spec-writer/SKILL.md skills/combat-and-roles-designer/SKILL.md skills/progression-structure-designer/SKILL.md skills/economy-model-designer/SKILL.md skills/balance-framework/SKILL.md skills/content-pipeline-planner/SKILL.md skills/liveops-event-designer/SKILL.md skills/telemetry-kpi-designer/SKILL.md skills/anti-cheat-and-exploit-review/SKILL.md; do rg -n "输入契约|设计步骤|输出工件|质量门禁|风险|反模式|完成判定" "$f" >/dev/null || echo "MISSING:$f"; done
```

**Step 2: Run test to verify it fails**

Run: 同上命令
Expected: 至少部分文件输出 `MISSING`。

**Step 3: Write minimal implementation**

- 统一为领域层严格模板。
- 每个 skill 加入本域专用质量门禁与风险控制。

**Step 4: Run test to verify it passes**

Run: 同上命令
Expected: 无 `MISSING` 输出。

**Step 5: Commit**

```bash
git add skills/game-vision-alignment/SKILL.md skills/core-loop-architect/SKILL.md skills/mechanic-spec-writer/SKILL.md skills/combat-and-roles-designer/SKILL.md skills/progression-structure-designer/SKILL.md skills/economy-model-designer/SKILL.md skills/balance-framework/SKILL.md skills/content-pipeline-planner/SKILL.md skills/liveops-event-designer/SKILL.md skills/telemetry-kpi-designer/SKILL.md skills/anti-cheat-and-exploit-review/SKILL.md
git commit -m "docs: harden domain-layer skills with strict process templates"
```

### Task 5: 增加自动校验脚本与测试

**Files:**
- Create: `tools/validate_skills_contract.py`
- Create: `tests/test_validate_skills_contract.py`

**Step 1: Write the failing test**

```bash
cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_validate_skills_contract.py -v
```

**Step 2: Run test to verify it fails**

Run: 同上命令
Expected: 失败（文件未创建）。

**Step 3: Write minimal implementation**

- 校验每个层级 skill 是否包含必须章节。
- 校验 description 使用 `Use when` 触发格式。

**Step 4: Run test to verify it passes**

Run:
```bash
cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_validate_skills_contract.py -v
cd /Users/ymr/github/gamepowers && python3 tools/validate_skills_contract.py
```
Expected: PASS。

**Step 5: Commit**

```bash
git add tools/validate_skills_contract.py tests/test_validate_skills_contract.py
git commit -m "test: add contract validation for hardened skills"
```

### Task 6: 回归验证与说明更新

**Files:**
- Modify: `README.md`

**Step 1: Write the failing test**

```bash
cd /Users/ymr/github/gamepowers && rg -n "validate_skills_contract|skill-governance|skill-doc-ownership" README.md
```

**Step 2: Run test to verify it fails**

Run: 同上命令
Expected: 无匹配或不完整。

**Step 3: Write minimal implementation**

- README 增加 skill 治理与校验命令说明。

**Step 4: Run test to verify it passes**

Run:
```bash
cd /Users/ymr/github/gamepowers && rg -n "validate_skills_contract|skill-governance|skill-doc-ownership" README.md
cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_validate_task_map.py tests/test_sync_tasks_to_bd.py tests/test_cli_commands.py tests/test_validate_skills_contract.py -v
```
Expected: 全部通过。

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs: document strict skill governance and validation"
```
