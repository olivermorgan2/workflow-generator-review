# Verification report

## 1. Methodology check

### Deterministic methodology (§3)

Mostly sound for reproducible mechanical checks. I would make two corrections/clarifications:

- **`desc_has_when_marker` is intentionally narrow, but should not be interpreted as “no descriptions state when.”** It only detects `"use when"`, `"when the user"`, and `"trigger when"`. Anthropic guidance does not require those exact phrases; it requires enough “what + when + triggers” information in the description. A description can satisfy “when” without the literal marker, e.g. “Brief a fresh Claude Code session…” or “Generate … for a closed or near-closing milestone…”.
- **`body_tokens_est = round(len(body)/4)` is acceptable as triage, not as a canonical Anthropic token-budget verdict.** The methodology says this, but findings later lean on “over 5k tokens” as if exact. I would phrase those as “estimated over 5k; confirm with tokenizer before enforcing.”

### Qualitative methodology (§4.1)

The rubric is broadly aligned with Anthropic’s “what + when + triggers” guidance, but it has one internal tension and one over-strict example.

#### `has_when`

Sound in principle:

- `yes` for explicit “Use when…” / “Trigger when…”
- `yes` for a recognizable trigger noun framed as the invocation context
- `partial` for workflow-only sequencing or chain context
- `no` for pure capability statements

However, the prior audit applies this more strictly than the rubric. Anthropic does not require the literal phrase “Use when.” Descriptions like `resume` (“Brief a fresh Claude Code session…”) and `milestone-summary` (“for a closed or near-closing milestone…”) do provide recognizable invocation contexts and should be closer to `yes` than `partial`.

#### `has_triggers`

This rubric is less clean. It says concrete file types, slash commands, user phrases, or named artifacts score `yes`; but the note says “Tag a semver release” scores `has_triggers=no`. That is too strict. “semver release,” “GitHub Release,” “PR,” “ADR,” “GitHub issue number,” `design/state.md`, and `prompts/issue-NNN-short-title.md` are concrete routing hooks even if not introduced by “Use when.”

Concrete revision:

> `has_triggers=yes` — description includes concrete user-visible hooks such as artifact names, file paths, commands, issue/PR/release/milestone nouns, or likely user terms.  
> `partial` — hooks exist but are internal, indirect, or only meaningful after knowing this workflow.  
> `no` — generic wording only.

With that revision, many prior `has_triggers=no` scores become `partial` or `yes`.

#### Omission

The methodology does not explicitly score **negative routing boundaries** in descriptions: “does not do X,” “not for Y,” “before/after Z.” Anthropic best practices emphasize clear descriptions for selection among multiple skills; in a 19-skill workflow cohort, disambiguators matter. This could be added as a non-binary cohort check rather than per-skill field.

---

## 2. Independent re-scoring of `skills-audit-judgment.csv`

Using only methodology §4.1 and the supplied frontmatter descriptions:

