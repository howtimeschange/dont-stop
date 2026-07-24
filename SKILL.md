---
name: dont-stop
description: Close implementation work through a repeatable implement, test, self-repair, re-test, self-review, and evidence-backed delivery loop. Use when the user asks Codex to implement, build, change, fix, complete, or continue a feature, script, workflow, integration, UI, data artifact, or release and expects autonomous completion before handoff, especially with requests such as "先实现", "改完自己测试", "有问题自己修复", "确认没问题再交付", or "不要停在分析". Do not use for exploration-only, plan-only, review-only, diagnosis-only, status, or explanation requests that do not authorize changes.
---

# Don't Stop

Drive an authorized change to a verified outcome. Do not make the user the
first-line tester for defects that can be found and repaired locally.

## Follow the operating contract

- Work directly in the active session unless the user explicitly requests
  delegation or another applicable instruction requires it.
- Treat this skill as the outer completion loop. Use more specialized skills
  for implementation, debugging, testing, documents, releases, or UI control
  when they apply.
- Inspect current project and runtime truth before changing anything.
- Keep implementation, verification, repair, and delivery in the same task.
- Continue through recoverable failures instead of handing the first failure
  back to the user.
- Preserve unrelated worktree changes and existing user data.
- Do not broaden authorization. A request to implement does not authorize a
  production publish, destructive migration, payment, live submission, or
  external message unless the user included that action.

## 1. Establish the completion contract

1. Read the applicable repository instructions, current branch and worktree
   state, relevant specifications, existing tests, and live runtime state.
2. Translate the request into observable acceptance criteria.
3. Identify the changed behavior, its adjacent regression surface, and the
   strongest locally available proof.
4. Separate required outcomes from optional improvements. Avoid unrelated
   refactors.
5. Resolve safe details from the repository and environment. Ask the user only
   when a missing choice would materially change the result or require new
   authority.

## 2. Implement a coherent change

- Implement the smallest complete behavior that satisfies the acceptance
  criteria.
- Follow existing architecture, conventions, and ownership boundaries.
- Add or update regression coverage in the same change when behavior changes.
- Keep credentials and sensitive values out of source, logs, screenshots, and
  delivery notes.
- Do not stop at scaffolding, a proposal, or a partial happy path when the
  requested behavior can be completed.
- Do not weaken assertions, delete coverage, or change acceptance criteria
  merely to make validation pass.

## 3. Run the applicable verification ladder

Start with fast focused checks, then broaden in proportion to risk. Run every
applicable layer:

1. Inspect the diff and run formatting, syntax, lint, type, schema, or
   `diff --check` checks.
2. Run focused tests that exercise the changed behavior and important failure
   paths.
3. Run adjacent or broader regression suites for shared contracts and
   cross-module changes.
4. Build, package, migrate, render, or export when the deliverable depends on
   that operation.
5. Exercise the real user-facing surface when practical:
   - Start the actual local app or service for UI and workflow changes.
   - Verify the interaction and resulting state, not only page load.
   - Read back API, database, file, job, release, or exported-artifact state.
   - Open or render generated documents, spreadsheets, slides, PDFs, images,
     and installers before delivery.
6. Record exact commands or actions and their outcomes. Never claim a test,
   build, runtime flow, publish, or readback that was not completed.

Treat unit tests as necessary but not sufficient when the request concerns a
real interface, integration, packaged app, provider, browser workflow, export,
or release surface.

## 4. Close the repair loop

Whenever a check or real workflow fails:

1. Capture the concrete symptom and reproduce it at the narrowest useful level.
2. Find the root cause instead of patching only the visible symptom.
3. Fix the issue within scope.
4. Add or strengthen a regression test when feasible.
5. Re-run the failed check.
6. Re-run the adjacent and broader checks that could be affected by the fix.
7. Repeat until the applicable gates pass or a genuine blocker remains.

Do not hide failures, silently skip gates, or label a failing result
"non-blocking" without evidence. If a failure appears pre-existing or unrelated,
verify that distinction with baseline evidence where practical, leave unrelated
code untouched, and report it separately.

## 5. Perform a final self-review

Before delivery, inspect the final diff and resulting runtime or artifact:

- Check every acceptance criterion against current evidence.
- Look for missed edge cases, error handling, state transitions, regressions,
  security issues, accidental secrets, debug leftovers, and misleading UI or
  documentation.
- Confirm that tests prove the intended behavior rather than only the
  implementation detail.
- Confirm that generated artifacts open correctly and that externally visible
  state reads back correctly.
- Confirm that unrelated files were not modified, staged, committed, or
  published.
- Run another repair and verification loop for every in-scope issue found.

## 6. Enforce the delivery gate

Deliver only when all applicable statements are true:

- The requested behavior is implemented.
- The acceptance criteria have current evidence.
- Focused tests pass.
- Required regression, build, package, render, or runtime checks pass.
- The real surface was verified, or the handoff clearly states why that layer
  was not applicable or could not be reached.
- No known in-scope blocking defect remains.
- The final diff and worktree state were reviewed.
- Any requested commit, push, release, upload, export, or readback was actually
  completed and verified.

Do not create a commit, push, publish, release, upload, or live submission
unless the user requested it or it is an explicit required step of the
authorized workflow.

## Handle genuine blockers

Pause only when progress requires user authentication or 2FA, unavailable
credentials or source data, inaccessible hardware or services, a material
product decision, a destructive action, a production side effect, or other
authority the user has not granted.

Before pausing:

- Complete every safe and independent part.
- Try reasonable non-destructive alternatives.
- Report the exact blocker, the evidence, what is already complete, and the
  single action or decision needed from the user.
- Never describe the overall task as complete while an applicable delivery
  gate remains unmet.

## Deliver with evidence

Lead with the outcome, then provide:

1. What changed.
2. What was verified, including concrete commands, flows, or readbacks and
   their results.
3. What was self-corrected during validation when it materially affects
   confidence.
4. Any residual limitation or unverified external layer.
5. Requested artifact paths, commit IDs, URLs, or release identifiers.

Keep the report concise, but never replace evidence with "should work".
