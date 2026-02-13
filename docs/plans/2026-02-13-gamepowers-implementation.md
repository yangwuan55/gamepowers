# GamePowers 全量功能 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个中文优先、ECS 强约束、可将设计文档树同步为 `bd` 可执行任务图的 GamePowers 技能扩展。

**Architecture:** 采用“技能层 + 文档层 + 任务同步层”三层结构。技能层负责游戏设计编排与 ECS 设计约束；文档层沉淀玩法到经济的树形规范；任务同步层把机读映射转换为 `bd` 任务与依赖，作为唯一执行状态源。编码实现阶段通过交接技能移交给 superpowers。

**Tech Stack:** Markdown Skills、Python 3（argparse/json/subprocess/unittest）、bd CLI

---

### Task 1: 建立项目骨架与入口文档

**Files:**
- Create: `README.md`
- Create: `docs/gamepowers/index/domain-index.md`
- Create: `docs/gamepowers/README.md`

**Step 1: Write the failing test**

```bash
test -f README.md && test -f docs/gamepowers/README.md && test -f docs/gamepowers/index/domain-index.md
```

期望：命令返回非 0（文件尚不存在）。

**Step 2: Run test to verify it fails**

Run: `test -f README.md && test -f docs/gamepowers/README.md && test -f docs/gamepowers/index/domain-index.md; echo $?`
Expected: 输出 `1`。

**Step 3: Write minimal implementation**

- 写入项目入口说明、目录说明、使用流程。

**Step 4: Run test to verify it passes**

Run: `test -f README.md && test -f docs/gamepowers/README.md && test -f docs/gamepowers/index/domain-index.md; echo $?`
Expected: 输出 `0`。

**Step 5: Commit**

```bash
git add README.md docs/gamepowers/README.md docs/gamepowers/index/domain-index.md
git commit -m "docs: add gamepowers project skeleton"
```

### Task 2: 实现 GamePowers 技能全集（中文提示词）

**Files:**
- Create: `skills/game-design-orchestrator/SKILL.md`
- Create: `skills/game-vision-alignment/SKILL.md`
- Create: `skills/core-loop-architect/SKILL.md`
- Create: `skills/mechanic-spec-writer/SKILL.md`
- Create: `skills/combat-and-roles-designer/SKILL.md`
- Create: `skills/progression-structure-designer/SKILL.md`
- Create: `skills/economy-model-designer/SKILL.md`
- Create: `skills/balance-framework/SKILL.md`
- Create: `skills/content-pipeline-planner/SKILL.md`
- Create: `skills/liveops-event-designer/SKILL.md`
- Create: `skills/anti-cheat-and-exploit-review/SKILL.md`
- Create: `skills/telemetry-kpi-designer/SKILL.md`
- Create: `skills/ecs-architecture-designer/SKILL.md`
- Create: `skills/design-handoff-to-superpowers/SKILL.md`

**Step 1: Write the failing test**

```bash
[ -d skills ] && [ "$(find skills -name SKILL.md | wc -l | tr -d ' ')" -ge 14 ]
```

期望：返回非 0（技能文件未齐全）。

**Step 2: Run test to verify it fails**

Run: `[ -d skills ] && [ "$(find skills -name SKILL.md | wc -l | tr -d ' ')" -ge 14 ]; echo $?`
Expected: 输出 `1`。

**Step 3: Write minimal implementation**

- 为每个技能写中文触发描述与输出规范。
- `ecs-architecture-designer` 明确 ECS 约束。
- `design-handoff-to-superpowers` 明确交接流程。

**Step 4: Run test to verify it passes**

Run: `[ -d skills ] && [ "$(find skills -name SKILL.md | wc -l | tr -d ' ')" -ge 14 ]; echo $?`
Expected: 输出 `0`。

补充验证：

```bash
rg -n "description: Use when" skills -g 'SKILL.md'
rg -n "中文|ECS|superpowers" skills -g 'SKILL.md'
```

**Step 5: Commit**

```bash
git add skills
git commit -m "feat: add gamepowers full skill set in Chinese"
```

### Task 3: 生成全量设计文档树与 ECS 文档组

**Files:**
- Create: `docs/gamepowers/gameplay/README.md`
- Create: `docs/gamepowers/levels/README.md`
- Create: `docs/gamepowers/characters/README.md`
- Create: `docs/gamepowers/equipment/README.md`
- Create: `docs/gamepowers/skills/README.md`
- Create: `docs/gamepowers/items/README.md`
- Create: `docs/gamepowers/economy/README.md`
- Create: `docs/gamepowers/liveops/README.md`
- Create: `docs/gamepowers/telemetry/README.md`
- Create: `docs/gamepowers/anti-cheat/README.md`
- Create: `docs/gamepowers/ecs/ecs-principles.md`
- Create: `docs/gamepowers/ecs/entity-component-catalog.md`
- Create: `docs/gamepowers/ecs/system-schedule.md`
- Create: `docs/gamepowers/ecs/event-flow.md`
- Create: `docs/gamepowers/ecs/performance-budget.md`

**Step 1: Write the failing test**

