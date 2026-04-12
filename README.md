# Claude Code Workflow Kit

A GitHub-distributed toolkit of Claude Code skills, templates, and workflow
docs that helps a solo developer or small team set up a GitHub-first software
delivery workflow for a **new** software project. The kit takes a user from a
rough idea, a standard PRD, or a custom PRD to an implementation-ready backlog
of ADRs, GitHub issues, and Claude Code prompts.

> **Scope:** v1 is for **new projects only**. It does not retrofit existing
> repositories. See [ADR-002](Design/adr/adr-002-new-project-only-scope.md).

## How it is installed

The kit uses a **project-local installation model**: each new target project
gets its own copy of the skills under `.claude/skills/`, and the kit's source
is not required after install. Details:

- [`docs/repo-structure.md`](docs/repo-structure.md) — kit vs. target-project layout and what gets copied
- [ADR-001](Design/adr/adr-001-project-local-installation-model.md) — why project-local and not global

A full install guide will be added in Issue #2.

## What is in this repo

| Path | What it is |
|---|---|
| `Design/adr/` | Accepted ADRs that govern the kit |
| `docs/` | Kit documentation |
| `skills/` | Source of the Claude Code skills shipped by the kit |
| `templates/` | Starter templates rendered into target projects |
| `examples/` | Worked examples for the three PRD intake paths |
| `notes/` | Working notes for building the kit |

See [`docs/repo-structure.md`](docs/repo-structure.md) for the full map.

## Status

Early development. Work is tracked in GitHub issues against milestones M1–M4.
