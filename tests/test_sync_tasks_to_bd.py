import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gamepowers_cli.core.bd_sync import (  # noqa: E402
    build_operations,
    build_task_description,
    sync_to_bd,
)


class SyncTasksToBDTests(unittest.TestCase):
    def test_build_task_description_contains_fields(self) -> None:
        task = {
            "key": "GP-010",
            "title": "ECS 蓝图",
            "type": "feature",
            "priority": 1,
            "architecture": "ECS",
            "docs": ["docs/ecs/ecs-principles.md"],
            "ecs_refs": ["docs/ecs/system-schedule.md"],
            "deps": [],
            "acceptance": ["完成 ECS 设计"],
        }

        desc = build_task_description(task)
        self.assertIn("TaskKey: GP-010", desc)
        self.assertIn("Architecture: ECS", desc)
        self.assertIn("docs/ecs/ecs-principles.md", desc)
        self.assertIn("docs/ecs/system-schedule.md", desc)

    def test_build_operations_outputs_create_and_deps(self) -> None:
        tasks = [
            {
                "key": "A",
                "title": "任务A",
                "type": "task",
                "priority": 1,
                "architecture": "DESIGN",
                "docs": ["docs/a.md"],
                "ecs_refs": [],
                "deps": [],
                "acceptance": ["done"],
            },
            {
                "key": "B",
                "title": "任务B",
                "type": "task",
                "priority": 1,
                "architecture": "DESIGN",
                "docs": ["docs/b.md"],
                "ecs_refs": [],
                "deps": ["A"],
                "acceptance": ["done"],
            },
        ]

        create_ops, dep_ops = build_operations(tasks)
        self.assertEqual(len(create_ops), 2)
        self.assertEqual(len(dep_ops), 1)
        self.assertEqual(dep_ops[0], {"blocked": "B", "blocker": "A"})

    def test_sync_to_bd_dry_run_returns_mapping(self) -> None:
        data = {
            "tasks": [
                {
                    "key": "A",
                    "title": "任务A",
                    "type": "task",
                    "priority": 1,
                    "architecture": "DESIGN",
                    "docs": ["docs/a.md"],
                    "ecs_refs": [],
                    "deps": [],
                    "acceptance": ["done"],
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "bd-task-map.json"
            result = sync_to_bd(
                data=data,
                apply=False,
                parent_title="Parent",
                output_map_path=out_path,
                keep_parent_open=False,
            )
            self.assertEqual(result["parent"], "DRY-PARENT")
            self.assertEqual(result["task_key_to_bd"]["A"], "DRY-A")
            self.assertFalse(out_path.exists())


if __name__ == "__main__":
    unittest.main()
