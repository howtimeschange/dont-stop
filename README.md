# Don't Stop

[English](README.md) | [简体中文](README.zh-CN.md)

An autonomous completion-loop skill for Codex and compatible agent-skill
runtimes:

> Implement → Test → Fix → Re-test → Self-review → Deliver with evidence

`dont-stop` keeps an authorized implementation task moving through recoverable
failures until the requested outcome is actually verified. It prevents the
common failure mode where an agent writes code, runs one check, and hands the
remaining debugging or validation back to the user.

## What it enforces

- Inspect the real repository, worktree, instructions, specifications, tests,
  and runtime state before changing anything.
- Convert the request into observable acceptance criteria.
- Implement the smallest coherent change that satisfies those criteria.
- Run focused checks first, then broader regression, build, packaging, render,
  export, or live-surface verification when applicable.
- Diagnose and repair failures, add regression coverage where practical, and
  re-run affected checks.
- Perform a final diff, runtime, artifact, security, and scope review.
- Deliver only with concrete verification evidence.

The skill treats unit tests as necessary but not always sufficient. UI,
integration, browser, provider, exported-artifact, packaged-app, and release
work should be verified on the strongest practical surface.

## When to use it

Use the skill for implementation requests such as:

- Build or complete a feature.
- Fix a defect and verify the regression.
- Continue an unfinished development task.
- Implement an integration, workflow, script, UI, or data artifact.
- Finish a change, test it, repair discovered problems, and then hand it off.

Typical trigger phrases include:

```text
Implement this, test it yourself, fix any issues you find, and deliver it when it is ready.
改完自己测试，有问题自己修复，确认没问题再交付。
不要停在分析，直接实现并跑通完整流程。
```

Do not use it for exploration-only, planning-only, review-only, diagnosis-only,
status, or explanation requests that do not authorize changes.

## Installation

Clone the repository into the Codex skills directory:

```bash
git clone https://github.com/howtimeschange/dont-stop.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/dont-stop"
```

Restart Codex or begin a new task so the skill catalog refreshes.

To update an existing installation:

```bash
git -C "${CODEX_HOME:-$HOME/.codex}/skills/dont-stop" pull --ff-only
```

## Usage

Invoke it explicitly:

```text
Use $dont-stop to implement this feature and deliver it only after the applicable checks pass.
```

The skill can also be selected implicitly when an implementation request
matches the trigger description in `SKILL.md`.

## Completion loop

1. **Establish the contract** — inspect current truth and define observable
   acceptance criteria.
2. **Implement** — make a complete, scoped change using the project's existing
   conventions.
3. **Verify** — run the applicable static, focused, regression, build, render,
   export, runtime, and readback checks.
4. **Repair** — diagnose failures, fix root causes, add coverage, and re-run
   affected checks.
5. **Self-review** — inspect the final diff, behavior, artifacts, security, and
   unrelated-file boundaries.
6. **Deliver** — report the outcome, evidence, residual limitations, and any
   requested commit, artifact, or release identifiers.

## Safety boundaries

“Don't stop” means continue through safe and recoverable failures. It does not
expand the user's authorization.

The skill does not automatically authorize:

- Production publishing or live submissions
- Destructive migrations or data deletion
- Payments or external messages
- Commits, pushes, releases, or uploads that were not requested
- Bypassing authentication, 2FA, missing credentials, or material product
  decisions

When one of these boundaries blocks progress, the agent should finish every
safe independent step and report the exact action or decision required.

## Repository structure

```text
dont-stop/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── validate.py
├── README.md
└── README.zh-CN.md
```

`SKILL.md` is the runtime instruction source. The README files are human-facing
documentation for the published repository.

## Validation

Run the repository's dependency-free validator:

```bash
python3 scripts/validate.py
```

It checks the frontmatter, required files, naming rules, UI metadata, and
bilingual README links.
