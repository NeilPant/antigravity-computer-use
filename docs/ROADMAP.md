# Roadmap and Phase 1 checkpoint

**Checkpoint — 2026-11-10, plugin v0.1.0.** A live Antigravity run completed a read-only browser task through the plugin, establishing the functional baseline. The plugin targets Antigravity App and CLI through a [shared installation](../README.md). IDE support is deferred.

## Phase 1 decisions

| Question | Evidence and decision |
| --- | --- |
| Where does the agent loop run? | `idea/` puts reasoning, action selection, and verification in Antigravity chat. Antigravity's native plugin format bundles skills and local MCP servers. Use its existing model and tool host. There is no separate agent, SDK dependency, browser service, or custom UI in this candidate. |
| What is the thinnest connection? | Cua documents direct Antigravity MCP registration. The installed binary's help and the tagged Rust implementation agree that `mcp` on macOS proxies stdio to `CuaDriver.app`, which owns the OS permissions. Point the plugin at the standard app-bundle executable. This avoids relying on the GUI's shell `PATH`. |
| What belongs in the skill? | MCP tool metadata exposes individual operations. The Antigravity skill adds task-level targeting, image fallback, browser binding, state verification, session cleanup, and provenance. CLI 1.5.3 autocomplete confirmed the plugin-qualified test entry point `/antigravity-computer-use:computer-use`. |
| Which tool surface ships? | Use the Driver's window and browser primitives directly. Antigravity's `enabledTools` list exposes discovery, capture, verification, common UI actions, bounded Cua steps, and typed browser actions. It leaves Driver management, scripts, clipboard access, recordings, and history out of the normal tool catalog. The list controls exposure in Antigravity. It is not a Cua permission sandbox, and `run_steps` can execute supported nested actions. |
| How is browser execution attributed? | `/browser` is Antigravity's own Chrome DevTools subagent. The plugin independently exposes Cua's typed browser tools and native window controls. The two are separate test lanes. Use a Driver-owned `isolated_new` browser for repeatable plugin tests. The candidate provides no existing-profile launch grant, and Antigravity's tool approval cannot confer one. Cua browser calls do not inherit `/browser` site rules. |
| What would justify an adapter? | A reproducible gap in the native connection or result handling. First test the stock MCP path, then Cua's existing image size and file options when relevant. Keep the minimal package if it passes. Evaluate a compatibility layer only against a failing case that those options cannot solve. |

[Antigravity plugins](https://antigravity.google/docs/build-plugins/) · [Antigravity MCP and tool exposure](https://antigravity.google/docs/mcp/) · [Native `/browser`](https://antigravity.google/docs/commands/browser/) · [Cua with Antigravity](https://cua.ai/docs/cua-driver/guides/gemini) · [Cua Driver 0.43.2 stdio proxy](https://github.com/trycua/cua/blob/cua-driver-rs-v0.43.2/libs/cua-driver/rust/crates/cua-driver/src/proxy.rs) · [Cua browser binding and authorization](https://cua.ai/docs/cua-driver/guides/browsers)

## Verification at handoff

| Check | Status |
| --- | --- |
| `agy plugin validate --strict --json` | Passed with CLI 1.5.3 on the source package and a staged workspace copy in a path with spaces. The loader recognizes one skill and one MCP server. A generic icon is the only note. |
| Cua tool compatibility | The configured macOS executable exists. Cua Driver 0.43.2 advertises all 32 configured tools. The browser preparation, exact binding, window capture, stale token, and session behavior in the runbook use the installed schemas. |
| Local browser fixture | An ephemeral loopback HTTP server returned the fixture with status 200. Non-GUI JavaScript tests exercised literal form submission, unique random transfer tokens, and reset between page contexts. |
| Shared installation and discovery | `agy plugin install` writes to the user plugin directory shared by App and CLI. Confirm discovery in fresh conversations in App 2.29.0 and interactive CLI 1.5.3 during live validation. |
| Live operation | A live Antigravity run completed the browser reading task. It repeatedly used Cua native window snapshots to read page content and spent over 11 minutes on computer use. The runbook tracks coverage of other scenarios separately for App and CLI. |

Use the [validation runbook](VALIDATION.md) to record each live attempt. The key acceptance result is a trace from one Antigravity conversation showing the plugin observe the browser, obtain a fresh value, act on an exact native window, and verify that value at both ends. A separate screenshot-only run tests whether the model has usable pixels.

## Phase 2 — Speed and reliability

- **Give browser work a dedicated route.** Evaluate a browser entry point backed by Cua's typed tools for exact-tab binding, scoped page reads, and tab screenshots. Reuse the same workflow for the browser leg of mixed tasks. Surface attachment failures clearly and keep native window controls available for authorized desktop work.
- **Measure before adding code.** Use the Antigravity and Codex transcripts to compare tool routes, elapsed time, call count, approvals, retries, and result coverage. Repeat the same task in Antigravity with the typed browser route. Use existing Cua mechanisms and tune tool exposure or batching where the trace shows a benefit. Implement a new Cua-backed operation only when a measured gap calls for it.
- **Verify across hosts.** Record App and CLI results separately. Recheck native and mixed workflows as routing changes, and track signed-in browser attachment and Antigravity's built-in `/browser` separately from plugin execution.

## Distribution

- **Marketplace logo & assets.** When ready for cosmetic polish or Marketplace distribution, add a dedicated square logo under `assets/logo.svg` (or `.png`). Per Antigravity & Google Marketplace asset guidance: must be at least 128×128 pixels (square), transparent background, high contrast across both light/dark themes, and roughly 10% empty margin baked in (the UI frame center-crops and adds no padding). Reference via `"logo": "assets/logo.svg"` in `plugin.json` to eliminate the generic icon fallback note in strict validation.
