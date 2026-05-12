# Eval — Issue #91: Repoint examples/*.md references to deleted issue-prompt files

**Branch:** `examples-issue-prompt-cleanup`
**Commit:** `e7dd8e5 docs: repoint examples/*.md issue-prompt refs (#91)`
**Prompt:** `prompts/issue-091-examples-prompt-cleanup.md`
**ADR:** none (docs-cleanup only; identical reasoning to PR #90 / issue #89)

## What changed

**`examples/idea-only-example.md`** (2 edit sites, net −7 lines)
- Step 5 paragraph: replaced the broken `notes/issue-prompt.md` link with
  `prompts/issue-NNN-implement-gpx-parser.md` + parenthetical link to
  `prompts/_template.md`. The "how to fill / sample" guidance previously
  carried by the two `→` follow-up bullets is folded into the parenthetical
  ("its header comment documents how to fill it and what the closing
  evaluation summary must contain"), since `_template.md`'s header (added
  in PR #90) now serves both purposes.
- Deleted the two follow-up bullets that pointed at the deleted
  `notes/issue-prompt-sample.md` and `docs/issue-prompt-guide.md`.
- "What happens next" line 118: replaced inline `notes/issue-prompt.md`
  reference with "copying `prompts/_template.md` to a fresh
  `prompts/issue-NNN-*.md` for each".

**`examples/custom-prd-example.md`** (1 edit site, net −5 lines)
- Step 4 paragraph: replaced broken `notes/issue-prompt.md` link with
  `prompts/issue-NNN-slack-event-subscription.md` (copied from
  `prompts/_template.md`).
- Deleted the 3-line "Template and guide:" follow-up block pointing at
  the two deleted files.

**`examples/standard-prd-example.md`** (1 edit site, net −5 lines)
- Step 4 paragraph: replaced broken `notes/issue-prompt.md` link with
  `prompts/issue-NNN-tag-range-resolution.md` (copied from
  `prompts/_template.md`).
- Deleted the 3-line "Template and guide:" follow-up block.

**`design/state.md`** (in-flight zone)
- `Branch: n/a` → `Branch: examples-issue-prompt-cleanup`
- `Status: prepared` → `Status: verified`

## Commits

- `e7dd8e5` — `docs: repoint examples/*.md issue-prompt refs (#91)` — 4 files
  changed, 15 insertions(+), 22 deletions(-)

## Verification performed

### Acceptance criterion 1: zero hits in `examples/*.md`

```
$ grep -n "issue-prompt" examples/*.md
(no output; exit=1)
```

### Acceptance criterion 2: zero hits in `examples/` for the three deleted paths

```
$ grep -rln "docs/issue-prompt-guide\|notes/issue-prompt\.md\|notes/issue-prompt-sample\.md" --include="*.md" examples/
(no output; exit=1)
```

### Acceptance criterion 3: manual smoke read

Read each rewritten section back end-to-end. All three flow cleanly
into the subsequent `## Final state of design/` heading — no orphaned
bullets, no broken sentence flow at the deletion points. The folded
parenthetical in `idea-only-example.md` preserves the guidance that
used to live in the deleted follow-up bullets without duplicating
content that already lives in `_template.md`'s header.

### Acceptance criterion 4: scope discipline

Only `examples/` (and `design/state.md` per ADR-035 session-continuity)
were touched. No skill, template, doc, prompt, archive, or design changes.
`bin/sync-adr-index` not run (no `design/adr/` files touched).

## Out-of-scope hits in the wider grep (informational)

`grep -rln ... --include="*.md"` from repo root still matches in these
locations — all expected and out-of-scope for this issue:

- `archive/*` — historical record per CLAUDE.md, never edited.
- `notes/issue-draft-examples-broken-refs.md`,
  `notes/issue-draft-legacy-prompt-cleanup.md`,
  `notes/eval-issue-089.md`,
  `notes/refactoring-ideas.md`,
  `notes/bug-fixes.md` — drafts, eval summaries, and idea log
  documenting the broken-refs cleanup; these *should* reference the
  deleted paths as the work item.
- `prompts/issue-091-*.md`, `prompts/issue-089-*.md` — this issue's
  own prompt and the sibling's prompt, both reference the deleted
  files in their scope/rationale sections (correct).
- `design/state.md` — continue-here narrative describes "the
  `examples/*.md` broken refs to the deleted issue-prompt files"
  as the in-flight work.

## Follow-ups

- **`notes/refactoring-ideas.md` entry #12** — mark as `shipped-#92`
  (or whatever PR number this lands as) at PR-merge time. Out of
  scope for this implementation session per the prompt's scope note;
  belongs in the PR body's bookkeeping or a follow-up commit on
  `main` after merge, the same pattern PR #90 used for entry #8.
- **`design/state.md` recent zone** — will be updated by
  `/pr-review-packager` / post-merge bookkeeping, not by this skill
  per ADR-035.

## Commands to reproduce

```bash
# Confirm zero broken refs in examples/
grep -n "issue-prompt" examples/*.md

# Confirm zero hits across examples/ for the three deleted paths
grep -rln "docs/issue-prompt-guide\|notes/issue-prompt\.md\|notes/issue-prompt-sample\.md" \
  --include="*.md" examples/

# Smoke-read the three rewritten sections
sed -n '81,91p'  examples/idea-only-example.md
sed -n '115,118p' examples/idea-only-example.md
sed -n '109,115p' examples/custom-prd-example.md
sed -n '169,175p' examples/standard-prd-example.md

# See the commit
git log -1 --stat e7dd8e5
```

## Next step

Run `/pr-review-packager` to package this branch into a PR against
`main`. The PR body should:

- close issue #91,
- cross-reference `notes/refactoring-ideas.md` entry #12,
- note the sibling pairing with PR #90 / issue #89.
