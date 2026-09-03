---
name: dont-stop
description: Use when an authorized implementation, fix, build, workflow, UI, data, integration, or release task is multi-phase, long-running, likely to cross context compaction, resume later, touch external state, or require autonomous repair. Do not use for exploration-only, plan-only, review-only, diagnosis-only, status, or explanation requests that do not authorize changes.
---

# Don't Stop

Drive an authorized change to a verified outcome. Do not make the user the
first-line tester for defects that can be found and repaired locally.

**Completion invariant:** “Don't stop” means do not abandon recoverable work;
it does not mean restart completed work or retry an unchanged action forever.
Progress requires a new state, new evidence, or a changed hypothesis.

## Follow the operating contract

- Work directly in the active session unless the user explicitly requests
  delegation or another applicable instruction requires it.
- Treat this skill as the outer completion loop. Use more specialized skills
  for implementation, debugging, testing, documents, releases, or UI control
  when they apply.
- Inspect current project and runtime truth before changing anything.
- Keep implementation, verification, repair, and delivery in the same task.
- For any multi-phase, long-running, context-compaction-prone, or externally
  affecting task, maintain a compact durable checkpoint; do not use commentary
  as the only record of progress.
- Treat checkpoint state and evidence as the source of truth for resuming.
- Continue through recoverable failures instead of handing the first failure
  back to the user.
- Preserve unrelated worktree changes and existing user data.
- Do not broaden authorization. A request to implement does not authorize a
  production publish, destructive migration, payment, live submission, or
  external message unless the user included that action.

## 0. Persist and resume task state

Create a checkpoint before the first expensive action when the task has more
than one phase, may be compacted, or can affect external state. Prefer a
first-class plan/state that survives compaction (for example, `update_plan`).
If that persistence is not guaranteed, use a small non-deliverable workspace
checkpoint such as `.codex-tmp/dont-stop/<task-id>/checkpoint.json` or `work/`.
Never put secrets or giant raw outputs in it, and never stage it as a product
change unless the user explicitly requests that.

The checkpoint must contain:

- objective, scope, authorization boundary, and explicit non-goals;
- stable step and acceptance-criterion IDs with states:
  `pending`, `in_progress`, `verified`, `failed`, `unknown`, `superseded`, or
  `blocked`;
- the current step, the single next action, and evidence pointers/results;
- completed actions with an operation key, inputs or source fingerprint, and
  outcome;
- failed actions with the changed hypothesis required for a retry;
- in-flight or unknown external operations, request IDs, and pre/post-snapshot
  pointers when applicable;
- a no-repeat list and the current worktree/runtime baseline.

After context compaction or when inheriting a long task:

1. Read the checkpoint and current plan first. Do not restart from the
   original prompt or repeat the first step merely because context was lost.
2. Reconcile only the current step with targeted current truth. Read an
   immutable document or rerun a successful probe only if its source, inputs,
   or freshness requirement changed. Read a selected skill once per task;
   after compaction, use the checkpoint unless a new skill is selected or its
   source changed.
3. If the checkpoint is missing or contradictory, perform one bounded
   inventory, record the result, and then resume; do not repeatedly rediscover
   the whole task.
4. When the user changes scope, append or revise the affected step while
   preserving verified steps and their evidence. Do not reset the whole plan.
5. Update the checkpoint after each material change, verification gate,
   external request, or newly discovered blocker, before starting the next
   expensive action.

### Action-state gate

Use an operation key such as `phase | target | operation | input-hash` before
every expensive read, write, test, or deployment action:

| Recorded state | Required next action |
| --- | --- |
| `verified` | Reuse the evidence; rerun only if an input or dependency changed. |
| `failed` | Diagnose and change the hypothesis or input before retrying. |
| `unknown` | Inspect logs, operation status, or readback before resending. |
| `in_progress` | Check whether the original operation is still running. |
| `blocked` | Complete safe independent work, then report the blocker. |

For external writes, change one variable per probe, save the pre-state first,
and record the operation/request ID if available. Classify a timeout,
interruption, or missing response as `unknown`, not `failed`; a transport or
business acceptance response is still `in_progress` until required readback
passes. Read back before retrying. Never blindly resend an operation whose
request may already have reached the provider.

Example: a provider returns HTTP 200 but the response is lost before the
readback. Keep the operation `unknown`, query logs/resource state, and only
then decide whether a changed request is safe.

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
6. Give each step and acceptance criterion a stable ID, set the initial
   checkpoint, and record positive as well as negative constraints (for
   example, “must not resend” or “must not publish”).

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
6. Record exact commands or actions and their outcomes in the checkpoint as
   they occur. Never claim a test, build, runtime flow, publish, or readback
   that was not completed.

After each verification gate, mark the relevant criterion and evidence before
moving to the next gate. Do not rerun a passed gate solely because the context
was compacted; rerun it when its inputs, dependencies, or required freshness
changed.

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
7. Repeat until the applicable gates pass or a genuine blocker remains. A
   retry is valid only when it has a changed implementation, input, hypothesis,
   or newly relevant evidence; an identical retry is not progress.

Do not hide failures, silently skip gates, or label a failing result
"non-blocking" without evidence. If a failure appears pre-existing or unrelated,
verify that distinction with baseline evidence where practical, leave unrelated
code untouched, and report it separately.

Record the failed check and next hypothesis before repairing it. If the repair
or verification changes no state and produces no new evidence, return to the
action-state gate instead of expanding the search or repeating the same probe.

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
- Mark the checkpoint complete only after every applicable criterion has current
  evidence and no operation is left `in_progress` or `unknown`.

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

## Prevent endless loops

The following are red flags that the task is being reinitialized rather than
continued:

- rereading all skills, handoffs, or immutable source files after every
  compaction;
- repeating a page/API probe whose inputs and result are already recorded;
- treating “no response” as proof that an external write did not happen;
- retrying the same failed operation without a changed hypothesis;
- saying “continue from the previous state” without naming the current step,
  evidence, and next action;
- interpreting “don't stop” as permission to ignore completion, scope, or a
  no-progress blocker.

When the same operation key has the same inputs and outcome twice, do not make
a third identical attempt. Either change the hypothesis/input, wait for a
defined external state transition, or classify the issue as a blocker with the
evidence already collected.

## Handle genuine blockers

Pause only when progress requires user authentication or 2FA, unavailable
credentials or source data, inaccessible hardware or services, a material
product decision, a destructive action, a production side effect, a
deterministic no-progress condition after the circuit breaker, or other
authority the user has not granted.

Before pausing:

- Complete every safe and independent part.
- Try reasonable non-destructive alternatives.
- Report the exact blocker, the evidence, what is already complete, and the
  single action or decision needed from the user.
- Preserve the checkpoint with the current step, attempted operation keys, and
  the exact state needed to resume without repeating completed work.
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

Before handoff, include the checkpoint's current step, completed criteria, open
blockers, and next action so a later continuation can resume directly.

Keep the report concise, but never replace evidence with "should work".
