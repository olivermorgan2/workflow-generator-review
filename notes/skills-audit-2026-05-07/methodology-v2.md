# Skills Audit Methodology (v2, 2026-05-07)

This is a revision of `methodology.md` (v1) following an independent
verification pass by `openai/gpt-5.5` (report:
`verification-openai_gpt-5.5.md`) and a direct source check against
Anthropic's canonical guidance. v1 remains in the directory as the
audit trail; v2 is what to refactor against.

## Why v2

v1 had three issues that v2 fixes:

1. **Internal contradiction in the `has_triggers` rubric.** v1's prose
   said concrete artifact names count as triggers, but its example
   ("Tag a semver release" → `has_triggers=no`) treated the absence of
   a "Use when…" wrapper as missing triggers. v2 settles this in
   favour of the prose: concrete user-visible nouns count.
2. **Over-application of the third-person rule.** v1 flagged
   second-person prose in skill *bodies* as a guideline violation. The
   Anthropic rule applies to **descriptions only**. v2 drops the body
   second-person check from the violations list.
3. **Sidecars treated as expected default.** v1 called out skills with
   no sidecar as a problem. Anthropic explicitly says "A basic Skill
   starts with just a SKILL.md file" — sidecars are a progressive
   disclosure pattern when content is large, not a uniform default.
   v2 downgrades this to a cohort-consistency observation.

A summary of changes is in §7 below.

## 1. Purpose

Audit the 19 skills under `skills/<name>/SKILL.md` against the
canonical guidance for Claude Skills, with two goals:

1. **Token efficiency** — keep each skill's body under the
   Anthropic-stated 500-line / 5k-token L2 budget; push content into
   sidecars (progressive disclosure) when the body grows past that.
2. **Routing accuracy** — make every skill's `description` field
   unambiguous about *what* it does AND *when* to invoke it, so Claude
   picks the right skill from a cohort of 19. Adjacent-skill ambiguity
   matters as much as missing trigger framing.

Deterministic measurements are in `skills-audit.csv` (mechanical:
file size, regex matches, sidecar inventory). Qualitative judgments
are in `skills-audit-judgment-v2.csv` (re-scored under the corrected
rubric below).

## 2. Sources of truth

### Authoritative guidance

The two pages below were retrieved on 2026-05-07 and are the basis
for every threshold and rule cited here:

- Anthropic — Skill authoring best practices: <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>
- Anthropic — Agent Skills overview: <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview>

### Quantitative thresholds (verbatim from the source)

| Threshold | Value | Source verbatim |
|---|---|---|
| `name` max length | 64 chars | "Maximum 64 characters" (best-practices, "YAML Frontmatter" Note) |
| `name` charset | lowercase letters, numbers, hyphens | "Must contain only lowercase letters, numbers, and hyphens" |
| `name` reserved words | not "anthropic", not "claude" | "Cannot contain reserved words: 'anthropic', 'claude'" |
| `description` max length | 1,024 chars | "Maximum 1024 characters" |
| `description` content | non-empty, third person, what + when | "Should describe what the Skill does and when to use it" + "Always write in third person" |
| Body line budget | ≤500 lines | "Keep SKILL.md body under 500 lines for optimal performance" |
| L2 token budget | <5,000 tokens | Overview page table: "Level 2: Instructions … Under 5k tokens" |
| Reference depth | ≤1 (SKILL.md → file; not file → file) | "Keep references one level deep from SKILL.md" |
| Path style | forward slashes only | "Always use forward slashes in file paths, even on Windows" |
| Description voice | third person, names *what* AND *when* | "**Always write in third person**. The description is injected into the system prompt…" |
| MCP tool refs | fully qualified `Server:tool_name` | "Format: `ServerName:tool_name`" |

### Repository-specific facts

- 19 skills under `skills/<name>/SKILL.md` as of branch
  `rename-design-directory-lowercase`, commit `5808f19`.
