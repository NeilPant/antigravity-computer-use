# Antigravity Computer Use

A native Antigravity plugin for operating macOS apps and browser pages from chat, including tasks that cross between them. Antigravity owns the conversation and decides what to do. The installed Cua Driver supplies window observations, browser state, and UI actions over its existing stdio MCP server.

**Status.** Phase 1 is packaged and verified non-interactively. Live Antigravity validation is pending. Start with the [live test runbook](docs/VALIDATION.md) and record results in the [Phase 1 checkpoint](docs/ROADMAP.md).

## Install for one project

Requires Antigravity App with native plugin support, its `agy` CLI for validation, and the standard macOS Cua Driver installation. The candidate was checked against Antigravity App 2.29.0, `agy` 1.5.3, and Cua Driver 0.43.2. Browser validation uses a signed system Chrome installation with a disposable Driver-owned profile. If Cua is installed at a different path, update `command` in `plugin/mcp_config.json` before installing.

In Terminal, run the following. The copy is scoped to this Antigravity project.

```sh
project='/Users/yamato/yamato-samurai-sanctum/samurai-armory/tools/Antigravity Computer Use'
target="$project/.agents/plugins/antigravity-computer-use"
agy plugin validate --strict "$project/plugin" &&
  mkdir -p "$target" &&
  cp -R "$project/plugin/." "$target/"
```

Open the project in Antigravity App and start a fresh conversation. Type `/computer-use` in the composer. The expected MCP server name is `antigravity-computer-use_cua-driver`. Try a prompt from the [runbook](docs/VALIDATION.md) and keep Antigravity's normal permission prompts enabled. To update this copy, rerun the commands and start a new conversation. To remove it, close the test conversation and remove the copied `antigravity-computer-use` directory from `.agents/plugins/`.

For availability across projects, use `agy plugin install "$project/plugin"` instead. Check `agy plugin list` and start a fresh App chat. Disable or uninstall that copy from Antigravity Customizations or with `agy plugin uninstall antigravity-computer-use`. Keep one copy active when validating. [Antigravity plugin installation](https://antigravity.google/docs/plugins/)

## Package

- [`plugin/`](plugin/) contains the installable manifest, Cua MCP declaration, and `/computer-use` skill.
- [`fixtures/index.html`](fixtures/index.html) supplies the local browser form and one-time transfer token used in testing.
- [`docs/VALIDATION.md`](docs/VALIDATION.md) has the live scenarios and provenance criteria.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) records the evidence, decisions, checkpoint, and next phase.
