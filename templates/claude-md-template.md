<!--
  Template: CLAUDE.md — project rules for Claude Code
  Filled by: the workflow-docs skill, or a human at project bootstrap
  Output in a target project: CLAUDE.md at the repo root
  CLAUDE.md is the single most important file for AI-assisted work in a
  project. Claude Code reads it on every session. Keep it current —
  stale rules create worse output than no rules.
-->

# {{PROJECT_NAME}}

## What this is

{{One paragraph. What the project does, for whom, and roughly how.}}

## Technology stack

- Runtime / language: {{e.g. Node.js 22, TypeScript}}
- Framework: {{e.g. Next.js 15, Django, none}}
- Database / storage: {{e.g. Postgres, SQLite, none yet}}
- Key libraries: {{top 3–5 that a reviewer needs to know about}}

## Conventions

- Module system: {{ESM / CommonJS / N/A}}
- Code style: {{formatter, linter, any explicit rules}}
- Dependency policy: {{how you pin versions; when you upgrade}}
- Secret management: {{where secrets live; how they are loaded}}
- Commit style: {{e.g. conventional commits, or plain prose}}

## Project structure

```
{{PROJECT_NAME}}/
  {{top-level directory tree with one-line descriptions}}
```

See also: `Design/` for ADRs and AI summary, `notes/` for process docs.

## How to run

```bash
{{install command, e.g. npm install}}
{{dev command, e.g. npm run dev}}
{{build command, e.g. npm run build}}
```

## Testing

- Framework: {{e.g. vitest, pytest}}
- Location: {{e.g. test/ mirroring src/}}
- Run: `{{test command}}`
- Coverage expectations: {{e.g. new modules must include unit tests for
  happy path, edge cases, and error handling}}

## Review expectations

- Every change lands via PR linked to a GitHub issue.
- Plan-first execution: propose a plan, wait for approval, then implement.
- Commit messages reference the ADR and issue (e.g. `Add X (ADR-003, #15)`).
- Existing tests must continue to pass on every PR.

## Current phase

{{One short line: what the project is focused on right now. Update
this as the project evolves — it is the first thing Claude Code reads.}}