| skill | gpt_has_what | gpt_has_when | gpt_has_triggers | gpt_third_person | agree_with_prior | note |
|---|---|---|---|---|---|---|
| adr-writer | yes | no | yes | yes | partial | Agree `has_when=no`, but `has_triggers` should be `yes`: “ADRs,” “architectural decision topics,” and “ADR template” are concrete named artifacts/user hooks. |
| audit-milestone | yes | yes | yes | yes | no | Prior under-scores. “Verify a GitHub milestone is complete” and “failure … before /complete-milestone” give a clear milestone-verification context plus concrete hooks: GitHub milestone, ADRs, PRs, phase exit criteria, `/complete-milestone`. |
| changelog | yes | no | yes | yes | partial | Agree `has_when=no`; disagree `has_triggers=no`. “git log between two refs,” “release notes,” “GitHub Release body” are concrete triggers. |
| check-plan | yes | partial | yes | yes | partial | Agree `has_when=partial` due chain/pre-commit context. `has_triggers` should be `yes`: ADR, issue prompt, `adr-writer`, `prepare-issue`, `--skip-check` are concrete hooks. |
| clarify | yes | partial | yes | yes | partial | Agree `has_when=partial`. `has_triggers` should be `yes`: “unresolved implementation questions,” “gray areas,” MVP scoping, ADR drafting, `design/decisions.md` are concrete enough. |
| claude-issue-executor | yes | no | yes | yes | partial | Agree `has_when=no`; disagree `has_triggers=no`. “prepared issue prompt,” “branch,” “incremental commits,” “tests,” “evaluation summary” are concrete workflow hooks. |
| complete-milestone | yes | yes | yes | yes | no | Prior too strict. “Close a GitHub milestone” is itself a user-recognizable invocation context; triggers include GitHub milestone, `design/state.md`, ADR-035, `/release`, `--milestone-phase`, `/audit-milestone`, `/milestone-summary`. |
| idea-to-prd | yes | yes | yes | yes | partial | Prior under-scores. “rough idea” is a direct user-language trigger, and “PRD draft” / `prd-normalizer` are concrete artifacts. |
| issue-planner | yes | yes | yes | yes | no | Prior too strict. The description says when the required inputs exist: `design/mvp.md` and `design/build-out-plan.md`; output GitHub issues and Project board are concrete triggers. |
| milestone-summary | yes | yes | yes | yes | partial | Prior under-scores. “for a closed or near-closing milestone” is a clear invocation context; GitHub milestone, git log, ADRs, phase range, `design/milestones/N-summary.md` are concrete hooks. |
| pause | yes | yes | yes | yes | partial | Prior under-scores. “context-window-exhausting session handoffs” is a clear when-context; `design/state.md` and `notes/handoff-YYYY-MM-DD.md` are strong triggers. |
| planning | yes | partial | yes | yes | partial | Agree `has_when=partial`: “before ADR drafting” is positional. `has_triggers` should be `yes`: requirements decomposition, risks, assumptions, sequencing rationale, open research questions, `design/planning.md`. |
| pr-review-packager | yes | yes | yes | yes | no | Prior too strict. “Draft a pull-request body… then open the PR” is a clear ready-to-open-PR context. Triggers include PR, branch, commit history, `Closes #N`, ADR references, `gh pr create`. |
| prd-normalizer | yes | no | yes | yes | partial | Agree `has_when=no`; disagree `has_triggers=no`. “standard or custom PRD” and “canonical form” are concrete enough for routing. |
| prd-to-mvp | yes | no | yes | yes | partial | Agree `has_when=no`; disagree `has_triggers=no`. “normalized PRD,” “MVP statement,” and “build-out plan” are concrete artifacts. |
| prepare-issue | yes | yes | yes | yes | no | Prior too strict. “from a GitHub issue number, linked ADRs, and the build-out plan” describes a clear preparation context; `prompts/issue-NNN-short-title.md` is a strong trigger. |
| release | yes | no | yes | yes | partial | Agree `has_when=no` under the rubric’s own “Tag a semver release” example, but `has_triggers` should be `yes`: semver release, release notes, `/changelog`, GitHub Release are concrete user hooks. |
| resume | yes | yes | yes | yes | partial | Prior under-scores. “fresh Claude Code session” is a recognizable trigger context; `design/state.md`, `gh`, blockers, next action are concrete hooks. |
| workflow-docs | yes | yes | yes | yes | no | Prior too strict. “Generate README.md and design/ai-summary.md… from PRD, MVP, ADRs, and CLAUDE.md” gives a concrete documentation-generation context and many artifact triggers. |

Summary: I agree with the prior audit that **none use the exact Anthropic-recommended “Use when…” style**, but I do **not** agree that many descriptions lack triggers. Most have concrete artifact triggers; the common weakness is framing, not absence.

---

## 3. Findings verification

### Finding 1 — “Zero descriptions explicitly state when to use the skill”

**Partial.** Agree that zero descriptions use the literal “Use when…” / “Trigger when…” formula, and that a uniform description rewrite is high-leverage. Disagree with the broader implication that zero descriptions state when: `resume`, `pause`, `milestone-summary`, `complete-milestone`, `prepare-issue`, `idea-to-prd`, `issue-planner`, `workflow-docs`, and `pr-review-packager` contain recognizable invocation contexts.

**Correction:** Retitle as: “Zero descriptions use explicit `Use when…` routing language; several rely on implicit artifact/workflow triggers.”

### Finding 2 — “Four skills exceed the L2 token budget; one exceeds the line budget”