```bash
test -f docs/gamepowers/ecs/ecs-principles.md && test -f docs/gamepowers/levels/README.md
```

期望：返回非 0。

**Step 2: Run test to verify it fails**

Run: `test -f docs/gamepowers/ecs/ecs-principles.md && test -f docs/gamepowers/levels/README.md; echo $?`
Expected: 输出 `1`。

**Step 3: Write minimal implementation**

- 写各领域模板文档。
- ECS 文档明确实体/组件/系统/调度/性能预算。

**Step 4: Run test to verify it passes**

Run: `test -f docs/gamepowers/ecs/ecs-principles.md && test -f docs/gamepowers/levels/README.md; echo $?`
Expected: 输出 `0`。

**Step 5: Commit**

```bash
git add docs/gamepowers
git commit -m "docs: add full game design tree and ecs docs"
```

### Task 4: 定义可执行任务清单与机读映射

**Files:**
- Create: `docs/gamepowers/tasks/executable-task-list.md`
- Create: `docs/gamepowers/index/task-doc-map.yaml`

**Step 1: Write the failing test**

```bash
test -f docs/gamepowers/tasks/executable-task-list.md && test -f docs/gamepowers/index/task-doc-map.yaml
```

期望：返回非 0。

**Step 2: Run test to verify it fails**

Run: `test -f docs/gamepowers/tasks/executable-task-list.md && test -f docs/gamepowers/index/task-doc-map.yaml; echo $?`
Expected: 输出 `1`。

**Step 3: Write minimal implementation**

- Markdown 任务清单写人读视图。
- YAML 写机读视图，确保每项包含 `docs[]`、`deps[]`、`architecture`、`ecs_refs[]`。

**Step 4: Run test to verify it passes**

Run: `test -f docs/gamepowers/tasks/executable-task-list.md && test -f docs/gamepowers/index/task-doc-map.yaml; echo $?`
Expected: 输出 `0`。

**Step 5: Commit**

```bash
git add docs/gamepowers/tasks/executable-task-list.md docs/gamepowers/index/task-doc-map.yaml
git commit -m "docs: add executable task list and task-doc mapping"
```

### Task 5: 实现 task-doc-map 到 bd 的同步工具

**Files:**
- Create: `tools/sync_tasks_to_bd.py`
- Create: `tools/validate_task_map.py`

**Step 1: Write the failing test**

```bash
python3 tools/validate_task_map.py --map docs/gamepowers/index/task-doc-map.yaml
```

期望：命令失败（脚本不存在）。

**Step 2: Run test to verify it fails**

Run: `python3 tools/validate_task_map.py --map docs/gamepowers/index/task-doc-map.yaml; echo $?`
Expected: 输出非 `0`。

**Step 3: Write minimal implementation**

- `validate_task_map.py`：校验必填字段、依赖引用、ECS 字段完整性。
- `sync_tasks_to_bd.py`：读取映射并创建/更新 bd 任务、添加依赖、写入文档引用说明，支持 `--dry-run`。

**Step 4: Run test to verify it passes**

Run:

```bash
python3 tools/validate_task_map.py --map docs/gamepowers/index/task-doc-map.yaml
python3 tools/sync_tasks_to_bd.py --map docs/gamepowers/index/task-doc-map.yaml --dry-run
```

Expected:
- 校验脚本输出 `Validation passed`。
- 同步脚本输出待创建任务及依赖，不报错。

**Step 5: Commit**

```bash
git add tools/sync_tasks_to_bd.py tools/validate_task_map.py
git commit -m "feat: add task map validation and bd sync tools"
```

### Task 6: 增加自动化测试与端到端演练

**Files:**
- Create: `tests/test_validate_task_map.py`
- Create: `tests/test_sync_tasks_to_bd.py`
- Create: `docs/gamepowers/handoffs/design-handoff-to-superpowers.md`

**Step 1: Write the failing test**

```bash
python3 -m unittest tests/test_validate_task_map.py tests/test_sync_tasks_to_bd.py -v
```

期望：失败（测试文件未创建）。

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_validate_task_map.py tests/test_sync_tasks_to_bd.py -v; echo $?`
Expected: 输出非 `0`。

**Step 3: Write minimal implementation**

- 为校验脚本和同步脚本编写单元测试。
- 产出交接文档示例，包含 `bd` 任务引用与 ECS 契约。

**Step 4: Run test to verify it passes**

Run:

```bash
python3 -m unittest tests/test_validate_task_map.py tests/test_sync_tasks_to_bd.py -v
python3 tools/validate_task_map.py --map docs/gamepowers/index/task-doc-map.yaml
python3 tools/sync_tasks_to_bd.py --map docs/gamepowers/index/task-doc-map.yaml --apply --parent-title "GamePowers 实现任务"
```

Expected:
- 单元测试通过。
- 映射校验通过。
- bd 成功创建任务并建立依赖。

**Step 5: Commit**

```bash
git add tests docs/gamepowers/handoffs/design-handoff-to-superpowers.md
git commit -m "test: cover task map tooling and add superpowers handoff sample"
```
