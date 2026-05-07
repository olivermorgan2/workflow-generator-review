# Claude Code Workflow Kit — State

**Last updated:** 2026-05-08
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** none
- **Prompt:** n/a
- **Branch:** n/a
- **Status:** none

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #88 — none — unify example.md naming and document orchestration-only skills (#84 Phase 3 — closes #84)
- #87 — none — bring 4 over-budget SKILL.md files under L2 budget via sidecars (#84 Phase 2)
- #86 — none — rewrite 19 SKILL.md descriptions to canonical Use-when shape (#84 Phase 1)
- #85 — none — prune type-3 ADR attributions across 17 SKILL.md files
- #82 — ADR-045 — rename Design/ → design/ kit-wide for root-directory casing consistency

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

PR #88 merged (squash `4420a2c`); Phase 3 of issue #84 shipped, **issue #84 closed**. All three phases done: #86 (descriptions), #87 (body slimming), #88 (sidecar consistency). 17/17 sidecar-bearing skills use the singular `example.md`; the no-sidecar pair (`complete-milestone`, `milestone-summary`) is documented as orchestration-only in `docs/skills.md` §5. `notes/refactoring-ideas.md` entry #9 moved from filed → fully shipped. **No in-flight work.** Pick the next item from `notes/refactoring-ideas.md` (open entries: #1, #3, #4, #5, #6, #8, #10, #11) when ready, or capture new ideas as they arise.

<!-- state:continue-here:end -->
