#!/usr/bin/env python3
"""Validate strict contract for GamePowers skill docs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

EXPECTED_SKILL_LAYERS: dict[str, str] = {
    "game-design-orchestrator": "orchestrator",
    "design-handoff-to-superpowers": "orchestrator",
    "ecs-architecture-designer": "architecture",
    "game-vision-alignment": "domain",
    "core-loop-architect": "domain",
    "mechanic-spec-writer": "domain",
    "combat-and-roles-designer": "domain",
    "progression-structure-designer": "domain",
    "economy-model-designer": "domain",
    "balance-framework": "domain",
    "content-pipeline-planner": "domain",
    "liveops-event-designer": "domain",
    "telemetry-kpi-designer": "domain",
    "anti-cheat-and-exploit-review": "domain",
}

REQUIRED_HEADINGS: dict[str, list[str]] = {
    "orchestrator": [
        "## 适用条件",
        "## 阶段状态机",
        "## 输入契约",
        "## 路由规则",
        "## 阶段门禁",
        "## 文档索引更新规则",
        "## bd 同步规则",
        "## 冲突仲裁与升级",
        "## 反模式（禁止）",
        "## 完成判定",
    ],
    "architecture": [
        "## 适用条件",
        "## 输入契约",
        "## ECS 设计流程",
        "## 强制校验清单",
        "## 输出模板",
        "## 禁止项（反模式）",
        "## 验证与回滚",
        "## 与协调层联动",
        "## 完成判定",
    ],
    "domain": [
        "## 适用条件",
        "## 输入契约",
        "## 设计步骤",
        "## 输出工件",
        "## 质量门禁",
        "## 风险与缓解",
        "## 与 ECS/协调层联动",
        "## 反模式（禁止）",
        "## 完成判定",
    ],
}


def extract_frontmatter_description(content: str) -> str | None:
    lines = content.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return None

    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if stripped.startswith("description:"):
            return stripped.split(":", 1)[1].strip()
    return None


def validate_skill_file(skill_name: str, layer: str, file_path: Path) -> list[str]:
    errors: list[str] = []
    if not file_path.exists():
        return [f"{skill_name}: 缺少文件 {file_path}"]

    content = file_path.read_text(encoding="utf-8")
    description = extract_frontmatter_description(content)
    if description is None:
        errors.append(f"{skill_name}: 缺少 frontmatter description")
    elif not description.startswith("Use when"):
        errors.append(f"{skill_name}: description 必须以 'Use when' 开头")

    for heading in REQUIRED_HEADINGS[layer]:
        if heading not in content:
            errors.append(f"{skill_name}: 缺少章节 {heading}")

    return errors


def validate_skills_contract(
    skills_root: Path,
    expected_skill_layers: dict[str, str] | None = None,
) -> list[str]:
    expected_skill_layers = expected_skill_layers or EXPECTED_SKILL_LAYERS

    errors: list[str] = []
    for skill_name, layer in expected_skill_layers.items():
        if layer not in REQUIRED_HEADINGS:
            errors.append(f"{skill_name}: 未知层级 {layer}")
            continue

        skill_path = skills_root / skill_name / "SKILL.md"
        errors.extend(validate_skill_file(skill_name, layer, skill_path))

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验 GamePowers skills 契约完整性")
    parser.add_argument("--repo-root", default=".", help="仓库根目录")
    parser.add_argument("--skills-dir", default="skills", help="skills 目录路径（相对 repo-root）")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    skills_root = (repo_root / args.skills_dir).resolve()

    if not skills_root.exists():
        print(f"skills 目录不存在: {skills_root}", file=sys.stderr)
        return 1

    errors = validate_skills_contract(skills_root)
    if errors:
        print("Skill contract validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Skill contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
