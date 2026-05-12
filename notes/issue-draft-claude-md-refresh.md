<!--
  Draft GitHub issue body for "Refresh CLAUDE.md — drop dated stub framing".
  Source: notes/refactoring-ideas.md entry #4.
  Review, then file with: gh issue create --title "..." --body "$(cat this-file.md)"
-->

## Summary

Surgical refresh of `CLAUDE.md` to remove the dated `## What this file is NOT` footer left over from the kit's earliest issues. That section describes the file as "a stub added in Issue #1 ... a fuller `CLAUDE.md` ... will be written alongside the template work in later issues" — anachronistic after 70+ shipped issues, four milestones, and substantive load-bearing rules already in the body. Keep every other section byte-identical.

## ADR

None required. `CLAUDE.md` is the kit's project-rules file. The **rules themselves** aren't changing — only the framing prose around them. Per the `notes/refactoring-ideas.md` preamble's ADR test ("ADR only when the refactor changes a kit convention that target projects depend on"), this is below the threshold. The kit-internal `CLAUDE.md` is a different artefact from the target-project template at `templates/claude-md-template.md`, so target projects are unaffected.

## Why

`CLAUDE.md` is the first file Claude Code reads on every session in this repo. Right now its bottom section literally tells the LLM:

> This file is a stub added in Issue #1 so Claude Code has a minimal rules baseline while working on the kit. A fuller `CLAUDE.md` — with commands, testing expectations, and review conventions — will be written alongside the template work in later issues.

Two problems:

