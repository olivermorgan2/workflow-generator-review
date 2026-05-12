# Evaluation — Issue #93 (CLAUDE.md framing refresh)

**Branch:** `claude-md-refresh`
**Commit:** `a1968ae docs: drop dated stub framing from CLAUDE.md (#93)`
**ADR:** none (kit-internal framing refresh — issue body and prompt are explicit; plan-first per ADR-006 still applied)

## What changed

- `CLAUDE.md`: deleted the `## What this file is NOT` section (preceding blank line + heading + blank + 4 prose lines = 7 lines total). All four preserved sections (`## Project context`, `## Guiding documents`, `## Working rules`, `## Developing the kit on itself (dogfooding)`) are byte-identical to pre-refactor.

## Commits

- `a1968ae` — `docs: drop dated stub framing from CLAUDE.md (#93)`

## Verification performed

The kit has no automated test runner; verification is the grep / diff / wc trio from the prompt's acceptance criteria.

```text
$ grep -n "Issue #1\|stub\|later issues\|What this file is NOT" CLAUDE.md
# (no output — exit 1, zero hits)
```

```text
$ wc -l CLAUDE.md
      72 CLAUDE.md
```

```text
$ git diff main -- CLAUDE.md
diff --git a/CLAUDE.md b/CLAUDE.md
index 078a647..e47334e 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -70,10 +70,3 @@ The `link-skills` tool lives in the personal dotfiles repo so it syncs
 across machines; it is intentionally NOT part of the kit. See the
 dogfooding playbook at `~/dotfiles/claude-config/docs/dogfooding-playbook.md`
 for the full methodology (kit dogfooding and app dogfooding).
-
-## What this file is NOT
-
-This file is a stub added in Issue #1 so Claude Code has a minimal rules
-baseline while working on the kit. A fuller `CLAUDE.md` — with commands,
-testing expectations, and review conventions — will be written alongside
-the template work in later issues.
```

Single deletion hunk at lines 73–79. Zero other hunks. Smoke-read of the four preserved sections confirms voice and structure are intact.

Skill smoke check (per the prompt's "no skill behaviour change" acceptance criterion) is implicitly covered: the deleted section described CLAUDE.md as a stub but contained no rules, references, or wiring that any skill consults. The four preserved sections — which carry the load-bearing rules — are byte-identical, so `/prepare-issue`, `/claude-issue-executor`, `/adr-writer`, and `/pr-review-packager` behave identically against the trimmed file.

## Follow-ups

- **Off-by-one in the prompt's acceptance-criteria math.** The prompt projected `wc -l CLAUDE.md` at exactly 73 lines (down from 80). The live file was 79 lines, so after deleting the 7-line block the result is 72, not 73. The deletion itself matches the prompt's intent precisely (lines 73–79 of the original file) — only the projected post-deletion line count is off. No corrective action needed.
- **PR-time edit (out of session scope, per prompt).** `notes/refactoring-ideas.md` entry #4 status line should be flipped from `filed-#93` to `shipped` (or equivalent), referencing the eventual PR number. `/pr-review-packager` or a one-line commit at PR time covers this.

## Commands to reproduce the verification

```bash
git checkout claude-md-refresh
grep -n "Issue #1\|stub\|later issues\|What this file is NOT" CLAUDE.md
wc -l CLAUDE.md
git diff main -- CLAUDE.md
```

## Next step

`/pr-review-packager` to draft the pull request from this branch. The PR body should cross-reference `notes/refactoring-ideas.md` entry #4 per the prompt's acceptance criteria, and the sibling shipped cleanups #89 / PR #90 (`docs/` slice) and #91 / PR #92 (`examples/` slice) for context.