**Agree, with one caution.** The deterministic data supports the line finding and the rough token-estimate finding. I would avoid treating `body_tokens_est` as definitive Anthropic-token counts until checked with a real tokenizer, especially for borderline cases like `prepare-issue`.

**Correction:** Say “four skills are estimated over 5k tokens” rather than “exceed” unless confirmed.

### Finding 3 — “Two skills have no sidecar at all”

**Partial.** The fact is correct: `complete-milestone` and `milestone-summary` have no sidecars. I disagree that this is necessarily a problem; Anthropic guidance recommends progressive disclosure when content is large or detailed, not uniform sidecar count for its own sake. Both are under 3k estimated tokens and below 250 lines.

**Correction:** Downgrade from a finding to a consistency/nice-to-have item. Do not add example sidecars unless examples materially improve routing or execution.

### Finding 4 — “Sidecar naming drift”

**Agree.** `prd-normalizer/examples.md` is a trivial consistency drift, and `check-plan/criteria.md` is a legitimate sidecar pattern.

**Correction:** None, except I would keep this lower priority than body slimming.

### Finding 5 — “Second-person language in skill bodies”

**Partial.** The body hit counts are useful, but Anthropic’s “third person” guidance is primarily about descriptions. Imperative instructions inside `SKILL.md` bodies often naturally address the model and may be acceptable if clear. The audit should distinguish harmful second-person prose from normal operational imperatives.

**Correction:** Reframe as “review second-person body prose for consistency” rather than “contrary to guidance.” Keep description voice as the hard requirement.

### Finding 6 — “Cohort outline shape is loosely consistent”

**Agree.** This is correctly treated as a soft finding. The cohort has a recognizable common structure but not a strict template.

**Correction:** None.

---

## 4. Routing test

Invented prompts below do not reuse the methodology’s suggested examples verbatim.

| # | User prompt | Routed skill | Confidence | Rationale / ambiguity |
|---:|---|---|---|---|
| 1 | “I’ve got a half-baked product concept and need to turn it into something structured before we design anything.” | `idea-to-prd` | High | “rough idea” → PRD draft is clear. |
| 2 | “Take this existing PRD and clean it up into the format the rest of the workflow expects.” | `prd-normalizer` | High | “existing PRD” + “canonical form” maps directly. |
| 3 | “We have the normalized PRD now; define the MVP and break out what comes later.” | `prd-to-mvp` | High | normalized PRD → MVP statement/build-out plan. |
| 4 | “Before we write ADRs, I want to capture assumptions, risks, sequencing logic, and open research questions.” | `planning` | High | Wording closely matches description. |
| 5 | “There are still a few gray areas about implementation tradeoffs; can we settle them and record the decisions?” | `clarify` | High | “gray areas,” implementation questions, decisions. |
| 6 | “Create the architecture decision records from the topics we just agreed on.” | `adr-writer` | High | ADR drafting from decision topics. |
| 7 | “Use the MVP and build-out plan to create the GitHub issues and board for the next chunk of work.” | `issue-planner` | High | Inputs and outputs match exactly. |
| 8 | “I’m ready to start coding issue 42; generate the local prompt file with the linked ADR context first.” | `prepare-issue` | Medium | Could be confused with `claude-issue-executor` because “start coding” appears, but “generate prompt file first” points to `prepare-issue`. |
| 9 | “Open a pull request for this branch and fill in the template with issue and ADR links.” | `pr-review-packager` | High | PR body/template/issue/ADR links are direct triggers. |
| 10 | “This session is running out of context; update the state file and write handoff notes for the next session.” | `pause` | High | “context-window… handoff,” `design/state.md`, handoff notes. |

### Self-score

I feel confident on **9/10**. The only medium-confidence route is prompt #8 because `prepare-issue` and `claude-issue-executor` overlap around “starting work on an issue.” The frontmatter descriptions distinguish them, but only if the model notices “generate prompt file first.”

### Descriptions causing ambiguity

