"""handoff subcommand."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gamepowers_cli.core.handoff import generate_handoff_markdown, load_bd_map, write_handoff
from gamepowers_cli.core.task_map import load_map_file, validate_map


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("handoff", help="生成交接文档")
    parser.add_argument("--map", default="docs/gamepowers/index/task-doc-map.yaml", help="任务映射文件路径")
    parser.add_argument("--repo-root", default=".", help="仓库根目录")
    parser.add_argument("--bd-map", default="docs/gamepowers/index/bd-task-map.json", help="bd 映射文件路径")
    parser.add_argument(
        "--output",
        default="docs/gamepowers/handoffs/generated-handoff.md",
        help="输出交接文档路径",
    )
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    map_path = Path(args.map).resolve()
    repo_root = Path(args.repo_root).resolve()
    bd_map_path = Path(args.bd_map).resolve()
    output_path = Path(args.output).resolve()

    if not map_path.exists():
        print(f"映射文件不存在: {map_path}", file=sys.stderr)
        return 1

    try:
        map_data = load_map_file(map_path)
    except Exception as exc:
        print(f"映射解析失败: {exc}", file=sys.stderr)
        return 1

    errors = validate_map(map_data, repo_root)
    if errors:
        print("校验失败，已阻止生成交接文档：", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    try:
        bd_map_data = load_bd_map(bd_map_path)
        content = generate_handoff_markdown(map_data, bd_map_data, map_path)
        write_handoff(output_path, content)
    except Exception as exc:
        print(f"交接文档生成失败: {exc}", file=sys.stderr)
        return 1

    print(f"Handoff written: {output_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="生成交接文档")
    parser.add_argument("--map", default="docs/gamepowers/index/task-doc-map.yaml")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--bd-map", default="docs/gamepowers/index/bd-task-map.json")
    parser.add_argument("--output", default="docs/gamepowers/handoffs/generated-handoff.md")
    args = parser.parse_args(argv)
    return handle(args)
