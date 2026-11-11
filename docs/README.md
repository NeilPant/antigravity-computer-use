# Documentation guide

The live 0.4.x tests and installed-source review supersede the earlier optimization assumptions. Read these three documents before choosing further performance work:

1. [Persistent runtime design](PERSISTENT_RUNTIME_DESIGN.md): the current proposed architecture, implementation sequence and acceptance gates. Implementation has not started; this is the direction for a future agreed task.
2. [CUA source review](CUA_SOURCE_REVIEW.md): verified mechanisms, qualifications, and the boundary between plugin, Driver and host responsibilities.
3. [0.4.1 validation](VALIDATION_0_4_1.md): the live observations, repairs, successful checks and remaining browsing failures that motivate that direction.

Use the validation record for observed behavior, the source review for established mechanisms, and the design for proposed behavior. A design target is not a measured result. Earlier plans do not override these documents.

## Current understanding

- The 0.4.1 repairs address real transport, startup, coverage and input problems. The full public browsing task still failed; general browsing efficiency is unresolved.
- `browser_flow` retains a binding and snapshot and batches a fixed set of operations. The proposed persistent JS environment adds programmable control flow, retained values and selected observations across calls.
- Driver already supplies native diffs and browser observations combining accessibility, DOM, layout and viewport information. A new execution runtime does not inherently require a Driver fork.
- Whether existing browser formats preserve the required catalog text/link relationships remains untested on the actual catalog. The previous DOM probe happened inside the discussion.
- Direct image delivery to Gemini vision remains a host integration gate. Producing a screenshot or displaying an image card does not prove model perception.
- The recordings and diagnostics do not establish a controlled speedup ratio. Compare performance after equal task coverage passes.

## Supporting and historical documents

| Document | Role |
| --- | --- |
| [Roadmap](ROADMAP.md) | Current direction and readiness to begin; summarizes the three primary documents. |
| [Browser flow](BROWSER_FLOW.md) | Existing 0.4.1 mechanism and manual checks; not the future execution architecture. |
| [Validation runbook](VALIDATION.md) | Reusable functional scenarios and provenance rules. Runtime acceptance is defined in the persistent runtime design. |
| [Optimization plan](OPTIMIZATION_PLAN.md) | Superseded historical investigation. Version claims, package tables and recommendations describe earlier candidates, not the current implementation or next task. |

The former speed plan was removed. Earlier roadmap versions remain in Git history. Keep historical observations attributed to their original candidates rather than presenting them as current instructions.
