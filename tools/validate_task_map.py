#!/usr/bin/env python3
"""Backward-compatible wrapper for map validation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gamepowers_cli.commands.validate_cmd import main  # noqa: E402
from gamepowers_cli.core.task_map import load_map_file, validate_map  # noqa: E402

__all__ = ["load_map_file", "validate_map", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
