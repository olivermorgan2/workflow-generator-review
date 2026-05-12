You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `docs/workflow-guide.md`.

ADR:
- none — issue is a kit-internal framing refresh. The issue body's `## ADR` section is explicit: "None required. `CLAUDE.md` is the kit's project-rules file. The rules themselves aren't changing — only the framing prose around them. ... The kit-internal `CLAUDE.md` is a different artefact from the target-project template at `templates/claude-md-template.md`, so target projects are unaffected." Plan-first execution per ADR-006 still applies.

GitHub Issue:
- Title: Refresh CLAUDE.md — drop dated stub framing from the kit root
- Number: #93
- Milestone: none
- Labels: none

Goal
Surgical removal of the dated `## What this file is NOT` section (CLAUDE.md lines 74–79) — the "stub added in Issue #1 / later issues" framing — preserving every other section byte-identical. The kit has shipped 70+ issues across four milestones; the load-bearing rules the section deferred to "later issues" already exist in the body.

Why it matters
`CLAUDE.md` is the first file Claude Code reads on every session in this repo, so its content is eager-loaded and pays a token cost on every invocation. The "## What this file is NOT" footer currently tells the LLM that the file is a stub awaiting a fuller version, which is two problems at once: (1) misleading framing — the rules, dogfooding playbook, and SKILL.md style guide all landed long ago; (2) wasted tokens on prose that no longer delivers current information. This pairs with the just-shipped sibling cleanups #89 (`docs/` slice — PR #90) and #91 (`examples/` slice — PR #92): same pattern of post-MVP framing gone stale, now in the kit-root slice with the highest blast radius per token.

Requirements
- Delete the entire `## What this file is NOT` section in `CLAUDE.md` (lines 74–79 plus the preceding blank line at line 73). No other text in the file changes.
- The four preserved sections (`## Project context`, `## Guiding documents`, `## Working rules`, `## Developing the kit on itself (dogfooding)`) must remain byte-identical to pre-refactor — verify via `git diff CLAUDE.md`.
- Pre-flight `grep -n "Issue #1\|stub\|later issues" CLAUDE.md` confirms the deletion is bounded to that single block — no scattered "stub" references elsewhere in the file.

Acceptance criteria
- `grep -n "Issue #1\|stub\|later issues\|What this file is NOT" CLAUDE.md` returns zero hits.
- `wc -l CLAUDE.md` reports exactly 73 lines (down from 80; the 7-line block + 1 blank).
- `git diff CLAUDE.md` shows only the lines 73–79 block deleted — zero hunks elsewhere in the file.
- All four preserved sections render byte-identical to pre-refactor.
- No skill behaviour change. Smoke check: `/prepare-issue`, `/claude-issue-executor`, `/adr-writer`, `/pr-review-packager` still run end-to-end against the trimmed `CLAUDE.md`.
- The PR body cross-references `notes/refactoring-ideas.md` entry #4 (already moved to Filed with this issue number).

Scope and constraints
- Primary folders to touch: kit root (`CLAUDE.md` only).
- Folders to avoid unless absolutely necessary: everything else — `docs/`, `skills/`, `templates/`, `examples/`, `prompts/`, `notes/` (the entry-#4 status update is a separate one-line edit at PR time), `design/`, `bin/`, `archive/`.
- Cosmetic / framing only — zero rule changes, zero behaviour changes. Single-file, ~7-line deletion. One-shot single PR.
- Plan-first per ADR-006 still applies but the change is trivial — a one-paragraph plan listing the section to delete + the grep + diff verification is sufficient.

Evaluation & testing requirements
- After the edit lands, run `grep -n "Issue #1\|stub\|later issues\|What this file is NOT" CLAUDE.md` and confirm zero hits. Paste the command output into the evaluation summary.
- Run `git diff CLAUDE.md` and visually confirm the diff is a single deletion block — no inadvertent edits to the four preserved sections.
- Run `wc -l CLAUDE.md` and confirm 73 lines.
- Smoke read the four preserved sections end-to-end to confirm voice and structure are intact.
- All existing tests must continue to pass (kit has no automated test runner — single-file framing changes covered by the grep / diff / wc checks).
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md` (the file you'll be editing — read the whole thing so you can verify the section boundaries and preserved-section line ranges before the cut)
   - `notes/refactoring-ideas.md` entry #4 (origin, now in Filed section — path-choice and open-question resolutions)
   - The sibling shipped cleanups for context: #89 / PR #90 (`docs/` slice), #91 / PR #92 (`examples/` slice). Same pattern, adjacent surface.
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the exact line range you'll delete (expected: a 7-line block at lines 73–79 plus the preceding blank line — confirm against the live file before the cut),
   - the grep / diff / wc verification commands you'll run after the edit,
   - your verification or test plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the issue (e.g. `docs: drop dated stub framing from CLAUDE.md (#93)`).
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed (paste the grep / diff / wc outputs),
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
