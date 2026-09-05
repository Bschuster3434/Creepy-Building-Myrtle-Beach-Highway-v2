# Myrtle Beach Highway Astra v2

Research a real building independently, reconstruct it in a new Blender scene, and deliver a polished React and Three.js walkthrough with a complete furnished interior and working doors, windows, and lights. The intended appearance is realistic, a little abandoned and clearly long unused, clean and not overrun, with an empty chair near the front. Brian confirmed this preference during M2 scoping; it supersedes the earlier well-maintained restoration direction.

## Project records

- [Notion project: brief, milestones, decisions, and session handoff](https://app.notion.com/p/3d1488886d5780e292f4e569963f0155)
- [Existing project to-do list](https://app.notion.com/p/3d1488886d578070b4b9ed62f736d1a8)
- [V2 Google Drive folder](https://drive.google.com/drive/folders/13gJwmiCTufdMq079mPgrfDjDZXm7c3xy)
- [V2 GitHub repository](https://github.com/Bschuster3434/Creepy-Building-Myrtle-Beach-Highway-v2)

Notion is the authoritative project plan and task tracker. This README provides local orientation and a resume point.

## Task ownership and confirmation

The project's existing inline to-do list is the assistant's working list. The assistant creates and maintains tasks, updates their statuses, and records findings and deliverables.

Before creating a new ticket or starting materially different work, present its scope and intended results to Brian and confirm that they describe the right thing to build. Once scope is agreed, proceed without repeating confirmation for routine execution or status updates. Record scope changes and confirm substantive additions.

Size each ticket for one working session, with its component steps as an internal checklist. Do not turn each step into a separate ticket. If a blocker prevents completion, keep the remaining checklist and a precise resume point on the same ticket.

Use the existing GTD task list and link each task to this project. Include the milestone, concrete deliverable, and completion criteria in each task description. Use the existing statuses: To Do, In Progress, Done, and Cancelled. Record blockers, artifact links, and next actions. Mark tasks Done only when the completion criteria are met.

At the end of a work session, maintain a short handoff in Notion and update this README when the local resume point changes. Distinguish confirmed scope from proposals awaiting confirmation.

## Milestones

1. Research and building identification.
2. Architectural layout and blockout.
3. Small playable quality sample.
4. Complete building and environment.
5. Complete interactive walkthrough.
6. Verification and public release.

Detailed scope, dependencies, and completion criteria are in Notion. Delivery dates are deferred. Interior design will be developed collaboratively; target devices and performance budgets will be settled during the playable sample milestone.

## V2 boundaries

- Work in this separate V2 directory, a new Blender file, the V2 repository, and a new Vercel project.
- Preserve all V1 files, source, exports, repositories, and deployments unchanged.
- V1 local reference directory: `C:\Users\brian\Documents\Blender\Creepy Building Myrtle Beach Highway`.
- Treat V1 research and original photos as leads. V1 geometry is not authoritative, and generated imagery is not photographic evidence.
- Independently establish the building identity and geometry. Label conclusions as directly observed, strongly inferred, weakly inferred, or invented.
- Prioritize exterior consistency, architectural plausibility, visual quality, and exploratory interest, in that order.

## Working with Blender headless

Blender is driven without the GUI in this project. The Blender MCP add-on server on port 9876 is not running, and the MCP server's background mode (`execute_blender_code_for_cli`) fails with "Blender executable not found at 'blender'" because `BLENDER_PATH` is not set for the `blender` entry in `~/.claude.json`. The working method is to call the installed executable directly from the shell in background mode, the same way `planning/inspect_v1_layout.py` inspected V1:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --version
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background <file.blend> --python <script.py>
```

Installed versions found: Blender 5.0, 5.1 and 5.2 under `C:\Program Files\Blender Foundation\`. Verified 2026-09-04 with Blender 5.2.1 LTS. To create a new V2 scene, omit the `.blend` argument (Blender starts from the default file) and have the script save with `bpy.ops.wm.save_as_mainfile`. Keep V1 files read-only: never pass a V1 `.blend` to a script that saves.

Optional: set `BLENDER_PATH` in the `env` of the `blender` MCP server in `~/.claude.json` to enable the MCP background tools in future sessions.

## Resume point — 2026-09-04

The six milestones are documented. M1 research has been performed and the dossier published in Notion. No Blender scene or application has been created.

M1 is Done: all five checklist items are complete; the dossier is assembled and the modeling-readiness review is recorded. Brian confirmed the location and supplied recollections. The remaining gaps are documented uncertainties carried forward into architectural planning, not outstanding research requirements.

Current ticket: [M2 — Establish the architectural layout and Blender blockout](https://app.notion.com/p/3d1488886d5781c18428fc814fe8cba4) — To Do. Created at Brian's request; M2 implementation is not started.

1. Inventory original references and V1 research leads — source inventory distinguishing real photos, generated imagery, and prior outputs.
2. Identify and corroborate the building and address — sourced identification with matching evidence and remaining uncertainty.
3. Gather and date exterior and site evidence — annotated views, maps, site context, and relevant history.
4. Create the architectural evidence and uncertainty register — classified conclusions, missing views, uncertain dimensions, and interior constraints.
5. Assemble the research dossier and review modeling readiness — consolidated findings and decisions needed before blockout.

Research dossier: [M1 Research Dossier — 4397 Hwy 9 W](https://app.notion.com/p/3d1488886d5781839b10f5576dfe98e5).

The building and location are confirmed by Brian as **4397 Hwy 9 W**, Loris area, South Carolina, approximately **34.007932, -78.764340**. County GIS calls the address **4397 HWY 9 E**; retain both labels and use coordinates. A state survey probably identifies it as an unnamed circa-1940 store. New aerial metadata reports October 30, 2025, and the best securely dated ground screenshots show November 2025. The old GIS footprint is about 7.35 × 15.3 m, a provisional mapped envelope rather than measured wall dimensions.

Brian recalls a centered rear door, flat ceiling, lower rear elevation and Century Farm produce-store use. Treat these as recollections rather than verified photographic details. Nearby Bellamy Farms is corroborated as a Century Farm and produce market; its exact historical connection to the target store is still unverified. Brian has no additional real photographs or measurements beyond Google Maps. One clarification remains pending: whether upper walls coming down meant stepped parapets toward the rear or collapse over time.

Local research artifacts:

- [Annotated reference board](research/reference-board.html), with date filters and unchanged photographic references.
- [Dossier snapshot](research/dossier.notion.md), [user recollections](research/user-recollections.md), and [site schematic](research/site-context.svg).
- [Source inventory](research/source-inventory.csv): 28 classified local files with SHA-256 hashes. Detailed CSV remains local; grouped source inventory is in Notion.
- `research/sources/`: saved county address/parcel/footprint JSON and Esri acquisition metadata.
- `research/references/`: nine unchanged Google reference copies and aerial/board screenshots.

Validation: all 28 original reference hashes and nine copied-photo hashes match; all 11 board images load; date filtering shows four explicitly dated ground views. V1 files were not modified. Rebuild the local board/schematic with `python research/build_reference_board.py`.

M2 and M3 have now been scoped as a proposal in the Notion project, with a [local proposal snapshot](planning/m2-m3-scope.md). M2 establishes the whole-building layout and Blender blockout using Brian's V1 imagined layout reference, including the empty front-right chair behind a counter and the two rear storerooms. M3 finishes the representative front room and adjoining storefront as a playable browser quality sample, carrying the confirmed long-unused atmosphere into materials and furnishings. Exact room dimensions, furniture details and the operable-window solution remain to be developed. The M2 ticket is now created as To Do; no M2 implementation or M3 ticket has started.

Next action: leave M2 To Do until Brian asks to begin implementation. The [M3 stub](https://app.notion.com/p/3d1488886d57812f82abeb392ee5a101) is also created as To Do, dependent on M2. Refine its sample boundary, checklist and performance budgets after M2 review. Neither milestone has started.

Brian has authorized V1's imagined interior as the M2 layout reference. The saved Blender scene has an open front shop and two rear storerooms flanking a central passage to the rear exit. His chair/counter placement is just inside the front entrance on the right, chair behind counter. Those furnishings were not found in the saved scene; their placement is user-specified. See the [V1 layout review](planning/v1-layout-review.md) and [entry cutaway](planning/v1-inspection/v1-entry-cutaway.png). The older Phase 1C YAML differs from the saved scene. Refit this arrangement to V2's researched shell; V1 remained unchanged.

When resuming, read the latest Notion project and its linked tasks before relying on this snapshot. Check for confirmation already given in the conversation or task records; do not ask again for scope already authorized.
