"""validate subcommand."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gamepowers_cli.core.task_map import validate_map_file


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("validate", help="校验任务映射文件")
    parser.add_argument("--map", default="docs/gamepowers/index/task-doc-map.yaml", help="任务映射文件路径")
    parser.add_argument("--repo-root", default=".", help="仓库根目录")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    map_path = Path(args.map).resolve()
    repo_root = Path(args.repo_root).resolve()

    if not map_path.exists():
        print(f"映射文件不存在: {map_path}", file=sys.stderr)
        return 1

    try:
        _, errors = validate_map_file(map_path, repo_root)
    except Exception as exc:
        print(f"解析失败: {exc}", file=sys.stderr)
        return 1

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="校验 GamePowers 的任务映射文件")
    parser.add_argument("--map", default="docs/gamepowers/index/task-doc-map.yaml")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args(argv)
    return handle(args)
