"""Task map loading and validation logic."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

REQUIRED_TASK_FIELDS = {
    "key",
    "title",
    "type",
    "priority",
    "architecture",
    "docs",
    "ecs_refs",
    "deps",
    "acceptance",
}
VALID_TYPES = {"bug", "feature", "task", "epic", "chore"}


def load_map_file(map_path: Path) -> dict[str, Any]:
    text = map_path.read_text(encoding="utf-8")

    if yaml is not None:
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "无法解析映射文件。请安装 PyYAML，或使用 JSON 兼容的 YAML 内容。"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError("映射文件根节点必须是对象。")

    return data


def _resolve_path(repo_root: Path, path_value: str) -> Path:
    path_obj = Path(path_value)
    if path_obj.is_absolute():
        return path_obj
    return repo_root / path_obj


def validate_map(data: dict[str, Any], repo_root: Path) -> list[str]:
    errors: list[str] = []

    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return ["tasks 必须是非空数组。"]

    key_set: set[str] = set()
    for index, task in enumerate(tasks):
        label = f"tasks[{index}]"
        if not isinstance(task, dict):
            errors.append(f"{label} 必须是对象。")
            continue

        missing = REQUIRED_TASK_FIELDS - set(task.keys())
        if missing:
            errors.append(f"{label} 缺少字段: {sorted(missing)}")

        key = task.get("key")
        if not isinstance(key, str) or not key.strip():
            errors.append(f"{label}.key 必须是非空字符串。")
        elif key in key_set:
            errors.append(f"发现重复 task key: {key}")
        else:
            key_set.add(key)

        task_type = task.get("type")
        if task_type not in VALID_TYPES:
            errors.append(f"{label}.type 非法: {task_type}，允许值: {sorted(VALID_TYPES)}")

        priority = task.get("priority")
        if not isinstance(priority, int) or priority < 0 or priority > 4:
            errors.append(f"{label}.priority 必须是 0-4 的整数。")

        architecture = task.get("architecture")
        if not isinstance(architecture, str) or not architecture.strip():
            errors.append(f"{label}.architecture 必须是非空字符串。")

        docs = task.get("docs")
        if not isinstance(docs, list) or not docs:
            errors.append(f"{label}.docs 必须是非空数组。")
        else:
            for doc in docs:
                if not isinstance(doc, str) or not doc.strip():
                    errors.append(f"{label}.docs 包含非法路径: {doc}")
                    continue
                resolved = _resolve_path(repo_root, doc)
                if not resolved.exists():
                    errors.append(f"{label}.docs 路径不存在: {doc}")

        deps = task.get("deps")
        if not isinstance(deps, list):
            errors.append(f"{label}.deps 必须是数组。")
        else:
            for dep in deps:
                if not isinstance(dep, str) or not dep.strip():
                    errors.append(f"{label}.deps 包含非法依赖 key: {dep}")

        acceptance = task.get("acceptance")
        if not isinstance(acceptance, list) or not acceptance:
            errors.append(f"{label}.acceptance 必须是非空数组。")
        else:
            for rule in acceptance:
                if not isinstance(rule, str) or not rule.strip():
                    errors.append(f"{label}.acceptance 包含空项。")

        ecs_refs = task.get("ecs_refs")
        if not isinstance(ecs_refs, list):
            errors.append(f"{label}.ecs_refs 必须是数组。")
            ecs_refs = []

        arch_value = str(architecture).strip().upper() if architecture is not None else ""
        if arch_value == "ECS":
            if not ecs_refs:
                errors.append(f"{label} 是 ECS 任务，但 ecs_refs 为空。")
            for ref in ecs_refs:
                if not isinstance(ref, str) or not ref.strip():
                    errors.append(f"{label}.ecs_refs 包含非法路径: {ref}")
                    continue
                resolved = _resolve_path(repo_root, ref)
                if not resolved.exists():
                    errors.append(f"{label}.ecs_refs 路径不存在: {ref}")

    key_index = {
        task["key"]
        for task in tasks
        if isinstance(task, dict) and isinstance(task.get("key"), str)
    }
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            continue
        deps = task.get("deps")
        if not isinstance(deps, list):
            continue
        for dep in deps:
            if isinstance(dep, str) and dep not in key_index:
                errors.append(f"tasks[{index}].deps 引用了不存在的 key: {dep}")

    return errors


def validate_map_file(map_path: Path, repo_root: Path) -> tuple[dict[str, Any], list[str]]:
    data = load_map_file(map_path)
    errors = validate_map(data, repo_root)
    return data, errors
