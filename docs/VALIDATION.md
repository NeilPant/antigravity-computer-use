# Phase 1 validation runbook

Yamato conducts the live tests in Antigravity App and interactive Antigravity CLI. Run preflight and scenarios 1–4 on each surface and record the results separately. Use fresh conversations, synthetic data, and the same chat model across comparable runs. Capture the namespaced tool calls and final observed state before ending each run. A permission denial is a valid diagnostic result. Leave the permission preset and personal browser profiles as they were.

## Prepare

1. Start a loopback fixture server in Terminal. Use the printed port in all prompts. Stop this server with Control-C when finished.

   ```sh
   project='/Users/yamato/yamato-samurai-sanctum/samurai-armory/tools/Antigravity Computer Use'
   /Users/yamato/venv/bin/python3 -m http.server 8765 --bind 127.0.0.1 --directory "$project/fixtures"
   ```

2. For the optional Antigravity baseline, run the next section before installing the plugin. Then install once with `agy plugin install` using the [README](../README.md). Check the shared installation in `agy plugin list` and **Customizations → Installed** in the App. Start fresh conversations on both hosts and check `/computer-use` autocomplete and `/context` for the skill. In the CLI, the interactive `/mcp` manager also shows connection status. Confirm actual execution in each conversation's tool trace. [Antigravity customization discovery](https://antigravity.google/docs/customization-discovery/), [Interactive MCP manager](https://antigravity.google/docs/mcp/#interactive-mcp-manager)
3. Use this plugin preflight prompt. Review any MCP and macOS permission prompts. Cua's Accessibility and Screen Recording grants belong to `CuaDriver.app`.

   > /computer-use Use the plugin MCP server to check its permissions and list only TextEdit windows. Report the server name, the permission status and the window identifiers. Leave application state as it is.

   **Pass:** the trace shows calls to `antigravity-computer-use_cua-driver` and the results are usable. An empty TextEdit list is expected when it has no windows. If discovery works but the driver is unavailable, record the exact failure, then check the installed app path and macOS grants. [Cua Driver permissions](https://cua.ai/docs/cua-driver/guides/permissions)

## Antigravity browser baseline

With the plugin absent or disabled, use the built-in `/browser` command in the App composer or CLI prompt with your usual approved browser setup. Record any remote-debugging requirement. Use a test browser profile if setup is needed.

> /browser Open http://127.0.0.1:8765/. Enter `native-browser-baseline` into Test message and click Submit test message. Verify the displayed result and report it.

**Pass:** the visible result is `Submitted message: native-browser-baseline`, and the trace attributes execution to Antigravity's browser subagent. Record this row as **Antigravity built-in**. [Antigravity browser setup](https://antigravity.google/docs/commands/browser/)

## Plugin scenarios

### 1. Native app and exact target

In TextEdit, open two disposable documents. Save one as `CUA Phase 1 Target.txt` in a scratch folder, and leave the other open as a decoy. Keep Antigravity in front during the run.

> /computer-use Through the TextEdit UI, append `phase-one-native` on a new line in `CUA Phase 1 Target.txt`. Work in the background, leave the other document alone, and verify the exact target's text through a fresh Cua window observation. Leave it open so I can inspect it.

**Pass:** the trace binds the named window before action and verifies it afterward. The target text matches, the decoy stays unchanged, and the native action does not bring TextEdit forward. Save or discard the scratch document yourself after inspection.

### 2. Screenshot perception and a pixel-grounded action

Manually put a fresh random code on its own line in a new TextEdit scratch document named `CUA Phase 1 Vision.txt`. Put the code in the document body only. Leave its window visible and keep the code out of the chat prompt.

> /computer-use Target `CUA Phase 1 Vision.txt` in TextEdit. Read the code using a Cua screenshot with `include_accessibility_tree:false`. Use a window-local pixel click from that screenshot to put the caret just after the code and append `-PIXEL` through the UI. Keep input in the background. After the action, verify the resulting line in a fresh Cua observation and report the original code and final line.

**Pass:** the trace shows screenshot-only observation before the action, the model reports the exact hidden code, and the click uses that window's image coordinates. The fresh result shows the suffix in the correct location. Record whether the model used an inline image, an Antigravity image path, or Cua's `screenshot_out_file` read through Antigravity. Run the default image path first. If it fails, retry with a smaller capture. For a file-based retry, give the agent an explicit writable scratch filename and remove that image after the test. A visible image card alone does not prove model access.

### 3. Browser page through the plugin

> /computer-use I authorize a fresh Cua-owned temporary Chromium profile. Use the plugin's typed browser tools to open http://127.0.0.1:8765/, enter `plugin-browser` into Test message, and click Submit test message. Verify the displayed result from a fresh snapshot before ending your Cua session. Report the browser tool route.

**Pass:** the trace uses the plugin for `browser_prepare`, exact binding, navigation, form actions, and the final browser observation. It shows `Submitted message: plugin-browser` before session cleanup. No existing browser profile is attached. If the typed route fails, record the error as a typed-route result. A separate run using Cua window controls can measure that route independently.

### 4. Browser to native app in one chat request

Create a fresh TextEdit document named `CUA Phase 1 Transfer.txt` with an empty body. Keep the fixture server running.

> /computer-use I authorize a fresh Cua-owned temporary Chromium profile. Open http://127.0.0.1:8765/ with the plugin, click Reveal transfer token, and read the newly displayed token from the live page. Then enter the exact token in `CUA Phase 1 Transfer.txt` through its TextEdit UI. Verify the displayed token on the page and the matching document text, use one Cua session across the two legs, and report both tool routes here. Leave TextEdit open for inspection.

**Pass:** a fresh browser observation contains `Transfer token: ` followed by 16 lowercase hex characters, and a fresh native observation shows the same token. Both legs appear under the plugin namespace in the same chat. The browser session may close after verification.

### 5. Denial, stale state, and interruption

- **Denied action.** Repeat the native scenario with a clean scratch target. Deny the first mutating MCP call. Check that the file stays unchanged and the agent reports the denial without changing routes.
- **Stale state.** In a disposable native window, have the agent take two full AX snapshots of the same target and request one harmless action with a token from the first. Cua should refuse the stale token and leave the window unchanged. Have the agent report the refusal and use a fresh token only after reobservation. If the runtime refuses the deliberate stale-token experiment before a call, record that separately.
- **Interrupted browser.** Stop a chat run after temporary browser preparation. Record any completed actions from the trace. If the browser is still open, ask the agent in the same conversation to end the exact named Cua session. Verify that the disposable browser exits. If the MCP transport has already closed, record whether the browser exits on disconnect or idle expiry. Keep the shared Driver running.

## Record results

Use one row per attempt. Report failures at the boundary where they occur. Examples include plugin discovery, MCP connection, Driver permission, image delivery to the model, browser attachment, action delivery, and state verification.

| Run | Provenance | Host / model | Tool or subagent | Target and mode | Verified state or exact error |
| --- | --- | --- | --- | --- | --- |
| Baseline or scenario number | Antigravity built-in / raw Cua / plugin | App or CLI, version and model | Namespaced call, including nested batch actions | Window or tab, background or foreground | Evidence from fresh observation |

For plugin passes, `/browser`, shell automation, direct file edits, and operator actions cannot stand in for any tested step. Operator setup and inspection are allowed. If troubleshooting requires a raw Cua run, use the same fixture and record it separately. Once the App has connected, the presence of cached tool schemas under `~/.gemini/antigravity/mcp/antigravity-computer-use_cua-driver/` can corroborate server discovery. The chat trace is the evidence of execution.
