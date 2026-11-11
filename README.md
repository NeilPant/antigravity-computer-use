# Antigravity Computer Use

A plugin for Antigravity App and Antigravity CLI that operates macOS apps and browser pages from chat, including tasks that cross between them. Antigravity owns the conversation and decides what to do. The installed Cua Driver supplies window observations, browser state, and UI actions over its existing stdio MCP server. IDE support is deferred.

**Status.** Phase 1 established end-to-end functionality in a live Antigravity browser task. Phase 2 focuses on speed, reliable browser routing, and clearer recovery when a target cannot be reached. See the [roadmap](docs/ROADMAP.md) and [live test runbook](docs/VALIDATION.md).

## Install once for App and CLI

Requires Antigravity App or interactive `agy`, Python 3, and the standard macOS Cua Driver installation. The earlier offline checks used `agy` 1.5.3 and Cua Driver 0.43.2. Browser validation uses a signed Chromium installation with a disposable Driver-owned profile. If Cua is installed at a different path, update its path in `args` in `plugin/mcp_config.json` before installing.

From the root of your local checkout, run this in Terminal. The CLI installs into Antigravity's shared user plugin directory, `~/.gemini/config/plugins/`, so App and CLI can both use the plugin across projects. If you made an earlier project-scoped copy, remove `.agents/plugins/antigravity-computer-use/` from that project first. [Antigravity plugin installation](https://antigravity.google/docs/plugins/)

```sh
project="$PWD"
agy plugin validate --strict "$project/plugin" &&
  agy plugin install "$project/plugin" &&
  agy plugin list
```

Start a fresh conversation on either surface.

- **App:** Look for **Computer Use** under **Customizations → Installed**. Open the project and select the plugin’s `computer-use` skill from composer autocomplete.
- **CLI:** Run `cd "$project" && agy` and type `/antigravity-computer-use:computer-use` in the interactive prompt.

The expected MCP server name is `antigravity-computer-use_cua-driver`. Try a prompt from the [runbook](docs/VALIDATION.md) with Antigravity's normal permission prompts enabled. To remove the shared installation, use App Customizations or `agy plugin uninstall antigravity-computer-use`.

## Package

- [`plugin/`](plugin/) contains the installable manifest, Cua MCP declaration, `computer-use` skill, and a stdio relay that makes browser binding IDs visible in MCP text output while forwarding other responses.
- [`fixtures/index.html`](fixtures/index.html) supplies the local browser form and one-time transfer token used in testing.
- [`docs/VALIDATION.md`](docs/VALIDATION.md) has the live scenarios and provenance criteria.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) records the evidence, decisions, checkpoint, and next phase.
- [`docs/OPTIMIZATION_PLAN.md`](docs/OPTIMIZATION_PLAN.md) tracks the speed work, implementation status, and remaining browser result-contract investigation.

## Contributing

See the [contribution guide](CONTRIBUTING.md) for how to agree on scope and demonstrate that a change works.

## License

This project is available under the [MIT License](LICENSE).
