"""sync subcommand."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gamepowers_cli.core.bd_sync import (
    build_operations,
    build_task_description,
    run_cmd,
    sync_to_bd,
)
from gamepowers_cli.core.task_map import validate_map_file

__all__ = [
    "build_operations",
    "build_task_description",
    "run_cmd",
    "sync_to_bd",
]


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("sync", help="将任务映射同步到 bd")
    parser.add_argument("--map", default="docs/gamepowers/index/task-doc-map.yaml", help="任务映射文件路径")
    parser.add_argument("--repo-root", default=".", help="仓库根目录")
    parser.add_argument("--apply", action="store_true", help="执行写入操作（默认 dry-run）")
    parser.add_argument("--dry-run", action="store_true", help="显式声明 dry-run")
    parser.add_argument("--parent-title", default="GamePowers 设计执行任务", help="创建 bd 父任务标题")
    parser.add_argument(
        "--keep-parent-open",
        action="store_true",
        help="保持父任务为 OPEN（默认自动关闭父任务）",
    )
    parser.add_argument(
        "--output-map",
        default="docs/gamepowers/index/bd-task-map.json",
        help="写入 key->bd id 的输出路径（仅 --apply 时生效）",
    )
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    map_path = Path(args.map).resolve()
    repo_root = Path(args.repo_root).resolve()
    output_map_path = Path(args.output_map).resolve()

    if args.apply and args.dry_run:
        print("--apply 与 --dry-run 不能同时使用", file=sys.stderr)
        return 1

    if not map_path.exists():
        print(f"映射文件不存在: {map_path}", file=sys.stderr)
        return 1

    try:
        data, errors = validate_map_file(map_path, repo_root)
    except Exception as exc:
        print(f"解析映射失败: {exc}", file=sys.stderr)
        return 1

    if errors:
        print("校验失败，已阻止同步：", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    try:
        sync_to_bd(
            data=data,
            apply=args.apply,
            parent_title=args.parent_title,
            output_map_path=output_map_path,
            keep_parent_open=args.keep_parent_open,
        )
    except Exception as exc:
        print(f"同步失败: {exc}", file=sys.stderr)
        return 1

    if args.apply:
        print("Sync completed")
    else:
        print("Dry-run completed")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="将 task-doc-map 同步到 bd")
    parser.add_argument("--map", default="docs/gamepowers/index/task-doc-map.yaml")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--parent-title", default="GamePowers 设计执行任务")
    parser.add_argument("--keep-parent-open", action="store_true")
    parser.add_argument("--output-map", default="docs/gamepowers/index/bd-task-map.json")
    args = parser.parse_args(argv)
    return handle(args)