1. **Misleading framing.** "Issue #1" was the kit-bootstrap milestone; the kit is four milestones past it. The "later issues" deferral has already happened — the load-bearing rules (plan-first per ADR-006, ADR-numbered commit messages, the SKILL.md style guide added by #85, the "never edit accepted ADRs" rule with the ADR-044 exception, the dogfooding bootstrap step) are all in the body now. The file is not a stub.
2. **Eager-load token cost.** `CLAUDE.md` is loaded into context on every session. Stale "what this file isn't" prose pays a token cost on every invocation without delivering current information. The eager-load surface is the most expensive bytes in the kit per session.

This pairs naturally with the just-shipped #89 / #91 — both were "kit docs now lie about reality" cleanups in adjacent surfaces (`docs/` and `examples/`). `CLAUDE.md` is the third surface where post-MVP framing went stale, and it has the highest blast radius per token because it's eager-loaded on every session.

## Scope

### Path chosen: Path A (surgical edit)

Two paths were considered in `notes/refactoring-ideas.md` entry #4:

- **Path A** — surgical removal of dated sections; preserve load-bearing rules verbatim. **Chosen.**
- **Path B** — rewrite from scratch using `templates/claude-md-template.md` as a starting point. Rejected — invites accidental rule drift, and the file isn't broken, just dated in its framing. More invasive than the trigger warrants.

### What gets removed

- **The entire `## What this file is NOT` section** (CLAUDE.md lines 74–79 plus any preceding blank line). The section's content adds no current value and actively misleads.
- **No other text in the file.** A pre-flight `grep -n "Issue #1\|stub\|later issues" CLAUDE.md` confirms the deletion is bounded to that single block — no scattered "stub" references elsewhere.

### What gets preserved byte-identical

The four substantive sections, all currently load-bearing and referenced by skills:

- **`## Project context`** (lines 8–18) — kit positioning, ADR-002 scope, GitHub Flow reference.
- **`## Guiding documents`** (lines 20–33) — recently refreshed pointer-index to `design/adr/`, `docs/repo-structure.md`, `docs/workflow-guide.md`, `docs/skills.md`, `README.md`, `archive/`. Pulls its weight as a slim, current docs index.
- **`## Working rules`** (lines 35–51) — plan-first per ADR-006; scope-to-issue rule; ADR-numbered commit messages; SKILL.md attribution-style guide (added by #85); kit-lightweight rule; "never edit accepted ADRs in place" rule with the ADR-044 mechanical-rewrite exception. All referenced by `/adr-writer`, `/prepare-issue`, `/claude-issue-executor`, `/pr-review-packager`.
- **`## Developing the kit on itself (dogfooding)`** (lines 53–72) — the `link-skills` bootstrap step. Real foot-gun protection. Entry #3 of `refactoring-ideas.md` (ship `link-skills` in-kit) may eventually obviate this section, but until that lands the current pointer to `~/dotfiles/...` is correct.

### Open question resolutions (from entry #4)

- *Keep the "Guiding documents" section, or move that index to a separate doc?* **Keep.** It's a slim list of pointers, not duplicated content, and CLAUDE.md is the natural orientation surface. Moving it to a separate doc would just add a hop without saving meaningful tokens.
- *How much should CLAUDE.md duplicate vs reference `workflow-guide.md` and `skills.md`?* **Reference, don't duplicate.** Current shape already follows this — the `Working rules` section states the rule; the procedural detail lives in `docs/workflow-guide.md` and the skill SKILL.md files. No reshape needed.

## Tasks

- [ ] Delete the `## What this file is NOT` section (lines 74–79 plus the preceding blank line at line 73).
- [ ] Run `grep -n "Issue #1\|stub\|later issues\|What this file is NOT" CLAUDE.md` and confirm zero hits remaining.
- [ ] `git diff CLAUDE.md` and verify the diff contains **only deletions** — no inadvertent edits to the four preserved sections.
- [ ] Smoke check the rule references: skills that read `CLAUDE.md` as context (`/prepare-issue`, `/claude-issue-executor`, `/adr-writer`, `/pr-review-packager`) still find what they expect — plan-first per ADR-006, the "never edit accepted ADRs" rule, the SKILL.md style guideline.
- [ ] Move `notes/refactoring-ideas.md` entry #4 from **Unfiled** to **Filed** with this issue's number.

## Acceptance criteria

- `grep -n "Issue #1\|stub\|later issues\|What this file is NOT" CLAUDE.md` returns zero hits.
- `CLAUDE.md` is exactly 73 lines (down from 80) after the deletion.
- `git diff CLAUDE.md` shows only the lines 73–79 block deleted — zero hunks elsewhere in the file.
- All four preserved sections (`## Project context`, `## Guiding documents`, `## Working rules`, `## Developing the kit on itself (dogfooding)`) render byte-identical to pre-refactor.
- No skill behaviour change. Smoke check: `/prepare-issue`, `/claude-issue-executor` still run end-to-end.
- The PR body cross-references `notes/refactoring-ideas.md` entry #4.

## Scope and constraints

- **Single-file edit.** Only `CLAUDE.md` in the kit root.
- **Cosmetic / framing only.** Zero rule changes. Zero behaviour changes.
- **Plan-first per ADR-006 still applies** but the change is trivial — a one-paragraph plan listing the section to delete + the grep + diff verification is sufficient.
- **No new tooling.** The grep / diff checks are one-liners.
- **No ADR.** Same reasoning as #89 and #91 — internal framing only, no target-project convention shift.

## Out of scope

- Refreshing `templates/claude-md-template.md` (target-project CLAUDE.md). Different artefact, different intake, separate decision.
- Shipping `link-skills` inside the kit (refactoring-ideas entry #3). The Dogfooding section's current pointer to `~/dotfiles/...` stays correct until entry #3 is filed and shipped.
- Token-budget instrumentation for CLAUDE.md (refactoring-ideas entry #10). This is a one-time framing refresh, not a sustained budget regime.
- Restructuring section ordering. Adding new rules. Renaming sections.

## Notes

Labels: `docs`, plus `tech-debt` if that label exists.
Milestone: open — assign at filing.

References:

- `notes/refactoring-ideas.md` entry #4 (origin)
- Sibling shipped cleanups in the same shape: #89 (`docs/` slice — PR #90), #91 (`examples/` slice — PR #92). `CLAUDE.md` is the third surface where post-MVP framing went stale; this is the kit-root slice.
