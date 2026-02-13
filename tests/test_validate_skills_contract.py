import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.validate_skills_contract import (  # noqa: E402
    EXPECTED_SKILL_LAYERS,
    validate_skills_contract,
)


class ValidateSkillsContractTests(unittest.TestCase):
    def test_repo_skills_contract_passes(self) -> None:
        errors = validate_skills_contract(ROOT / "skills")
        self.assertEqual(errors, [])

    def test_detects_missing_heading_and_bad_description(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skills_root = Path(tmp) / "skills"
            skill_path = skills_root / "demo-skill" / "SKILL.md"
            skill_path.parent.mkdir(parents=True, exist_ok=True)
            skill_path.write_text(
                "\n".join(
                    [
                        "---",
                        "name: demo-skill",
                        "description: 需要测试",
                        "---",
                        "",
                        "# Demo",
                        "## 适用条件",
                    ]
                ),
                encoding="utf-8",
            )

            errors = validate_skills_contract(
                skills_root,
                expected_skill_layers={"demo-skill": "domain"},
            )
            self.assertTrue(any("Use when" in e for e in errors))
            self.assertTrue(any("缺少章节 ## 输入契约" in e for e in errors))

    def test_expected_skill_count_is_14(self) -> None:
        self.assertEqual(len(EXPECTED_SKILL_LAYERS), 14)


if __name__ == "__main__":
    unittest.main()
