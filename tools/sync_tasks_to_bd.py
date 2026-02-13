#!/usr/bin/env python3
"""Backward-compatible wrapper for bd sync."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gamepowers_cli.commands.sync_cmd import main  # noqa: E402
from gamepowers_cli.core.bd_sync import (  # noqa: E402
    build_operations,
    build_task_description,
    run_cmd,
    sync_to_bd,
)

__all__ = ["build_operations", "build_task_description", "run_cmd", "sync_to_bd", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
