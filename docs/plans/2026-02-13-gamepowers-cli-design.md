# GamePowers CLI 工具包设计

## 1. 目标
把现有分散脚本能力产品化为可安装命令 `gamepowers`，支持：
- 任务映射校验
- `bd` 任务同步
- 交接文档生成
- 一键流水线执行（校验 -> 同步 -> 交接）

## 2. 约束
- 中文提示与中文错误信息优先。
- 技术任务必须满足 ECS 约束。
- 保持现有 `tools/*.py` 兼容入口。
- `bd` 为任务执行状态源。

## 3. 命令设计
- `gamepowers validate --map <path> [--repo-root <path>]`
- `gamepowers sync --map <path> [--apply] [--dry-run] [--parent-title <title>] [--keep-parent-open] [--output-map <path>]`
- `gamepowers handoff --map <path> [--bd-map <path>] [--output <path>]`
- `gamepowers pipeline --map <path> [--apply] [--parent-title <title>] [--keep-parent-open] [--output-map <path>] [--handoff-output <path>]`

## 4. 代码结构
- `gamepowers_cli/cli.py`：argparse 主入口。
- `gamepowers_cli/core/task_map.py`：映射读取与校验。
- `gamepowers_cli/core/bd_sync.py`：映射到 bd 同步。
- `gamepowers_cli/core/handoff.py`：交接文档生成。
- `gamepowers_cli/commands/*`：子命令封装。

## 5. 打包方案
采用 `pyproject.toml + setuptools`，通过 `project.scripts` 暴露命令：
- `gamepowers = gamepowers_cli.cli:main`

## 6. 兼容策略
- `tools/validate_task_map.py` 改为轻薄兼容层，复用 `gamepowers_cli.core.task_map`。
- `tools/sync_tasks_to_bd.py` 改为兼容层，复用 `gamepowers_cli.core.bd_sync`。

## 7. 验收标准
- `pip install -e .` 后 `gamepowers --help` 可用。
- `gamepowers validate` 与旧脚本校验结果一致。
- `gamepowers sync` 能创建 `bd` 任务并维护依赖关系。
- `gamepowers handoff` 产出包含任务、文档、bd ID、ECS 契约。
- `gamepowers pipeline` 一次完成全流程。
