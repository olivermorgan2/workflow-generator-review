#!/usr/bin/env python3
"""
Deterministic audit of skills/<name>/SKILL.md files.

Emits two CSVs:
  - skills-audit.csv      — one row per skill, deterministic metrics only
  - skills-sidecars.csv   — one row per sidecar file (stretch: per-file size)

All metrics are reproducible from a clean checkout. Qualitative columns
(description quality, terminology consistency) are out of scope here and
are scored separately in `skills-audit-judgment.csv`. See methodology.md.

Usage:
    python3 audit.py [SKILLS_DIR] [OUT_DIR]
Defaults:
    SKILLS_DIR = ../../skills          (relative to this script)
    OUT_DIR    = .                     (this directory)
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

CANONICAL_FRONTMATTER = {"name", "description", "disable-model-invocation", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
RESERVED_NAMES = {"anthropic", "claude"}

# Heuristic regexes
FIRST_PERSON_RE = re.compile(r"\b(I|We|Our|Us)\b")
SECOND_PERSON_RE = re.compile(r"\b(you|your)\b", re.IGNORECASE)
BACKSLASH_PATH_RE = re.compile(r"[A-Za-z0-9_.-]+\\[A-Za-z0-9_.-]+")
ADR_REF_RE = re.compile(r"ADR-\d{3}")
ISSUE_REF_RE = re.compile(r"#\d{1,4}\b")
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
TIME_SENSITIVE_RE = re.compile(
    r"\b(after|before|since|as of|deprecated\b)\b", re.IGNORECASE
)
# rough token estimate: 1 token ≈ 4 chars (English prose)
def est_tokens(s: str) -> int:
    return max(0, round(len(s) / 4))


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (frontmatter_fields, body). Naive parser — tolerates only the
    flat `key: value` shape we use across the kit."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    fm_block = text[4:end]
    body = text[end + 4 :].lstrip("\n")
    fields: dict[str, str] = {}
    for line in fm_block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        # strip inline `# comment` from value — require a space after `#` so we
        # don't eat legitimate `#N` issue references inside descriptions
        val = re.sub(r"\s+#\s+.*$", "", val).strip()
        fields[key.strip()] = val
    return fields, body


def extract_local_links(body: str) -> list[str]:
    """Return markdown link targets that look like local paths
    (not http(s)://) — used to estimate progressive-disclosure depth."""
    links = re.findall(r"\]\(([^)]+)\)", body)
    out = []
    for href in links:
        href = href.split("#", 1)[0].strip()
        if not href or href.startswith(("http://", "https://", "mailto:")):
            continue
        out.append(href)
    return out


def find_cross_skill_refs(body: str, all_skill_names: set[str]) -> list[str]:
    """Count plain-text references to other skill names. We match
    `skill-name` in backticks/slashes and bare to keep it conservative."""
    hits: set[str] = set()
    for name in all_skill_names:
        # match `name`, /name, `/name` — boundary-anchored
        if re.search(rf"[/`]{re.escape(name)}\b", body) or re.search(
            rf"\b{re.escape(name)}\b", body
        ):
            hits.add(name)
    return sorted(hits)


def audit_skill(skill_dir: Path, all_names: set[str]) -> dict[str, object]:
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    # ---- frontmatter checks ----
    name = fm.get("name", "")
    desc = fm.get("description", "")
    fm_keys = set(fm.keys())
    fm_extras = sorted(fm_keys - CANONICAL_FRONTMATTER)
    fm_missing = sorted({"name", "description"} - fm_keys)
    name_valid = bool(NAME_RE.match(name)) and name not in RESERVED_NAMES
    name_matches_dir = name == skill_dir.name

    # ---- description checks ----
    desc_chars = len(desc)
    desc_over_1024 = desc_chars > 1024
    desc_first_person = bool(FIRST_PERSON_RE.search(desc))
    desc_second_person = bool(SECOND_PERSON_RE.search(desc))
    # cheap "what+when" heuristic: presence of "use when" / "when " phrase
    desc_lower = desc.lower()
    desc_has_when_marker = any(
        marker in desc_lower for marker in ("use when", "when the user", "trigger when")
    )

    # ---- size checks ----
    body_lines = body.count("\n") + (0 if body.endswith("\n") or not body else 1)
    body_bytes = len(body.encode("utf-8"))
    body_tokens_est = est_tokens(body)
    over_500 = body_lines > 500
    over_5k_tokens = body_tokens_est > 5000

    # ---- structure ----
    h2_sections = H2_RE.findall(body)
    h2_count = len(h2_sections)

    # ---- forbidden / smelly patterns ----
    backslash_path_hits = len(BACKSLASH_PATH_RE.findall(body))
    time_sensitive_hits = len(TIME_SENSITIVE_RE.findall(body))
    body_first_person = len(FIRST_PERSON_RE.findall(body))
    body_second_person = len(SECOND_PERSON_RE.findall(body))

    # ---- references ----
    adr_refs = sorted(set(ADR_REF_RE.findall(body)))
    issue_refs = sorted(set(ISSUE_REF_RE.findall(body)))
    cross_refs = [n for n in find_cross_skill_refs(body, all_names) if n != name]

    # ---- sidecars + ref depth ----
    sidecars = sorted(
        p.name
        for p in skill_dir.iterdir()
        if p.is_file() and p.name != "SKILL.md"
    )
    sidecar_count = len(sidecars)

    local_links = extract_local_links(body)
    sidecar_links = [
        l for l in local_links if not l.startswith("../") and "/" not in l
    ]
    # depth-2 check: do sidecar files themselves link onward to other local files?
    deep_links: list[str] = []
    for side in sidecars:
        side_path = skill_dir / side
        if side_path.suffix.lower() != ".md":
            continue
        try:
            side_body = side_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for href in extract_local_links(side_body):
            if href and not href.startswith("../"):
                deep_links.append(f"{side}->{href}")

    return {
        "skill": skill_dir.name,
        # frontmatter
        "fm_name": name,
        "fm_name_valid": int(name_valid),
        "fm_name_matches_dir": int(name_matches_dir),
        "fm_extras": "|".join(fm_extras),
        "fm_missing": "|".join(fm_missing),
        # description
        "desc_chars": desc_chars,
        "desc_over_1024": int(desc_over_1024),
        "desc_first_person": int(desc_first_person),
        "desc_second_person": int(desc_second_person),
        "desc_has_when_marker": int(desc_has_when_marker),
        # size
        "body_lines": body_lines,
        "body_bytes": body_bytes,
        "body_tokens_est": body_tokens_est,
        "over_500_lines": int(over_500),
        "over_5k_tokens_est": int(over_5k_tokens),
        # structure
        "h2_count": h2_count,
        "h2_sections": "|".join(h2_sections),
        # smells
        "backslash_path_hits": backslash_path_hits,
        "time_sensitive_hits": time_sensitive_hits,
        "body_first_person_hits": body_first_person,
        "body_second_person_hits": body_second_person,
        # references
        "adr_refs": "|".join(adr_refs),
        "issue_refs": "|".join(issue_refs),
        "cross_skill_refs": "|".join(cross_refs),
        # sidecars
        "sidecar_count": sidecar_count,
        "sidecars": "|".join(sidecars),
        "deep_links": "|".join(deep_links),
    }


def main() -> int:
    here = Path(__file__).resolve().parent
    skills_dir = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else (here / ".." / ".." / "skills").resolve()
    )
    out_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else here

    if not skills_dir.exists():
        print(f"skills dir not found: {skills_dir}", file=sys.stderr)
        return 2

    skill_dirs = sorted(
        p for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists()
    )
    all_names = {p.name for p in skill_dirs}

    rows = [audit_skill(p, all_names) for p in skill_dirs]
    if not rows:
        print("no skills found", file=sys.stderr)
        return 1

    out_csv = out_dir / "skills-audit.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {out_csv} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
