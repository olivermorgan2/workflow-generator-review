# Claude Code Workflow Kit — State

**Last updated:** 2026-05-07
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

- #86 — none — rewrite 19 SKILL.md descriptions to canonical Use-when shape (#84 Phase 1)
- #85 — none — prune type-3 ADR attributions across 17 SKILL.md files
- #82 — ADR-045 — rename Design/ → design/ kit-wide for root-directory casing consistency
- #81 — ADR-044 — accept ADR-044 mechanical-rewrite immutability exception
- #77 — none — persist eval summary for issue #71

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

PR #86 merged (squash `b74778e`); Phase 1 of issue #84 shipped. Issue #84 stays open for Phase 2 + Phase 3. Audit-harness tracking decision made (commit `aafd34b`): curated subset tracked under `notes/skills-audit-2026-05-07/`, regenerable outputs gitignored, convention documented in the directory README. **Next:** pick Phase 2 (body slimming — bring 4 over-budget skills `claude-issue-executor`/`pr-review-packager`/`release`/`prepare-issue` under 500L/5k tokens via one-level-deep sidecars; higher-leverage) or Phase 3 (sidecar consistency: `examples.md` → `example.md`, `complete-milestone`/`milestone-summary` policy; smallest). Both ship as separate PRs against #84. To start either: `/prepare-issue 84` and brief executor for the chosen phase only. Rich handoff context: `notes/handoff-2026-05-07.md`.

<!-- state:continue-here:end -->
