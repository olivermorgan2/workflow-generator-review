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

- #87 — none — bring 4 over-budget SKILL.md files under L2 budget via sidecars (#84 Phase 2)
- #86 — none — rewrite 19 SKILL.md descriptions to canonical Use-when shape (#84 Phase 1)
- #85 — none — prune type-3 ADR attributions across 17 SKILL.md files
- #82 — ADR-045 — rename Design/ → design/ kit-wide for root-directory casing consistency
- #81 — ADR-044 — accept ADR-044 mechanical-rewrite immutability exception

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

PR #87 merged (squash `d76eb05`); Phase 2 of issue #84 shipped. All 19 cohort skills now under both 500L and 5k-token thresholds. Issue #84 stays open for Phase 3 — the only remaining phase, smallest of the three. **Phase 3 scope:** rename `skills/prd-normalizer/examples.md` → `example.md` (cohort uses singular; one drift), and decide cohort policy on the two skills currently with no sidecar (`complete-milestone`, `milestone-summary`) — either add `example.md` to each (matches 17/19 default) or document in `docs/skills.md` why they're orchestration-only. Voice/structure-only; small docs/file-rename PR. To start: `/prepare-issue 84` and brief executor for Phase 3 only.

<!-- state:continue-here:end -->
