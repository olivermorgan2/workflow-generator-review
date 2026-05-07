#!/usr/bin/env python3
"""
Send the audit deliverables to OpenRouter (default: openai/gpt-5.5-pro)
for independent verification, per methodology.md §4.3.

Outputs:
    verification-<model>.md    — the model's verdicts + disagreements
    verification-<model>.json  — raw API response (for cost / debugging)

Usage:
    OPENROUTER_API_KEY=... python3 verify.py [model_id]
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = (HERE / ".." / ".." / "skills").resolve()
DEFAULT_MODEL = "openai/gpt-5.5"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_frontmatter(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?\n)---", text, re.DOTALL)
    return m.group(1) if m else ""


def build_prompt() -> tuple[str, str]:
    methodology = read(HERE / "methodology.md")
    deterministic_csv = read(HERE / "skills-audit.csv")
    judgment_csv = read(HERE / "skills-audit-judgment.csv")
    findings = read(HERE / "findings.md")

    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    frontmatters = "\n\n".join(
        f"### {p.name}\n```\n{extract_frontmatter(p / 'SKILL.md').rstrip()}\n```"
        for p in skill_dirs
    )

    system = (
        "You are an independent senior reviewer auditing another AI's audit of a "
        "Claude Skills repository. Your job is to verify, disagree, and add findings — "
        "not to re-summarise what the prior audit already says. Be specific. Cite the "
        "skill name and (where relevant) the rubric field for every disagreement. "
        "Prefer concrete revisions over abstract critique. If you agree with a finding, "
        "say 'agree' and move on; if you partially agree, say what you'd change."
    )

    user = f"""\
# Verification request

A prior audit of 19 Claude Skills was produced under the methodology
below. Your job is to validate it against the canonical Anthropic
guidance for Skills (Agent Skills overview + best-practices). The
prior audit is in this directory; you are receiving its full contents
inline.

## What I want from you

Produce a markdown report with these sections:

1. **Methodology check** — Is the methodology in §3 (deterministic) and
   §4 (qualitative) sound? Specifically: does the rubric for `has_when`
   and `has_triggers` correctly reflect Anthropic's "what + when +
   triggers" requirement? Flag any omissions or over-strict criteria.

2. **Independent re-scoring of `skills-audit-judgment.csv`** —
   Re-score each of the 19 descriptions using only the rubric in
   methodology §4.1, given the raw frontmatters supplied below.
   Produce a table with columns: `skill | gpt_has_what | gpt_has_when |
   gpt_has_triggers | gpt_third_person | agree_with_prior | note`. The
   `agree_with_prior` column is yes / no / partial. Where `partial` or
   `no`, the `note` must say what you'd change and why.

3. **Findings verification** — For each of the six findings in
   `findings.md`, state: `agree` / `partial` / `disagree`, with one or
   two sentences of rationale. If `partial` or `disagree`, propose the
   correction.

4. **Routing test** — Invent 10 user prompts (do NOT reuse the
   suggested examples in methodology §4.2.4 — write your own; keep them
   realistic for someone using a workflow kit like this). Given only
   the 19 descriptions in the frontmatters below, which skill would
   you route each prompt to? Score yourself: how many do you feel
   confident about? Which descriptions caused ambiguity? This gives
   the maintainer a real signal on the cost of finding §1.

5. **Additional findings** — Anything the prior audit missed or
   under-weighted. Be willing to surface things even if minor.

6. **Bottom line** — One paragraph: what is the highest-leverage
   refactoring sequence, and do you agree with the prior audit's
   suggested order? If you disagree, propose your own ranking.

Don't repeat the prior audit. Assume the maintainer has already read
it. Spend your tokens on disagreement, refinement, and the routing
test — those are the parts only you can add.

---

## Methodology (verbatim from `methodology.md`)

{methodology}

---

## Raw SKILL.md frontmatters (for independent re-scoring)

{frontmatters}

---

## Deterministic CSV (`skills-audit.csv`)

```csv
{deterministic_csv}```

---

## Qualitative judgments to validate (`skills-audit-judgment.csv`)

```csv
{judgment_csv}```

---

## Prior audit findings (`findings.md`)

{findings}
"""
    return system, user


def main() -> int:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY not set", file=sys.stderr)
        return 2

    model = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL

    system, user = build_prompt()
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        # Cap reasoning so the entire output budget isn't consumed by hidden
        # reasoning tokens (failure mode observed with gpt-5.5-pro).
        "reasoning": {"effort": "low"},
        "max_tokens": 12000,
    }

    print(f"sending to {model}...", file=sys.stderr)
    print(f"  prompt size: {len(system) + len(user):,} chars (~{(len(system)+len(user))//4:,} tokens)", file=sys.stderr)

    # POST via curl — Python 3.14 on this machine has no CA bundle configured
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(body, f)
        body_path = f.name

    try:
        result = subprocess.run(
            [
                "curl", "--silent", "--show-error", "--fail-with-body",
                "--max-time", "300",
                "-H", f"Authorization: Bearer {api_key}",
                "-H", "Content-Type: application/json",
                "-H", "HTTP-Referer: https://github.com/anthropics/skills",
                "-H", "X-Title: skills-audit-verification",
                "--data-binary", f"@{body_path}",
                "https://openrouter.ai/api/v1/chat/completions",
            ],
            capture_output=True,
            text=True,
            timeout=320,
        )
    finally:
        os.unlink(body_path)

    if result.returncode != 0:
        print(f"curl failed (exit {result.returncode})", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return 1

    data = json.loads(result.stdout)

    safe_model = model.replace("/", "_").replace(":", "_")
    raw_path = HERE / f"verification-{safe_model}.json"
    raw_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    content = data["choices"][0]["message"]["content"]
    md_path = HERE / f"verification-{safe_model}.md"
    md_path.write_text(content, encoding="utf-8")

    usage = data.get("usage", {})
    print(f"wrote {md_path}", file=sys.stderr)
    print(f"  prompt_tokens={usage.get('prompt_tokens')}  "
          f"completion_tokens={usage.get('completion_tokens')}  "
          f"total={usage.get('total_tokens')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
