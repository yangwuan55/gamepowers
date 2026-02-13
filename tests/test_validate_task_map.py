import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gamepowers_cli.core.task_map import validate_map  # noqa: E402


class ValidateTaskMapTests(unittest.TestCase):
    def _build_valid_data(self) -> dict:
        return {
            "version": "1.0",
            "tasks": [
                {
                    "key": "A",
                    "title": "设计任务",
                    "type": "task",
                    "priority": 1,
                    "architecture": "DESIGN",
                    "docs": ["docs/a.md"],
                    "ecs_refs": [],
                    "deps": [],
                    "acceptance": ["完成设计"],
                },
                {
                    "key": "B",
                    "title": "ECS 任务",
                    "type": "feature",
                    "priority": 1,
                    "architecture": "ECS",
                    "docs": ["docs/b.md"],
                    "ecs_refs": ["docs/ecs.md"],
                    "deps": ["A"],
                    "acceptance": ["完成 ECS 设计"],
                },
            ],
        }

    def test_valid_map_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            (repo_root / "docs").mkdir(parents=True, exist_ok=True)
            (repo_root / "docs/a.md").write_text("a", encoding="utf-8")
            (repo_root / "docs/b.md").write_text("b", encoding="utf-8")
            (repo_root / "docs/ecs.md").write_text("ecs", encoding="utf-8")

            errors = validate_map(self._build_valid_data(), repo_root)
            self.assertEqual(errors, [])

    def test_ecs_task_requires_ecs_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            (repo_root / "docs").mkdir(parents=True, exist_ok=True)
            (repo_root / "docs/a.md").write_text("a", encoding="utf-8")
            (repo_root / "docs/b.md").write_text("b", encoding="utf-8")

            data = self._build_valid_data()
            data["tasks"][1]["ecs_refs"] = []

            errors = validate_map(data, repo_root)
            self.assertTrue(any("ecs_refs" in e for e in errors))

    def test_unknown_dependency_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            (repo_root / "docs").mkdir(parents=True, exist_ok=True)
            (repo_root / "docs/a.md").write_text("a", encoding="utf-8")
            (repo_root / "docs/b.md").write_text("b", encoding="utf-8")
            (repo_root / "docs/ecs.md").write_text("ecs", encoding="utf-8")

            data = self._build_valid_data()
            data["tasks"][1]["deps"] = ["NOT-EXIST"]

            errors = validate_map(data, repo_root)
            self.assertTrue(any("不存在" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
