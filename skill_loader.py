"""
skill_loader.py — Extract SKILL.md + reference docs from .skill ZIP archives.
"""

import zipfile
from pathlib import Path


def _display_name(filename: str) -> str:
    """Convert 'psx-earnings-analyzer.skill' → 'PSX Earnings Analyzer'."""
    return Path(filename).stem.replace("-", " ").title()


def _extract_skill(skill_path: Path) -> dict:
    """
    Open a .skill ZIP in memory, read SKILL.md and all reference/*.md files.

    Returns a dict with:
        display_name    : str — human-readable name
        system_prompt   : str — SKILL.md + all reference docs concatenated
        reference_files : list[str] — reference filenames found
        total_chars     : int
    """
    with zipfile.ZipFile(skill_path, "r") as zf:
        names = zf.namelist()

        # Find SKILL.md (may be at root or inside a subdirectory)
        skill_md_name = next((n for n in names if n.endswith("SKILL.md")), None)
        if skill_md_name is None:
            raise KeyError(f"No SKILL.md found in {skill_path.name}")

        skill_md = zf.read(skill_md_name).decode("utf-8")

        # Collect all reference docs (references/*.md)
        ref_names = sorted(
            n for n in names
            if "/references/" in n and n.endswith(".md")
        )
        ref_blocks: list[str] = []
        for ref_name in ref_names:
            ref_content = zf.read(ref_name).decode("utf-8")
            ref_filename = Path(ref_name).name
            ref_blocks.append(f"## Reference: {ref_filename}\n\n{ref_content}")

        # Build full system prompt
        if ref_blocks:
            system_prompt = skill_md + "\n\n---\n\n" + "\n\n---\n\n".join(ref_blocks)
        else:
            system_prompt = skill_md

    return {
        "display_name": _display_name(skill_path.name),
        "system_prompt": system_prompt,
        "system_prompt_skill_only": skill_md,
        "reference_files": [Path(n).name for n in ref_names],
        "total_chars": len(system_prompt),
    }


def load_skills(skills_dir: str = ".") -> dict[str, dict]:
    """
    Scan skills_dir for *.skill files and return a sorted skill registry.

    Returns:
        {display_name: skill_info_dict}  — sorted alphabetically by display_name

    Never raises — corrupt/missing files are skipped silently.
    """
    skills: dict[str, dict] = {}
    for skill_file in sorted(Path(skills_dir).glob("*.skill")):
        try:
            info = _extract_skill(skill_file)
            skills[info["display_name"]] = info
        except (zipfile.BadZipFile, KeyError, UnicodeDecodeError):
            continue

    return dict(sorted(skills.items()))
