# Skills Audit — Findings (v2, 2026-05-07)

This is the merged final findings document. It supersedes
`findings.md` (v1) and incorporates: (a) corrections from a direct
source check against Anthropic's canonical Skills guidance retrieved
2026-05-07, (b) substantive feedback from the
`openai/gpt-5.5` independent verification pass
(`verification-openai_gpt-5.5.md`), and (c) re-scoring under the
corrected `methodology-v2.md` rubric (`skills-audit-judgment-v2.csv`).

v1 is preserved in this directory as the audit trail. v2 is what to
refactor against.

## Cohort at a glance

| Metric | Min | Median | Max |
|---|---:|---:|---:|
| `body_lines` | 97 | 221 | 586 |
| `body_tokens_est` | 968 | 2,487 | 6,685 |
| `desc_chars` | 63 | — | 238 |

The cohort spans **6× in body length** (97 → 586 lines). The largest
seven skills account for the bulk of total surface area; the smallest
seven are tight one-pagers.

## What changed from v1

| Item | v1 | v2 |
|---|---|---|
| Description triggers | 0/19 had triggers | **19/19 have triggers** under the corrected rubric (concrete artifact nouns count) |
| Description when-framing | 0/19 had explicit "Use when…" | **9/19 yes, 4/19 partial, 6/19 no** |
| Body second-person | 7 skills flagged as "contrary to guidance" | **Retracted.** The third-person rule applies to descriptions only (Anthropic best-practices) |
| Missing sidecars | Flagged for `complete-milestone`, `milestone-summary` | **Downgraded to consistency note.** "A basic Skill starts with just a SKILL.md file" — not required |
| `deep_links` finding | Not surfaced | Inspected; **all candidates are false positives** (placeholder `(...)` hrefs, target-project refs, back-refs) — methodology fix queued instead |
| Adjacent-skill ambiguity | Not surfaced | **Added as Finding #5** (per GPT-5.5) |
| Refactor order | Sidecar fixes before body slimming | **Reordered**: body slimming has higher token-cost ROI than sidecar consistency |

## Headline findings (ranked by leverage)

### 1. Six descriptions still lack a "when" framing

Under the corrected rubric, every description has triggers (concrete
artifact nouns), but **6 of 19** still lack a clear invocation
context:

- `adr-writer`
- `changelog`
- `claude-issue-executor`
- `prd-normalizer`
- `prd-to-mvp`
- `release`

These are pure capability statements ("Tag a semver release…",
"Normalize a standard or custom PRD…"). Anthropic's three example
descriptions all use the literal "Use when…" pattern; adopting it
here is the single highest-leverage fix.

A further **4 of 19** have only positional/chain framing (`check-plan`,
`clarify`, `issue-planner`, `planning` — "before X", "between X and
Y", "chained from Z"). These work for readers already inside the
workflow but are weaker for cold-start routing.

**Recommendation.** Adopt the canonical Anthropic template for every
description:

> `[what it does]. Use when [trigger contexts / file types / user phrases].`

Example rewrite for `release`:

> Tag a semver release, generate release notes via /changelog, and publish a GitHub Release. Use when the user is ready to cut, tag, and publish a release; for release notes alone, use /changelog instead.

> Note the boundary clause — see Finding #5.

### 2. Four skills exceed the L2 token target; one exceeds the line budget

| Skill | `body_lines` | `body_tokens_est` | over 500 lines | over 5k tokens (est) |
|---|---:|---:|---|---|
| `claude-issue-executor` | 586 | 6,685 | yes | yes |
| `pr-review-packager` | 471 | 5,602 | no | yes |
| `release` | 474 | 5,438 | no | yes |
| `prepare-issue` | 405 | 5,197 | no | yes |
| `changelog` | 436 | 4,328 | no | (close: 87%) |

Anthropic's verbatim guidance: "Keep SKILL.md body under 500 lines for
optimal performance" + the overview's L2-tier budget of "Under 5k
tokens." `claude-issue-executor` is the only line-budget violation;
four are estimated over the token target.

> **Caveat.** `body_tokens_est` is `chars / 4`. For borderline cases
> (`prepare-issue` at 5,197), confirm with a real tokenizer before
> enforcing.

**Recommendation.** Apply progressive disclosure to these four:

- `claude-issue-executor`: extract "Failure modes & recovery" and
  worked-example content into a sidecar. Target: ≤300 lines / ≤3,500
  tokens in SKILL.md.
- `pr-review-packager`, `release`, `prepare-issue`: lift extensive
  worked examples or branch-state matrices into sidecars.

After the refactor, re-run `audit.py` and aim for the entire cohort
under 5,000 estimated tokens.

### 3. Cohort consistency: sidecar naming and presence

Two related observations, downgraded from "violations" to
"consistency":

- 18/19 skills use `example.md`; `prd-normalizer` uses `examples.md`
  (plural). Trivial drift.
- 17/19 skills have one sidecar (`example.md`); `complete-milestone`
  and `milestone-summary` have none; `check-plan` has two
  (`criteria.md` + `example.md`).

Anthropic does not require examples — "A basic Skill starts with just
a SKILL.md file." So this is purely cohort consistency.

**Recommendation.**
- Rename `prd-normalizer/examples.md` → `example.md` (one-line PR).
- Decide cohort policy on examples: either add examples to
  `complete-milestone` and `milestone-summary` for consistency, or
  document in `docs/skills.md` why those two don't need them. Either
  is fine; pick one.
- `check-plan/criteria.md` is a legitimate progressive-disclosure
  sidecar and a useful precedent for the Finding #2 refactors.

### 4. Routing test: 9/10 confidence, with one ambiguity cluster

GPT-5.5's independent routing test (10 self-generated user prompts
against the 19 descriptions only) returned 9/10 confident routes,
with the one medium-confidence call at `prepare-issue` vs
`claude-issue-executor`. So the routing problem is **real but
localized** — not the cohort-wide blackout v1 implied.

