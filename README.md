# GamePowers

GamePowers 是一个面向游戏研发的 AI 技能扩展，定位为 `superpowers` 的专业补充。

## 核心定位
- 聚焦游戏设计与规划：玩法、关卡、角色、装备、技能、物品、经济、LiveOps、埋点、反作弊。
- 统一输出可执行任务集合：人读 Markdown + 机读映射 + `bd` 执行状态。
- 技术实现阶段强制采用 `ECS` 架构。
- 实现、测试、调试阶段交给 `superpowers`。

## 仓库结构
- `skills/`：GamePowers 中文技能库。
- `docs/gamepowers/`：设计文档树、任务清单、映射、交接文档。
- `docs/gamepowers/index/skill-governance.md`：skill 协作治理规范（门禁、仲裁、发布前检查）。
- `docs/gamepowers/index/skill-doc-ownership.yaml`：单一主写归属与审查关系。
- `gamepowers_cli/`：可安装 CLI 包（`gamepowers` 命令）。
- `tools/`：兼容脚本入口（内部转调 `gamepowers_cli`）。
- `tests/`：脚本单元测试。
- `superpowers-ref/`：用于分析的上游 superpowers 仓库副本。

## 使用流程
1. 使用 `game-design-orchestrator` 明确需求并路由领域技能。
2. 产出文档树与任务映射（`task-doc-map.yaml`）。
3. 运行 `gamepowers validate` 确保映射与 ECS 合规。
4. 运行 `gamepowers sync` 将任务写入 `bd`，形成可执行依赖图。
5. 运行 `gamepowers handoff` 生成交接包。
6. 通过 `design-handoff-to-superpowers` 交接给 superpowers 进入实现。

## 安装
### 安装（推荐）
`Fetch and follow instructions from https://raw.githubusercontent.com/yangwuan55/gamepowers/refs/heads/main/.codex/INSTALL.md`  

该脚本会自动完成：
- 安装或更新 `beads`（`bd` 命令）。
- 安装或更新 `superpowers` 到 `~/.codex/superpowers`。
- 建立 `~/.agents/skills/superpowers -> ~/.codex/superpowers/skills` 软链。
- 建立 `~/.agents/skills/gamepowers -> <当前仓库>/skills` 软链。
- 安装当前 `gamepowers`（`pip install -e .`）。
- 当前仓库未初始化时自动执行 `bd init`。

说明：即使 `pip install -e .` 在系统 Python 下受限（如 PEP 668），脚本也会先完成 skills 软链，因此 GamePowers 仍可在 Codex 中被发现。

安装后请重启 Codex 以确保 `superpowers` skills 被发现。

可选参数：
```bash
./tools/install_all.sh --dry-run
./tools/install_all.sh --skip-bd-init
```

### 分步安装（手动）
```bash
cd /Users/ymr/github/gamepowers
pip install -e .
```

安装后可直接使用 `gamepowers` 命令。

## CLI 常用命令
```bash
cd /Users/ymr/github/gamepowers
gamepowers --help
gamepowers validate --map docs/gamepowers/index/task-doc-map.yaml --repo-root /Users/ymr/github/gamepowers
gamepowers sync --map docs/gamepowers/index/task-doc-map.yaml --dry-run
gamepowers handoff --map docs/gamepowers/index/task-doc-map.yaml --output docs/gamepowers/handoffs/generated-handoff.md
gamepowers pipeline --map docs/gamepowers/index/task-doc-map.yaml --dry-run --handoff-output docs/gamepowers/handoffs/generated-handoff.md
```

## 兼容脚本命令
```bash
python3 tools/validate_task_map.py --map docs/gamepowers/index/task-doc-map.yaml
python3 tools/validate_skills_contract.py --repo-root /Users/ymr/github/gamepowers
python3 tools/sync_tasks_to_bd.py --map docs/gamepowers/index/task-doc-map.yaml --dry-run
python3 tools/sync_tasks_to_bd.py --map docs/gamepowers/index/task-doc-map.yaml --apply --parent-title "GamePowers 实施任务"
python3 -m unittest tests/test_validate_task_map.py tests/test_sync_tasks_to_bd.py tests/test_cli_commands.py tests/test_validate_skills_contract.py -v
```

说明：同步脚本在 `--apply` 时默认会自动关闭父 Epic，避免 `bd` 将父任务视为阻塞项导致子任务不可执行。若希望保留父 Epic 为 OPEN，可加 `--keep-parent-open`。