- **`prepare-issue` vs `claude-issue-executor`**: both relate to issue execution. `prepare-issue` should explicitly say “before implementation” and `claude-issue-executor` should explicitly say “after a prepared issue prompt exists.”
- **`pause` vs `resume`**: distinguish “end/current session handoff” from “start/fresh session briefing” more explicitly.
- **`planning` vs `clarify` vs `adr-writer`**: all sit before/during ADR work. `planning` should be “capture context,” `clarify` should be “resolve open questions,” and `adr-writer` should be “draft ADR files.”
- **`changelog` vs `release`**: `release` chains `/changelog`; `changelog` should say it is for notes only, not tagging/publishing.

The routing cost is real, but less severe than finding #1 implies: artifacts and workflow nouns already provide many useful hooks. The main cost is ambiguity between adjacent pipeline skills, not complete invisibility.

---

## 5. Additional findings

### A. The prior audit under-weighted adjacent-skill ambiguity

The biggest routing risk is not just missing “Use when.” It is **boundary ambiguity between neighboring skills**:

- `prepare-issue` / `claude-issue-executor`
- `pause` / `resume`
- `planning` / `clarify` / `adr-writer`
- `changelog` / `release`
- `audit-milestone` / `complete-milestone` / `milestone-summary`

Concrete fix: each description should include both a positive trigger and a boundary clause when needed.

Example:

> `prepare-issue`: Auto-fill an implementation prompt file from a GitHub issue number, linked ADRs, and the build-out plan. Use when preparing to work on an issue before implementation; use `claude-issue-executor` after `prompts/issue-NNN-*.md` exists.

### B. Finding #1 should distinguish “explicit invocation language” from “trigger hooks”

Several descriptions already contain strong hooks: `GitHub milestone`, `PR`, `ADR`, `PRD`, `MVP`, `GitHub Release`, `design/state.md`, `README.md`, `prompts/issue-NNN-short-title.md`. The audit’s `has_triggers=no` scores for `release`, `changelog`, `prd-normalizer`, `prd-to-mvp`, and `claude-issue-executor` are too harsh under its own rubric.

Concrete fix: revise `skills-audit-judgment.csv` so `has_triggers` measures concrete hooks, not only explicit “Use when” framing.

### C. Description rewrites should preserve concrete artifacts, not just add “Use when”

A bad fix would be:

> “Use when the user wants help with releases.”

A better fix keeps artifacts and boundaries:

> `release`: Tag a semver release, generate release notes via `/changelog`, and publish a GitHub Release. Use when the user is ready to cut, tag, and publish a release; use `changelog` alone when only release notes are needed.

### D. `permission-category` may help humans but probably not skill routing

Every description omits permission category; frontmatter includes it separately. That is fine as a kit convention, but if users ask “do the safe/local version” vs “actually publish,” descriptions should make mutating behavior obvious. Some do (`release`, `pr-review-packager`, `complete-milestone`, `issue-planner`), but others could sharpen “writes locally” vs “creates public GitHub artifact.”

### E. The deterministic deep-link finding is absent from `findings.md`

The CSV shows `deep_links` for:

- `audit-milestone`
- `changelog`
- `workflow-docs`

Some may be harmless example references, but Anthropic best practices prefer reference depth ≤1. The prior findings do not mention this. At minimum, add a review note: verify whether sidecars link onward to local files in a way that creates multi-hop loading expectations.

### F. Body-size priority should consider routing importance, not only token count

`claude-issue-executor`, `release`, `prepare-issue`, and `pr-review-packager` are large and also likely high-frequency/high-impact. Slimming them matters. But if description routing is fixed first, the next best token ROI may be `claude-issue-executor` and `release` before minor sidecar consistency issues.

---

## 6. Bottom line

I agree that description rewrites are the highest-leverage first move, but I would adjust the sequence after that. Recommended order: **(1) rewrite all descriptions with explicit “Use when…” plus boundary clauses for adjacent skills; (2) slim the over-budget/high-impact skills, starting with `claude-issue-executor`, then `release`, `prepare-issue`, and `pr-review-packager`; (3) review deep links in sidecars; (4) rename `prd-normalizer/examples.md` to `example.md`; (5) optionally add or document missing examples for `complete-milestone` and `milestone-summary`; (6) do a light second-person/body-style sweep; (7) defer outline templating.** I disagree with the prior order mainly because adding sidecars to already-small skills and renaming one sidecar are lower leverage than reducing the four largest runtime-loaded skill bodies.