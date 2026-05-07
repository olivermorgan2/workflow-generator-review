#!/usr/bin/env python3
"""
Type-3 ADR attribution audit for SKILL.md files.

Per `notes/refactoring-ideas.md` entry #2, the goal is to find
attribution-style ADR references — "(ADR-014)", "per ADR-038",
"implements ADR-035" — that obscure the user-facing description
without adding load-bearing schema information.

Cannot perfectly distinguish:
  - type-1 (canonical anchor — keep)
  - type-2 (load-bearing schema — keep, e.g. "the ADR-040 carry-forward")
  - type-3 (informational attribution — prune)

So we output:
  - HIGH-CONFIDENCE type-3 patterns (parenthetical, "per ADR", "implements ADR")
  - MEDIUM-CONFIDENCE type-3 candidates ("see ADR", "ADR-NNN is explicit")
  - Per-skill summary with density
  - Per-match listing with line:context for manual verification

Outputs:
  adr-attributions.md — readable report
  adr-attributions.csv — per-skill counts for joining to skills-audit.csv

Usage:
    python3 adr-audit.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = (HERE / ".." / ".." / "skills").resolve()

# Strip markdown link syntax `[ADR-NNN](url)` to bare `ADR-NNN` for matching
MD_LINK_RE = re.compile(r"\[(ADR-\d{3})\]\([^)]+\)")

# HIGH-CONFIDENCE type-3 patterns
HIGH_PATTERNS: dict[str, re.Pattern[str]] = {
    "parenthetical": re.compile(r"\(ADR-\d{3}(?:\s*[,;]\s*ADR-\d{3})*\)"),
    "per_ADR_paren": re.compile(r"\(per\s+ADR-\d{3}[^)]*\)"),
    "per_ADR": re.compile(r"\bper\s+ADR-\d{3}\b(?=[\s.,;:)])"),
    "implements": re.compile(r"\bimplement(?:s|ing|ed)?\s+ADR-\d{3}\b"),
    "following": re.compile(r"\bfollow(?:s|ing|ed)?\s+ADR-\d{3}\b"),
    "in_line_with": re.compile(r"\bin\s+line\s+with\s+ADR-\d{3}\b"),
    "consistent_with": re.compile(r"\bconsistent\s+with\s+ADR-\d{3}\b"),
    "as_per": re.compile(r"\bas\s+per\s+ADR-\d{3}\b"),
}

# MEDIUM-CONFIDENCE — could be type-1/2 or type-3 depending on context
MED_PATTERNS: dict[str, re.Pattern[str]] = {
    "see_ADR": re.compile(r"\bsee\s+ADR-\d{3}\b"),
    "ADR_is_explicit": re.compile(r"\bADR-\d{3}\s+is\s+explicit\b"),
    "ADR_says": re.compile(r"\bADR-\d{3}\s+(?:says|states)\b"),
}


def parse_frontmatter_offset(text: str) -> int:
    """Return character offset where body starts (after closing ---)."""
    if not text.startswith("---\n"):
        return 0
    end = text.find("\n---", 4)
    return end + 4 if end != -1 else 0


def _line_kinds(text: str) -> list[str]:
    """Classify each line of `text` so we can skip matches inside code
    fences, indented code blocks, and markdown table rows. Returns one
    label per line: 'prose', 'code', 'table', or 'blank'."""
    kinds: list[str] = []
    in_fence = False
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            kinds.append("code")
            continue
        if in_fence:
            kinds.append("code")
            continue
        if not stripped:
            kinds.append("blank")
            continue
        # indented code block (4+ spaces or tab at start, with content)
        if (raw.startswith("    ") or raw.startswith("\t")) and stripped:
            kinds.append("code")
            continue
        # markdown table row: starts with |
        if stripped.startswith("|"):
            kinds.append("table")
            continue
        kinds.append("prose")
    return kinds


def find_matches(text: str, patterns: dict[str, re.Pattern[str]]) -> list[dict]:
    """Return list of match dicts: {pattern, match, line, context, kind}.
    Matches inside code blocks / tables are returned with kind set so
    callers can filter them out."""
    flat = MD_LINK_RE.sub(r"\1", text)
    line_starts = [0]
    for i, ch in enumerate(flat):
        if ch == "\n":
            line_starts.append(i + 1)

    line_kinds = _line_kinds(flat)

    out: list[dict] = []
    seen_spans: set[tuple[int, int]] = set()
    for label, pat in patterns.items():
        for m in pat.finditer(flat):
            span = m.span()
            if any(s <= span[0] and span[1] <= e for (s, e) in seen_spans):
                continue
            seen_spans.add(span)
            lineno = next(
                (i for i, start in enumerate(line_starts) if start > span[0]),
                len(line_starts),
            )
            line_text = flat[
                line_starts[lineno - 1] : (line_starts[lineno] - 1)
                if lineno < len(line_starts)
                else len(flat)
            ].strip()
            kind = (
                line_kinds[lineno - 1] if 0 < lineno <= len(line_kinds) else "prose"
            )
            out.append(
                {
                    "pattern": label,
                    "match": m.group(0),
                    "line": lineno,
                    "context": line_text,
                    "kind": kind,
                }
            )
    return out


def audit_skill(skill_dir: Path) -> dict:
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    body_offset = parse_frontmatter_offset(text)
    body = text[body_offset:].lstrip("\n")
    body_lines = body.count("\n")

    all_high = find_matches(body, HIGH_PATTERNS)
    all_med = find_matches(body, MED_PATTERNS)
    # Filter out matches inside code blocks or table rows — those are
    # literal data being demonstrated (commit-message examples, etc.),
    # not authorial attributions.
    high_matches = [m for m in all_high if m["kind"] == "prose"]
    med_matches = [m for m in all_med if m["kind"] == "prose"]
    excluded_high = [m for m in all_high if m["kind"] != "prose"]
    excluded_med = [m for m in all_med if m["kind"] != "prose"]

    # Total ADR refs in body (any form, deduped)
    flat_body = MD_LINK_RE.sub(r"\1", body)
    adr_refs = set(re.findall(r"ADR-\d{3}", flat_body))
    total_occurrences = len(re.findall(r"ADR-\d{3}", flat_body))

    return {
        "skill": skill_dir.name,
        "body_lines": body_lines,
        "unique_adrs": len(adr_refs),
        "total_adr_occurrences": total_occurrences,
        "high_conf_count": len(high_matches),
        "med_conf_count": len(med_matches),
        "type3_candidates": len(high_matches) + len(med_matches),
        "density_per_100l": round(
            (len(high_matches) + len(med_matches)) / max(body_lines, 1) * 100, 2
        ),
        "excluded_count": len(excluded_high) + len(excluded_med),
        "high_matches": high_matches,
        "med_matches": med_matches,
        "excluded_matches": excluded_high + excluded_med,
    }


def write_summary_csv(rows: list[dict], path: Path) -> None:
    cols = [
        "skill",
        "body_lines",
        "unique_adrs",
        "total_adr_occurrences",
        "high_conf_count",
        "med_conf_count",
        "type3_candidates",
        "density_per_100l",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in cols})


def write_report_md(rows: list[dict], path: Path) -> None:
    lines: list[str] = []
    lines.append("# Type-3 ADR attribution audit\n")
    lines.append("Generated by `adr-audit.py` against `skills/*/SKILL.md`.\n")
    lines.append(
        "Detects likely type-3 attribution patterns (parenthetical "
        "`(ADR-NNN)`, `per ADR-NNN`, `implements ADR-NNN`, etc.) so the "
        "scope of `notes/refactoring-ideas.md` entry #2 can be sized.\n"
    )
    lines.append(
        "**HIGH confidence**: bare/parenthetical attributions and "
        "explicit attribution verbs (`per`, `implements`, `following`).\n"
    )
    lines.append(
        "**MEDIUM confidence**: ambiguous between type-1/2/3 (`see ADR-NNN`, "
        "`ADR-NNN is explicit`). Manually verify before pruning.\n"
    )

    # Summary table
    lines.append("## Summary\n")
    lines.append(
        "| skill | body lines | unique ADRs | total occurrences | high-conf | med-conf | type-3 candidates | density / 100 lines |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    rows_sorted = sorted(rows, key=lambda r: -r["high_conf_count"])
    totals = {
        "body_lines": sum(r["body_lines"] for r in rows),
        "unique_adrs": sum(r["unique_adrs"] for r in rows),
        "total_adr_occurrences": sum(r["total_adr_occurrences"] for r in rows),
        "high_conf_count": sum(r["high_conf_count"] for r in rows),
        "med_conf_count": sum(r["med_conf_count"] for r in rows),
        "type3_candidates": sum(r["type3_candidates"] for r in rows),
    }
    for r in rows_sorted:
        lines.append(
            f"| `{r['skill']}` | {r['body_lines']} | {r['unique_adrs']} | "
            f"{r['total_adr_occurrences']} | {r['high_conf_count']} | "
            f"{r['med_conf_count']} | {r['type3_candidates']} | {r['density_per_100l']} |"
        )
    lines.append(
        f"| **TOTAL ({len(rows)} skills)** | {totals['body_lines']} | "
        f"{totals['unique_adrs']} | {totals['total_adr_occurrences']} | "
        f"**{totals['high_conf_count']}** | {totals['med_conf_count']} | "
        f"**{totals['type3_candidates']}** | — |"
    )
    lines.append("")

    # Per-pattern tally (high-confidence only)
    pattern_tally: dict[str, int] = {}
    for r in rows:
        for m in r["high_matches"]:
            pattern_tally[m["pattern"]] = pattern_tally.get(m["pattern"], 0) + 1
    lines.append("## High-confidence patterns by frequency\n")
    lines.append("| pattern | count |")
    lines.append("|---|---:|")
    for label, count in sorted(pattern_tally.items(), key=lambda x: -x[1]):
        lines.append(f"| `{label}` | {count} |")
    lines.append("")

    # Per-skill match listing
    lines.append("## Per-skill matches\n")
    lines.append(
        "Listed in source order. Manually verify whether each is genuinely "
        "type-3 (prune) versus type-1 (canonical anchor — keep) or type-2 "
        "(load-bearing schema — keep).\n"
    )
    for r in rows_sorted:
        if not r["high_matches"] and not r["med_matches"]:
            continue
        lines.append(f"### `{r['skill']}`  ({r['type3_candidates']} candidates)\n")
        if r["high_matches"]:
            lines.append("**High confidence:**\n")
            for m in sorted(r["high_matches"], key=lambda m: m["line"]):
                lines.append(
                    f"- L{m['line']}  `{m['pattern']}`  →  `{m['match']}`"
                )
                lines.append(f"  > {m['context']}")
        if r["med_matches"]:
            lines.append("\n**Medium confidence:**\n")
            for m in sorted(r["med_matches"], key=lambda m: m["line"]):
                lines.append(
                    f"- L{m['line']}  `{m['pattern']}`  →  `{m['match']}`"
                )
                lines.append(f"  > {m['context']}")
        lines.append("")

    # Skills with zero candidates
    zero = [r["skill"] for r in rows if r["type3_candidates"] == 0]
    if zero:
        lines.append("## Skills with zero candidates\n")
        for s in sorted(zero):
            lines.append(f"- `{s}`")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if not SKILLS.exists():
        print(f"skills dir not found: {SKILLS}", file=sys.stderr)
        return 2

    skill_dirs = sorted(
        p for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").exists()
    )
    rows = [audit_skill(p) for p in skill_dirs]

    csv_path = HERE / "adr-attributions.csv"
    md_path = HERE / "adr-attributions.md"
    write_summary_csv(rows, csv_path)
    write_report_md(rows, md_path)

    total_high = sum(r["high_conf_count"] for r in rows)
    total_med = sum(r["med_conf_count"] for r in rows)
    print(f"wrote {csv_path}")
    print(f"wrote {md_path}")
    print(
        f"summary: {total_high} high-confidence + {total_med} medium-confidence "
        f"type-3 candidates across {len(rows)} skills"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