- Every skill carries a `permission-category` frontmatter field. This
  is a kit convention (`docs/workflow-guide.md §7`), not part of
  Anthropic's canonical schema. v2 records it as universal cohort
  practice; not flagged.
- v2 also recognises `disable-model-invocation` and `allowed-tools` as
  optional canonical fields per the Anthropic best-practices page.

## 3. Deterministic checks (reproduced by `audit.py`)

### 3.1 How to run

From a clean checkout, with Python 3.10+:

```bash
cd notes/skills-audit-2026-05-07
python3 audit.py
```

Writes `skills-audit.csv`. Schema unchanged from v1; column-by-column
definitions in v1 §3.2 still apply.

### 3.2 Known false-positive in `deep_links`

v1 flagged `deep_links` for `audit-milestone`, `changelog`, and
`workflow-docs` as candidate depth-2 violations. After manual
inspection, **all three are false positives**:

- `changelog/example.md` uses literal `(...)` placeholders inside
  markdown link syntax for elided GitHub URLs, which the regex picks
  up as local hrefs.
- `workflow-docs/example.md` references **target-project** files
  (`design/adr/`, `CLAUDE.md`, `design/mvp.md`) that the rendered
  README would point to — not files inside the skill directory. These
  are runtime documentation links, not skill-internal load chains.
- `audit-milestone/example.md` has one back-reference to its own
  `SKILL.md`, which is meta-cross-reference, not a chain Claude would
  load from.

The Anthropic rule ("Keep references one level deep from SKILL.md")
is about **files Claude loads via bash to follow a workflow** — a
sidecar that itself links to another sidecar in the same skill.
References from a sidecar to project files or back to SKILL.md are
not what the rule prohibits.

**v2 action.** Improve the heuristic so it only flags hrefs that
point to other `.md` files inside the same skill directory. Until
then, treat the `deep_links` column as triage, not verdict, and
manually inspect any non-empty value.

### 3.3 Reproducibility checks for ChatGPT

Same procedure as v1 §3.3.

## 4. Qualitative checks (`skills-audit-judgment-v2.csv`)

Scored by a reviewer (human or LLM) against the rubric below.

### 4.1 Description quality rubric (corrected)

Score each description on four fields:

#### `has_what` — does the description name what the skill does?

- **yes** — a reader can tell from the description alone what the
  skill produces or which artifact it manipulates.
- **no** — vague ("helps with documents", "processes data", "does
  stuff with files" — using Anthropic's own bad-example list).

#### `has_when` — does the description name a trigger context?

- **yes** — the description gives a recognisable invocation context.
  This may be:
  - An explicit "Use when…" / "Trigger when…" phrase (the canonical
    pattern in all three Anthropic-supplied example descriptions).
  - A noun phrase that frames the trigger directly (e.g. "for a
    closed or near-closing milestone", "fresh Claude Code session",
    "rough idea").
- **partial** — workflow positioning only ("before ADR drafting",
  "chained from /prepare-issue") — useful inside the workflow,
  weaker for cold-start routing.
- **no** — pure capability statement with no trigger context.

#### `has_triggers` — are concrete user-language triggers present? (corrected from v1)

> **v2 correction.** v1's example scored "Tag a semver release" as
> `has_triggers=no`, contradicting v1's own prose that file types,
> commands, and named artifacts count. v2 settles this: concrete
> user-visible nouns *are* triggers. The framing question is
> separately captured by `has_when`.

- **yes** — description includes concrete user-visible hooks: artefact
  names, file paths, commands, slash-commands, issue/PR/release/
  milestone nouns, or other terms users actually type.
- **partial** — hooks are present but only meaningful after knowing
  this kit's workflow (e.g. internal filenames the user wouldn't say).
- **no** — generic wording only.

#### `third_person` — is the description written in third person?

- **yes** — no "I", "you", "we", or "your" outside literal quoted
  examples.
