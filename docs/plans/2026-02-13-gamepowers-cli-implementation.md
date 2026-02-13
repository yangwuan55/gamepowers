# GamePowers CLI Tooling Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将现有 GamePowers 脚本升级为可安装命令 `gamepowers`，并提供完整的 `validate/sync/handoff/pipeline` 子命令。

**Architecture:** 采用“核心模块 + 命令适配层 + 兼容脚本”结构。核心模块承载校验、同步、交接逻辑；命令层使用 argparse 解析子命令；原有 `tools/` 脚本作为兼容入口转调核心模块，避免双份逻辑。

**Tech Stack:** Python 3、argparse、setuptools(pyproject)、unittest、bd CLI

---

### Task 1: 建立可安装包与命令入口

**Files:**
- Create: `pyproject.toml`
- Create: `gamepowers_cli/__init__.py`
- Create: `gamepowers_cli/cli.py`

**Step 1: Write the failing test**

```bash
cd /Users/ymr/github/gamepowers && test -f pyproject.toml && test -f gamepowers_cli/cli.py
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/ymr/github/gamepowers && test -f pyproject.toml && test -f gamepowers_cli/cli.py; echo $?`
Expected: `1`

**Step 3: Write minimal implementation**

- 创建 `pyproject.toml` 并配置 `project.scripts`。
- 创建 `gamepowers_cli.cli:main` 与基础 argparse 结构。

**Step 4: Run test to verify it passes**

Run: `cd /Users/ymr/github/gamepowers && test -f pyproject.toml && test -f gamepowers_cli/cli.py; echo $?`
Expected: `0`

**Step 5: Commit**

```bash
cd /Users/ymr/github/gamepowers
git add pyproject.toml gamepowers_cli/__init__.py gamepowers_cli/cli.py
git commit -m "feat: bootstrap installable gamepowers cli package"
```

### Task 2: 迁移映射校验核心逻辑

**Files:**
- Create: `gamepowers_cli/core/task_map.py`
- Create: `gamepowers_cli/commands/validate_cmd.py`
- Modify: `tools/validate_task_map.py`
- Test: `tests/test_validate_task_map.py`

**Step 1: Write the failing test**

```bash
cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_validate_task_map.py -v
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_validate_task_map.py -v`
Expected: FAIL（迁移阶段导入路径暂未适配）

**Step 3: Write minimal implementation**

- 将 `load_map_file/validate_map` 迁移到 `gamepowers_cli.core.task_map`。
- `validate` 子命令调用核心逻辑。
- `tools/validate_task_map.py` 变为兼容包装器。

**Step 4: Run test to verify it passes**

Run: `cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_validate_task_map.py -v`
Expected: PASS

**Step 5: Commit**

```bash
cd /Users/ymr/github/gamepowers
git add gamepowers_cli/core/task_map.py gamepowers_cli/commands/validate_cmd.py tools/validate_task_map.py tests/test_validate_task_map.py
git commit -m "refactor: move map validation into cli core module"
```

### Task 3: 迁移 bd 同步核心逻辑

**Files:**
- Create: `gamepowers_cli/core/bd_sync.py`
- Create: `gamepowers_cli/commands/sync_cmd.py`
- Modify: `tools/sync_tasks_to_bd.py`
- Test: `tests/test_sync_tasks_to_bd.py`

**Step 1: Write the failing test**

```bash
cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_sync_tasks_to_bd.py -v
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_sync_tasks_to_bd.py -v`
Expected: FAIL（迁移阶段导入路径暂未适配）

**Step 3: Write minimal implementation**

- 迁移 `build_task_description/build_operations/sync_to_bd` 至核心层。
- `sync` 子命令调用核心逻辑。
- 保留 `--apply/--dry-run/--keep-parent-open` 语义。

**Step 4: Run test to verify it passes**

Run: `cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_sync_tasks_to_bd.py -v`
Expected: PASS

**Step 5: Commit**

```bash
cd /Users/ymr/github/gamepowers
git add gamepowers_cli/core/bd_sync.py gamepowers_cli/commands/sync_cmd.py tools/sync_tasks_to_bd.py tests/test_sync_tasks_to_bd.py
git commit -m "refactor: move bd sync logic into cli core module"
```

### Task 4: 实现 handoff 与 pipeline 命令

**Files:**
- Create: `gamepowers_cli/core/handoff.py`
- Create: `gamepowers_cli/commands/handoff_cmd.py`
- Create: `gamepowers_cli/commands/pipeline_cmd.py`
- Create: `tests/test_cli_commands.py`

**Step 1: Write the failing test**

```bash
cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_cli_commands.py -v
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_cli_commands.py -v; echo $?`
Expected: 非 `0`（测试文件或命令未实现）

**Step 3: Write minimal implementation**

- `handoff`：生成交接摘要文件。
- `pipeline`：串联 `validate -> sync -> handoff`。

**Step 4: Run test to verify it passes**

Run: `cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_cli_commands.py -v`
Expected: PASS

**Step 5: Commit**

```bash
cd /Users/ymr/github/gamepowers
git add gamepowers_cli/core/handoff.py gamepowers_cli/commands/handoff_cmd.py gamepowers_cli/commands/pipeline_cmd.py tests/test_cli_commands.py
git commit -m "feat: add handoff and pipeline subcommands"
```

### Task 5: 完成安装与端到端验证

**Files:**
- Modify: `README.md`
- Modify: `docs/plans/2026-02-13-gamepowers-cli-design.md`

**Step 1: Write the failing test**

```bash
cd /Users/ymr/github/gamepowers && gamepowers --help
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/ymr/github/gamepowers && gamepowers --help; echo $?`
Expected: 非 `0`（安装前）

**Step 3: Write minimal implementation**

- `pip install -e .`
- 更新 README 安装和使用文档。

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Users/ymr/github/gamepowers && pip install -e .
cd /Users/ymr/github/gamepowers && gamepowers --help
cd /Users/ymr/github/gamepowers && gamepowers validate --map docs/gamepowers/index/task-doc-map.yaml
cd /Users/ymr/github/gamepowers && gamepowers pipeline --map docs/gamepowers/index/task-doc-map.yaml --dry-run --handoff-output docs/gamepowers/handoffs/generated-handoff.md
cd /Users/ymr/github/gamepowers && python3 -m unittest tests/test_validate_task_map.py tests/test_sync_tasks_to_bd.py tests/test_cli_commands.py -v
```

Expected: 全部成功。

**Step 5: Commit**

```bash
cd /Users/ymr/github/gamepowers
git add README.md docs/plans/2026-02-13-gamepowers-cli-design.md
git commit -m "docs: add install and usage guide for gamepowers cli"
```
