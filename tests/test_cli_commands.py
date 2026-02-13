import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gamepowers_cli.cli import main  # noqa: E402


class CLITest(unittest.TestCase):
    def test_validate_command_success(self) -> None:
        rc = main([
            "validate",
            "--map",
            "docs/gamepowers/index/task-doc-map.yaml",
            "--repo-root",
            str(ROOT),
        ])
        self.assertEqual(rc, 0)

    def test_pipeline_dry_run_creates_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "handoff.md"
            rc = main([
                "pipeline",
                "--map",
                "docs/gamepowers/index/task-doc-map.yaml",
                "--repo-root",
                str(ROOT),
                "--dry-run",
                "--handoff-output",
                str(output),
            ])
            self.assertEqual(rc, 0)
            self.assertTrue(output.exists())
            content = output.read_text(encoding="utf-8")
            self.assertIn("ECS 实现契约", content)


if __name__ == "__main__":
    unittest.main()
