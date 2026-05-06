# Working notes

Scratch, ideation, and triage files used while building the kit itself.
These are **kit-repo-only** — they are not copied into target projects.

Contents:

- `bug-fixes.md` — triage holding pen for bugs found during dev / eval /
  dogfooding. Entries graduate to GitHub issues.
- `feature-ideas.md` — backlog of feature ideas captured for later batching.
- `eval-issue-<n>.md` — post-issue evaluation reports from
  `/claude-issue-executor` sessions.
- `archive/phase-1/` — archived phase-1 build artefacts: per-issue prompts,
  issue bodies, and one-off GitHub-setup prompts. Retained for browseable
  history; the current per-issue convention is `prompts/issue-NNN-*.md`
  (see ADR-006).

The reusable Claude Code session prompt is at
[`issue-prompt.md`](issue-prompt.md), with a worked example at
[`issue-prompt-sample.md`](issue-prompt-sample.md). See
[`docs/issue-prompt-guide.md`](../docs/issue-prompt-guide.md) for how
to fill it and what the end-of-session evaluation summary must contain.