**Recommendation.** Combine the description rewrites in Finding #1
with explicit boundary clauses for the adjacent-skill clusters in
Finding #5 below.

### 5. Adjacent-skill boundary ambiguity

Several pairs/triples of skills operate on the same artifact or
workflow stage and share vocabulary:

| Cluster | Disambiguation needed |
|---|---|
| `prepare-issue` ↔ `claude-issue-executor` | "before implementation" vs "after `prompts/issue-NNN-*.md` exists" |
| `pause` ↔ `resume` | "end of session / handoff" vs "start of session / briefing" |
| `planning` ↔ `clarify` ↔ `adr-writer` | "capture context" vs "resolve open questions" vs "draft ADR files" |
| `changelog` ↔ `release` | "render notes" vs "tag and publish" |
| `audit-milestone` ↔ `complete-milestone` ↔ `milestone-summary` | "verify before close" vs "close" vs "summarise after close" |

**Recommendation.** Each description in these clusters should include
both a positive trigger and a boundary clause. Example:

> `prepare-issue`: Auto-fill an issue prompt from a GitHub issue number, linked ADRs, and the build-out plan, then write it to prompts/issue-NNN-short-title.md. Use when preparing to work on an issue before implementation; for the implementation session itself, use claude-issue-executor.

This finding originated in GPT-5.5's verification and is the most
substantive net-new contribution beyond v1.

### 6. Cohort outline shape is loosely consistent

H2 counts vary 8–18 across skills with no enforced template. Most
follow some flavour of `When to use → Inputs → Output → Workflow →
Self-check → Handoff`. Soft finding; defer until after Findings #1–5
are addressed.

**Recommendation.** If the cohort grows past 19, codify a SKILL.md
template under `templates/skill-md-template.md` and reference it from
`CLAUDE.md`. Until then, no action.

## Things that are fine

Confirmed by source check:

- **`name` field**: every skill has a valid `name` matching its
  directory; none exceed 64 chars or use reserved words.
- **`description` length**: every description is ≤238 chars, well
  under the 1,024 limit. The problem is content (Finding #1), not
  size.
- **Description voice**: 0 descriptions use first or second person
  (per Anthropic's "Always write in third person" rule for
  descriptions).
- **Body voice**: imperative + occasional "you/your" in skill bodies
  is acceptable per Anthropic's own examples. v1's Finding #5 is
  retracted.
- **Forward slashes**: 0 backslash paths in any body.
- **Frontmatter consistency**: every skill carries `name`,
  `description`, and `permission-category`. The kit-specific
  `permission-category` field is universal and consistent — keep as
  is.
- **Reference depth**: cohort has no actual depth-2 violations. The
  `deep_links` column produces false positives (heuristic fix queued
  in `methodology-v2.md §3.2`).

## Suggested refactor order (revised per GPT-5.5 input)

In order of leverage per unit of churn:

1. **Description rewrites** (Findings #1 + #5). Touches metadata only,
   doesn't change behaviour, biggest payoff for routing. Bundle the
   "Use when…" rewrites with the boundary-clause rewrites for the
   adjacent-skill clusters. Single PR, all 19 descriptions.
2. **Body slimming for the four large skills** (Finding #2). Larger
   lift but mechanical: lift sections into sidecars, leave a one-line
   reference back in SKILL.md. Start with `claude-issue-executor`
   (the only outright budget violation), then `release`,
   `prepare-issue`, `pr-review-packager`.
3. **`deep_links` heuristic fix** in `audit.py`. Trivial code change;
   cleans up future audit signal.
4. **Sidecar consistency** (Finding #3). Rename
   `prd-normalizer/examples.md` → `example.md`. Decide cohort policy
   on `complete-milestone` / `milestone-summary` examples (add or
   document the exception).
5. **Outline templating** (Finding #6). Defer until cohort grows.

> v1 ranked sidecar consistency above body slimming. GPT-5.5 was
> right to flip these — body slimming has materially higher
> token-cost ROI, and the sidecar issues are now downgraded from
> violations to cosmetic.

Each of these can be a discrete issue under a single "Skills audit
follow-ups" milestone.

## Validation

To validate this report independently, run the procedure in
`methodology-v2.md §4.3`. The deterministic CSV is reproducible from
a clean checkout via `python3 audit.py`. The qualitative judgments
(`skills-audit-judgment-v2.csv`) should be re-scored against the
corrected rubric in `methodology-v2.md §4.1` — agreement on the
6 skills still scoring `has_when=no` is the most important sanity
check, since those drive Finding #1.

## Files in this audit (final)

```
notes/skills-audit-2026-05-07/
├── audit.py                                  (deterministic audit script)
├── verify.py                                 (OpenRouter verification script)
│
├── methodology.md                            (v1 — kept for audit trail)
├── methodology-v2.md                         (v2 — current)
│
├── skills-audit.csv                          (deterministic data, unchanged)
├── skills-audit-judgment.csv                 (v1 — kept for audit trail)
├── skills-audit-judgment-v2.csv              (v2 — re-scored under corrected rubric)
│
├── findings.md                               (v1 — kept for audit trail)
├── findings-v2.md                            (v2 — this file, what to refactor against)
│
├── verification-openai_gpt-5.5.md            (independent review)
├── verification-openai_gpt-5.5.json          (raw API response)
└── verification-openai_gpt-5.5-pro.json      (failed reasoning-budget run; cost record)
```
