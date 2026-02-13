"""Sync task map data into bd issues."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Callable

CommandRunner = Callable[[list[str], bool], str]


def build_task_description(task: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"TaskKey: {task['key']}")
    lines.append(f"Architecture: {task['architecture']}")
    lines.append("Docs:")
    for doc in task.get("docs", []):
        lines.append(f"- {doc}")

    ecs_refs = task.get("ecs_refs", [])
    if ecs_refs:
        lines.append("ECS References:")
        for ref in ecs_refs:
            lines.append(f"- {ref}")

    lines.append("Acceptance:")
    for item in task.get("acceptance", []):
        lines.append(f"- {item}")

    return "\n".join(lines)


def build_operations(tasks: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    create_ops: list[dict[str, Any]] = []
    dep_ops: list[dict[str, Any]] = []

    for task in tasks:
        create_ops.append(
            {
                "key": task["key"],
                "title": task["title"],
                "type": task["type"],
                "priority": task["priority"],
                "description": build_task_description(task),
            }
        )
        for dep in task.get("deps", []):
            dep_ops.append({"blocked": task["key"], "blocker": dep})

    return create_ops, dep_ops


def run_cmd(args: list[str], apply: bool) -> str:
    if not apply:
        print(f"DRY-RUN: {' '.join(args)}")
        return ""

    proc = subprocess.run(args, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"命令执行失败: {' '.join(args)}\nstdout: {proc.stdout}\nstderr: {proc.stderr}"
        )
    return proc.stdout.strip()


def sync_to_bd(
    data: dict[str, Any],
    apply: bool,
    parent_title: str,
    output_map_path: Path,
    keep_parent_open: bool,
    command_runner: CommandRunner = run_cmd,
) -> dict[str, Any]:
    tasks = data["tasks"]
    create_ops, dep_ops = build_operations(tasks)

    key_to_bd: dict[str, str] = {}
    parent_id = ""

    if parent_title:
        parent_cmd = ["bd", "create", parent_title, "--type", "epic", "--priority", "1", "--silent"]
        parent_output = command_runner(parent_cmd, apply)
        parent_id = parent_output if apply else "DRY-PARENT"
        if apply:
            print(f"Created parent issue: {parent_id}")

    for op in create_ops:
        cmd = [
            "bd",
            "create",
            op["title"],
            "--type",
            str(op["type"]),
            "--priority",
            str(op["priority"]),
            "--description",
            str(op["description"]),
            "--silent",
        ]
        if parent_id:
            cmd.extend(["--parent", parent_id])

        output = command_runner(cmd, apply)
        key_to_bd[op["key"]] = output if apply else f"DRY-{op['key']}"
        print(f"Task {op['key']} -> {key_to_bd[op['key']]}")

    for dep in dep_ops:
        blocked_id = key_to_bd[dep["blocked"]]
        blocker_id = key_to_bd[dep["blocker"]]
        dep_cmd = ["bd", "dep", "add", blocked_id, blocker_id]
        command_runner(dep_cmd, apply)
        print(f"Dependency {blocked_id} depends on {blocker_id}")

    if parent_id and not keep_parent_open:
        close_cmd = ["bd", "close", parent_id]
        command_runner(close_cmd, apply)
        print(f"Parent closed to avoid blocking children: {parent_id}")

    result = {
        "parent": parent_id,
        "task_key_to_bd": key_to_bd,
        "dependencies": dep_ops,
    }

    if apply:
        output_map_path.parent.mkdir(parents=True, exist_ok=True)
        output_map_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Wrote bd mapping: {output_map_path}")

    return result
