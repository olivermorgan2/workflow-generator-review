# Claude Code Workflow Kit

A GitHub-distributed toolkit of Claude Code skills, templates, and workflow
docs that helps a solo developer or small team set up a GitHub-first software
delivery workflow for a **new** software project. The kit takes a user from a
rough idea, a standard PRD, or a custom PRD to an implementation-ready backlog
of ADRs, GitHub issues, and Claude Code prompts.

## Who this is for

- A solo technical founder, indie hacker, or experienced developer starting a
  **new** project who wants to move fast without reinventing a workflow.
- A small team or consultant that wants a reusable, low-ceremony operating
  system for GitHub-based delivery with Claude Code.

## Who this is **not** for (in v1)

- Anyone trying to retrofit this workflow onto an **existing** repository.
- Teams that need non-GitHub providers (GitLab, Bitbucket) or non-Claude AI
  tooling.
- Anyone looking for a hosted UI or a SaaS product — this is a kit you
  install into your own project.

See [ADR-002](Design/adr/adr-002-new-project-only-scope.md) for why v1 is
new-projects-only and [`docs/install.md`](docs/install.md#what-v1-does-not-support)
for the full list of non-goals.

## At a glance

- **New projects only** — v1 will not adapt existing repos (ADR-002).
- **Project-local install** — each new project gets its own copy of the
  skills under `.claude/skills/`. No global install required (ADR-001).
- **GitHub-first** — issues, labels, milestones, PRs, `main + feature`
  branch model (ADR-004).
- **Plan-first execution** — Claude Code proposes a plan, you approve,
  then it implements (ADR-006).
- **Three starting paths** — rough idea, standard PRD, or custom PRD
  (ADR-003).

## Quick start

1. Install the prerequisites: Git, GitHub CLI (`gh auth login`), and Claude
   Code. Full list and verification commands in
   [`docs/install.md`](docs/install.md#1-prerequisites).
2. Create or clone your new target project:
   `gh repo create my-project --public --clone && cd my-project`
3. Clone this kit once, anywhere outside the target project:
   `git clone git@github.com:olivermorgan2/workflow-generator.git ~/src/workflow-generator`
4. Copy the skills into the target project:
   `mkdir -p .claude/skills && cp -R ~/src/workflow-generator/skills/* .claude/skills/`
5. Commit, then pick a starting path — rough idea, standard PRD, or custom
   PRD — and run the matching skill from inside Claude Code.

Full step-by-step guide: [`docs/install.md`](docs/install.md).

## What is in this repo

| Path | What it is |
|---|---|
| `Design/adr/` | Accepted ADRs that govern the kit |
| `docs/` | Kit documentation |
| `skills/` | Source of the Claude Code skills shipped by the kit |
| `templates/` | Starter templates rendered into target projects |
| `examples/` | Worked examples for the three PRD intake paths |
| `notes/` | Working notes for building the kit |

See [`docs/repo-structure.md`](docs/repo-structure.md) for the full map of
what lives in the kit versus what gets generated inside a target project.

## Status

Early development. Work is tracked in GitHub issues against milestones M1–M4.
