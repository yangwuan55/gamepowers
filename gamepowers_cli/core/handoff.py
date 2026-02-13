"""Generate handoff markdown from task map and bd mapping."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_bd_map(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def generate_handoff_markdown(
    map_data: dict[str, Any],
    bd_map_data: dict[str, Any],
    map_path: Path,
) -> str:
    tasks = map_data.get("tasks", [])
    key_to_bd = bd_map_data.get("task_key_to_bd", {}) if isinstance(bd_map_data, dict) else {}

    lines: list[str] = []
    lines.append("# GamePowers 自动交接包")
    lines.append("")
    lines.append(f"生成时间: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append("## 输入来源")
    lines.append(f"- 任务映射: `{map_path}`")
    lines.append("- 任务清单: `docs/gamepowers/tasks/executable-task-list.md`")
    lines.append("- 执行状态: `bd` 任务图")
    lines.append("")
    lines.append("## 任务与文档关联")
    lines.append("| TaskKey | bd ID | 架构 | 文档 |")
    lines.append("|---|---|---|---|")

    for task in tasks:
        if not isinstance(task, dict):
            continue
        key = str(task.get("key", ""))
        bd_id = key_to_bd.get(key, "N/A")
        arch = str(task.get("architecture", ""))
        docs = task.get("docs", [])
        doc_text = ", ".join(f"`{doc}`" for doc in docs if isinstance(doc, str))
        lines.append(f"| {key} | {bd_id} | {arch} | {doc_text} |")

    lines.append("")
    lines.append("## ECS 实现契约")
    lines.append("- 技术任务必须使用 `ECS` 架构。")
    lines.append("- 必须遵守系统调度顺序和事件流文档。")
    lines.append("- 关键参考文档:")
    lines.append("  - `docs/gamepowers/ecs/system-schedule.md`")
    lines.append("  - `docs/gamepowers/ecs/event-flow.md`")
    lines.append("  - `docs/gamepowers/ecs/performance-budget.md`")
    lines.append("")
    lines.append("## 进入 superpowers")
    lines.append("1. 调用 `superpowers:writing-plans`。")
    lines.append("2. 按 `superpowers:test-driven-development` 实施。")
    lines.append("3. 出现问题时使用 `superpowers:systematic-debugging`。")

    return "\n".join(lines) + "\n"


def write_handoff(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
