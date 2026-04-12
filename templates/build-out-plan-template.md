<!--
  Template: Build-out plan
  Filled by: the prd-to-mvp skill (alongside the MVP statement), or a human
  Output in a target project: Design/build-out-plan.md (recommended)
  The build-out plan sequences the MVP into phases, milestones, and an
  initial issue backlog. It should be lightweight enough to revise
  mid-project and concrete enough to drive GitHub issue creation.
-->

# {{PRODUCT_NAME}} — Build-Out Plan

**Last updated:** {{YYYY-MM-DD}}

## Objective

{{One paragraph: what this build-out plan covers and what it produces
by the end. Link back to the MVP document.}}

## Build strategy

{{Describe the order of work in 4–8 steps. Each step should be an
outcome, not a task. Example:
1. Define repo structure and decisions.
2. Write foundational documentation.
3. Implement core capability A.
4. Implement core capability B.
5. Dry-run on a sample input.
6. Package for release.}}

## Scope

- In scope: {{what this plan commits to delivering}}
- Out of scope: {{what this plan explicitly defers}}
- Assumptions: {{anything the plan depends on — tools, access, prior decisions}}

## Success criteria

The plan is complete when a user can:

1. {{End-to-end outcome 1.}}
2. {{End-to-end outcome 2.}}
3. {{End-to-end outcome 3.}}

## Repository structure

```text
{{PROJECT_NAME}}/
  {{top-level folders with one-line purposes}}
```

## Phases

### Phase 1 — {{NAME}}

- **Goal:** {{one line}}
- **Deliverables:** {{2–4 concrete artifacts}}
- **Exit criteria:** {{how you know the phase is done}}

### Phase 2 — {{NAME}}

- **Goal:** {{one line}}
- **Deliverables:** {{...}}
- **Exit criteria:** {{...}}

<!-- Add Phase 3+ as needed. Keep each phase to one readable block. -->

## Milestone recommendation

| Milestone | Focus |
|---|---|
| {{M1}} | {{what this milestone is for}} |
| {{M2}} | {{...}} |
| {{M3}} | {{...}} |

## Initial issue backlog

### {{Milestone 1}}

- {{Issue title 1}}
- {{Issue title 2}}
- {{Issue title 3}}

### {{Milestone 2}}

- {{Issue title 1}}
- {{Issue title 2}}

<!-- The issue-planner skill (or a human) turns each of these into a
full GitHub issue body using templates/issue-template.md. -->

## Testing strategy

{{How the deliverables are validated — unit tests, integration tests,
dry-run walkthroughs, manual verification. Match this to the nature of
the project; not every project needs every category.}}

## Risks and mitigations

### Risk 1 — {{NAME}}

Mitigation: {{one line}}

### Risk 2 — {{NAME}}

Mitigation: {{one line}}

## Acceptance criteria for this document

This build-out plan is acceptable when it:

- matches the MVP statement,
- sequences work in realistic phases,
- identifies initial ADRs or decisions,
- and produces a practical milestone and issue structure.