- **no** — first/second person.

> **Scope note (corrected from v1).** This rule applies to the
> `description` field only. The Anthropic guidance is:
> "Always write in third person. The description is injected into the
> system prompt, and inconsistent point-of-view can cause discovery
> problems." Skill **bodies** routinely use imperative voice ("Run X",
> "Create Y") and address Claude in second person in Anthropic's own
> examples; that is acceptable. v1's body-second-person finding is
> retracted.

### 4.2 Cohort-wide qualitative checks

Same as v1 §4.2 (outline shape consistency, terminology drift,
boilerplate, routing test). One addition:

5. **Adjacent-skill boundary check.** For pairs/triples of skills
   that operate on the same artifact or stage of the workflow,
   inspect their descriptions to confirm a reader can tell them
   apart from descriptions alone. Known overlapping clusters in this
   cohort:
   - `prepare-issue` ↔ `claude-issue-executor`
   - `pause` ↔ `resume`
   - `planning` ↔ `clarify` ↔ `adr-writer`
   - `changelog` ↔ `release`
   - `audit-milestone` ↔ `complete-milestone` ↔ `milestone-summary`
   For each pair, the description should include a positive trigger
   *and* a boundary clause when the pair is genuinely close
   (e.g., "Use when X; for Y, use /other-skill").

### 4.3 How ChatGPT (or another reviewer) should validate

Same procedure as v1 §4.3, plus:

- Re-score using the corrected `has_triggers` rubric in §4.1.
- Run the §4.2.5 adjacent-skill boundary check as a discrete pass.

## 5. Known limitations

Same as v1 §5, plus:

- **`deep_links` heuristic over-triggers.** See §3.2.
- **Token estimate is rough.** `chars / 4` is fine for relative
  ranking. Use a real tokenizer before enforcing the 5k-token target
  on borderline cases (`prepare-issue` at ~5,197 estimated tokens).

## 6. What the source check confirms vs. corrects

| v1 claim | Source check (verbatim quotes in §2) | v2 disposition |
|---|---|---|
| Third-person rule applies to bodies | "**Always write in third person**." appears under the "Writing effective descriptions" heading; bodies show imperative + "you/your" throughout official examples | **Corrected.** Descriptions only. |
| Every skill needs a worked-example sidecar | "A basic Skill starts with just a SKILL.md file" + Examples pattern is described as "For Skills where output quality depends on seeing examples" | **Corrected.** No requirement; cohort consistency only. |
| Concrete nouns aren't triggers without "Use when" | Anthropic example: "Use when working with PDF files **or when the user mentions PDFs, forms, or document extraction**" — concrete nouns are explicitly listed as triggers | **Corrected.** Concrete nouns count. |
| Reference depth ≤1 is a real rule | "**Keep references one level deep from SKILL.md.**" | **Confirmed.** But cohort has no real violations (see §3.2). |
| Body ≤500 lines | "Keep SKILL.md body under 500 lines for optimal performance" | **Confirmed.** |
| L2 ≤5k tokens | Overview table | **Confirmed**, with estimator caveat. |

## 7. Summary of changes from v1

- §4.1 `has_triggers`: contradictory example removed; rubric explicit
  that concrete nouns count.
- §4.1 `third_person`: scope clarified to descriptions only.
- §4.2: adjacent-skill boundary check added (§4.2.5).
- §3.2: deep_links false-positive note added; heuristic flagged for
  improvement.
- §6: source-check matrix added so future reviewers can see which v1
  claims survived contact with the canonical docs.
- The judgment CSV is replaced by `skills-audit-judgment-v2.csv` —
  every skill re-scored under §4.1; `change_from_v1` column shows
  what moved.

## 8. Versioning

This is v2 (2026-05-07), superseding v1 (`methodology.md`) of the
same date. v1 is preserved as the audit trail. If the SKILL spec
changes upstream, update §2's verbatim-quote table and bump.
