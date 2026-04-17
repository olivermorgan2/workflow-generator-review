# Skills

This directory holds the **source** of the Claude Code skills that make up the
workflow kit. Each skill lives in its own subdirectory with a `SKILL.md` file.

When a user installs the kit into a new target project, the contents of this
directory are copied into that project's `.claude/skills/` so the skills run
project-locally (see ADR-001).

## Planned skills

| Skill | Purpose | Added in |
|---|---|---|
| [`idea-to-prd/`](idea-to-prd/SKILL.md) | Turn a rough idea into a lightweight PRD | Issue #5 |
| [`prd-normalizer/`](prd-normalizer/SKILL.md) | Normalize standard or custom PRDs into one internal format | Issue #6 |
| [`prd-to-mvp/`](prd-to-mvp/SKILL.md) | Scope a PRD down to an MVP statement | Issue #7 |
| [`adr-writer/`](adr-writer/SKILL.md) | Draft ADRs from the MVP and key decisions | Issue #7 |
| `issue-planner/` | Turn MVP + ADRs into a GitHub issue backlog | later |
| [`prepare-issue/`](prepare-issue/SKILL.md) | Auto-fill an issue prompt from a GitHub issue and linked ADRs | Issue #15 |
| [`changelog/`](changelog/SKILL.md) | Generate grouped release notes from git history between two refs | Issue #18 |
| `workflow-docs/` | Generate README, CLAUDE.md, and AI summary | later |
| `claude-issue-executor/` | Plan-first, test-alongside execution for each issue | later |
| `pr-review-packager/` | Package PR summaries and review artifacts | later |

See ADR-001 for why skills live project-locally under `.claude/skills/`.
