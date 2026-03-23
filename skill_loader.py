"""
skill_loader.py — Extract SKILL.md system prompts from .skill ZIP archives.
"""

import os
import zipfile
from pathlib import Path


def _display_name(filename: str) -> str:
    """Convert filename like 'psx-earnings-analyzer.skill' to 'PSX Earnings Analyzer'."""
    stem = Path(filename).stem  # e.g. 'psx-earnings-analyzer'
    return stem.replace("-", " ").title()


def load_skills(skills_dir: str = ".") -> dict[str, str]:
    """
    Scan skills_dir for *.skill files, extract SKILL.md from each ZIP archive,
    and return {display_name: system_prompt} sorted by display name.
    """
    skills: dict[str, str] = {}
    skills_path = Path(skills_dir)

    for skill_file in sorted(skills_path.glob("*.skill")):
        try:
            with zipfile.ZipFile(skill_file, "r") as zf:
                # Find SKILL.md at root or in a subdirectory
                skill_md_name = next(
                    (n for n in zf.namelist() if n.endswith("SKILL.md")),
                    None,
                )
                if skill_md_name is None:
                    continue
                content = zf.read(skill_md_name).decode("utf-8")
                display = _display_name(skill_file.name)
                skills[display] = content
        except (zipfile.BadZipFile, KeyError, UnicodeDecodeError):
            # Skip unreadable or malformed skill files
            continue

    return dict(sorted(skills.items()))
