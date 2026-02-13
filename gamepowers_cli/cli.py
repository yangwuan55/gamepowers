"""Main CLI entrypoint for GamePowers."""

from __future__ import annotations

import argparse
import sys

from gamepowers_cli.commands import handoff_cmd, pipeline_cmd, sync_cmd, validate_cmd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gamepowers",
        description="GamePowers 工具包命令行：校验、同步、交接、一键流水线",
    )
    subparsers = parser.add_subparsers(dest="command")

    validate_cmd.register(subparsers)
    sync_cmd.register(subparsers)
    handoff_cmd.register(subparsers)
    pipeline_cmd.register(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0

    return int(handler(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
