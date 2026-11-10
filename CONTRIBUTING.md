# Contributing

These expectations apply to human and agent contributors alike.

> Translate engineering effort into practical performance. Theory crafting is useless if you cannot demonstrate it; never leave room to ask why an idea hasn't become working reality.

## Agree on the work

- Start from a maintainer-assigned task or an agreed issue. The [roadmap](docs/ROADMAP.md) describes priorities. Get agreement on the outcome, scope, and acceptance criteria before starting implementation.
- Keep changes within that scope. Bring up unrelated bugs, refactors, and new ideas separately. Ask before expanding the task or changing the architecture.
- Keep Antigravity in charge of the task and build on Cua Driver. Check what the installed tools already provide before adding another layer. Identify the gap that the proposed change will close.

## Demonstrate the result

- For behavior changes, run a reproducible task through the intended Antigravity entry point and verify the result. State the host, versions, tool route, and observed outcome. Label runs through Antigravity's built-in browser, raw Cua Driver, and this plugin separately.
- For performance changes, compare before and after on the same task, with the same model and starting state where possible. Report elapsed time, tool calls, and any relevant waits or retries. Verify that the faster run still delivers the required result.
- Follow the [validation runbook](docs/VALIDATION.md) for applicable checks. Keep evidence shareable by removing private page content, credentials, and personal screenshots from traces. If a live check is blocked, give the exact blocker and steps to reproduce it, and mark that result as unverified.

In the pull request, link the agreed task, state what changed, and include the commands or steps a reviewer can use to reproduce the result.
