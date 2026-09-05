# Myrtle Beach Highway Astra v2

Research a real building independently, reconstruct it in a new Blender scene, and deliver a polished React and Three.js walkthrough with a complete furnished interior and working doors, windows, and lights. The intended appearance is realistic, a little abandoned and clearly long unused, clean and not overrun, with an empty chair near the front. Brian confirmed this preference during M2 scoping; it supersedes the earlier well-maintained restoration direction.

## Project records

- [Notion project: brief, milestones, decisions, and session handoff](https://app.notion.com/p/3d1488886d5780e292f4e569963f0155)
- [Existing project to-do list](https://app.notion.com/p/3d1488886d578070b4b9ed62f736d1a8)
- [V2 Google Drive folder](https://drive.google.com/drive/folders/13gJwmiCTufdMq079mPgrfDjDZXm7c3xy)
- [V2 GitHub repository](https://github.com/Bschuster3434/Creepy-Building-Myrtle-Beach-Highway-v2)

Notion is the authoritative project plan and task tracker. This README provides local orientation and a resume point.

## Vercel deployment

Import this GitHub repository into a new Vercel project. Set **Root Directory** to `app`, select the **Vite** framework, use **Node.js 24.x**, and deploy the `main` production branch. Vercel runs `npm run build` and serves `dist`; no environment variables are currently required.

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

## Resume point — M5 accepted and Done, 2026-09-05

Brian accepted M5 and requested committing and pushing the reviewed work to `main` on September 5, 2026. **M5 is Done.** The accepted control revision makes **2** immediately enable no-click horizontal trackpad scrolling to orbit, vertical scrolling to zoom, A/D or Left/Right to orbit, and W/S or Up/Down to zoom. Left/right dragging also works; horizontal orbit direction is reversed from the previous build. **1** returns directly to first-person mouse-look. Entry has a single Explore button. Escape releases the cursor; one click in the view resumes mouse-look. Drag fallback is automatic only if the browser rejects mouse capture.

The accepted source, assets and evidence are packaged in the M5 commit on `main`. The production build and 16 Node tests pass; the latest control revision passes 82 checks in each of Chrome and Edge (`planning/m5-review/controls-review-report.json`). M6 remains To Do: verify a clean checkout, create the separate V2 Vercel project and verify the public deployment. No deployment is part of this M5 closeout.

## Historical M5 implementation verification — 2026-09-05

**[M5 — Complete the interactive walkthrough](https://app.notion.com/p/3d2488886d5781079825c661301c3c2c)** is complete locally. The accepted M3 baseline and M4 scene are carried forward. All doors and the approved window operate; four independent light circuits serve the sales room, crate storeroom, packing room and rear passage. Collision follows moving doors and reserves the window's opening clearance. Walking, orbit and top-down views have mouse/keyboard controls and preserve the walking position across inspection modes.

**Open [the local walkthrough](http://127.0.0.1:5173/)** while the production preview is running. Use **1 / 2 / 3** for Walk / Orbit / Top-down; click or **E** operates the centered object. All doors start closed. [M5 gallery and evidence](planning/m5-review/index.html) · [Review and release handoff](planning/m5-review.md) · [Controls and rebuild instructions](app/README.md) · [Exact artifact hashes](planning/m5-review/verification-summary.json).

Verification: production build and 16 Node tests pass; Chrome and Edge each pass 216 browser checks (90 interactions, 57 camera/input, 69 reverse-side door access and continuous-route/performance checks). Cold readiness is 5.01/5.14 seconds at 25 Mbps; transfer is 13.78 MB; all-lights-on walking p95 is 12.2/18.2 ms. Geometry retains 100 construction checks, 2,444 saved-mesh probes, 320 window/door poses and 108 glazing-grid rays. The complete GLB is 13.35 MB, with 298,883 source triangles and 33.33 MiB conservative texture memory. These meet the accepted desktop baseline; prior notes below calling that baseline pending are historical.

The authoritative source remains `model/myrtle-beach-v2-complete.blend`; `model/build_full.py` now applies `model/walkthrough_data.py` before batching to preserve circuit and door metadata. The app uses the aligned schema-3 `complete.json` and `complete.glb`. The new model report and verification gallery live in `planning/m5-review/`. M2/M3 source and all V1 files are preserved.

**Next action: [M6 — Verify and publicly release V2](https://app.notion.com/p/3d2488886d57814b90fdd6b8571462e4).** M6 remains To Do. Audit/select the release source state, commit and push the reviewed V2 source/assets, create the separate V2 Vercel project, and verify the deployed URL. M5 needed no Vercel setup and created no public deployment. Application/model/planning/research files were already untracked at pickup; repository release remains M6. The overall project remains In progress until M6 passes. Older handoffs below are historical.

## Historical M4 handoff — 2026-09-04

Brian requested creation and local completion of **[M4 — Complete the building and environment](https://app.notion.com/p/3d2488886d578105935cd7ff2897d3e4)**. The complete scene includes the approved front service shop, furnished crate and packing rooms, finished rear passage/exit, side paths, rear yard, roadway, controlled vegetation, eight branching trees and neighboring agricultural context.

**Open [the local walkthrough](http://127.0.0.1:5173/)** while the production preview server is running. [Visual review and exterior reference pairs](planning/m4-review/index.html) · [Verification and provenance](planning/m4-review.md) · [Application/rebuild instructions](app/README.md).

The authoritative M4 source is [myrtle-beach-v2-complete.blend](model/myrtle-beach-v2-complete.blend), generated by [build_full.py](model/build_full.py) with [full_scene_finish.py](model/full_scene_finish.py). The browser loads separate `complete.glb` / `complete.json` assets. M2/M3 sources and M3 exports are preserved.

September 5 adversarial revision: wall/trim gaps and floating mounts are corrected, right-wall masonry infill is nearly flush, and eight trees have substantially fuller canopies. The pass also corrects crate/trolley contact, utility supports and neighboring siding. [Before/after comparisons](planning/m4-adversarial/index.html) show the changes. Brian approved this revision and explicitly requested closing the ticket on September 5; M4 and its review follow-ups are accepted and closed in Notion.

Verification: nine Node tests, 27 Chrome interaction checks and 13 complete-scene checks in each of Chrome and Edge pass. Geometry passes 100 construction-contact checks, 2,444 saved-mesh probes, 320 entrance poses and 108 glazing-grid checks. GLB: 13.33 MB; source: 298,883 triangles; conservative textures: 33.33 MiB. At 1080p / 25 Mbps, isolated Chrome/Edge loads take 5.04/5.31 seconds with walking p95 intervals of 18.1/18.2 ms. Fuller foliage increases cold loading slightly beyond the provisional five-second target; other resource and frame-time targets pass. Conditions and earlier profiles are in the review.

M4 is complete. M3's visual benchmark remains approved and its device/budget confirmation remains pending; Brian explicitly authorized M4 without revisiting the accepted layout. M5 is next: independent door/light operation and orbit/top-down viewing. Rear and storeroom doors are currently held open; rear fixtures share the sample light circuit. Public release remains M6.

## Historical M3 handoff — 2026-09-04

M1 and M2 are complete. **M3 is In Progress:** Brian requested “start issue M3.” The first playable React/Three.js front-room sample is built and available at [the local preview](http://127.0.0.1:5173/) while its server is running. Brian approved revision 3's layout and atmosphere: “Nope, that feels totally right.” The visual benchmark is accepted; desktop-device budgets remain pending.

Current ticket: [M3 — Build a small playable quality sample](https://app.notion.com/p/3d1488886d57812f82abeb392ee5a101). **Revision 3 responds to Brian's service-shop feedback:** he likes the building and general interior, but the sales room feels too deep. He requested counters within the first 5–10 feet, a produce shop where customers were served, and a quiet, sad mood. The counter now defines about 7 feet of customer depth inside the recessed doors; storeroom fronts move from 8.80 to 5.80 m. The empty front-right chair sits on the serving side. Empty produce bins, an old scale, faded prices and paper bags establish the former use. A clear route around the left end connects to both storerooms and the rear passage. These furnishings and prices are invented. The exterior and M2 source are retained. See [before/after comparisons](planning/m3-review/compare.html), [review captures](planning/m3-review/index.html), [current verification and handoff](planning/m3-review.md), and [application setup](app/README.md). Brian approved this revision as the visual benchmark. M3 remains In Progress only for target-device/budget confirmation.

M3 Notion synchronization: the ticket is In Progress, its implementation checklist is updated, and visual acceptance is checked; target-device/budget confirmation remains unchecked. Automatic approval review rejected appending the detailed handoff because it exports local paths and hardware/performance details. Current detailed reports are saved locally in `planning/m3-review.md`; permission for the earlier export was requested and has not been granted. Revision 3 feedback and results are local. Do not assume the detailed report was uploaded.

M1 is Done: all five checklist items are complete; the dossier is assembled and the modeling-readiness review is recorded. Brian confirmed the location and supplied recollections. The remaining gaps are documented uncertainties carried forward into architectural planning, not outstanding research requirements.

Previous ticket: [M2 - Establish the architectural layout and Blender blockout](https://app.notion.com/p/3d1488886d5781c18428fc814fe8cba4) - Done. All seven checklist items are complete. Brian approved the blockout, the 45-degree entrance correction, and the concealed top-hinged right pane with a 15-degree inward tilt. M3 now implements and tests that operation.

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

Historically, M2 used the authorized V1 imagined layout reference: an open front store, two rear storerooms beside a central passage, and Brian's empty front-right chair behind a counter. The first implementation uses a provisional 7.35 × 15.30 m shell with a 1.50 m passage. M3 implements the full front room and adjoining storefront/canopy/apron; the rear remains blockout context.

Next action: retain revision 3 as the approved visual benchmark. Customer-area depth, service-counter organization, closer storerooms and the quiet produce-shop identity are accepted; do not reopen this review without new feedback. Desktop keyboard/mouse, Chrome/Edge at 1080p, 60 fps, p95 ≤ 20 ms, initial transfer ≤ 15 MB and ready ≤ 5 seconds at 25 Mbps are provisional targets awaiting his response. Keep M3 In Progress until the remaining device/budget decision is settled; visual acceptance is complete.

Brian has authorized V1's imagined interior as the M2 layout reference. The saved Blender scene has an open front shop and two rear storerooms flanking a central passage to the rear exit. His chair/counter placement is just inside the front entrance on the right, chair behind counter. Those furnishings were not found in the saved scene; their placement is user-specified. See the [V1 layout review](planning/v1-layout-review.md) and [entry cutaway](planning/v1-inspection/v1-entry-cutaway.png). The older Phase 1C YAML differs from the saved scene. Refit this arrangement to V2's researched shell; V1 remained unchanged.

When resuming, read the latest Notion project and its linked tasks before relying on this snapshot. Check for confirmation already given in the conversation or task records; do not ask again for scope already authorized.

### M2 generated artifacts

- [Authoritative V2 Blender blockout](model/myrtle-beach-v2-blockout.blend), [build script](model/build_blockout.py), and [provisional parameters](model/blockout-parameters.json).
- [Local review page](planning/m2-review/index.html): original/reference pairs, walking-height views, plan, section, schedules and MP4 walkthrough.
- [Geometry decisions and rebuild instructions](planning/m2-review.md).
- [Circulation check](planning/m2-review/circulation-check.json): sampled 0.50 m diameter route through all rooms, tested against walls, furniture and open leaves. Browser physics and threshold handling remain M3 work.

Blender source saves exterior review state at frame 1. Select the Walkthrough camera for its keyed route; front doors open over frames 28-40 during the approach; Workbench glass hides at frame 41 for interior visibility. Rebuilding overwrites generated V2 files; preserve manual changes separately.

Notion synchronization: M2 is fully updated, its seven checklist items are checked, its status is Done, and its approved review HTML is attached. Automatic approval review separately rejected handoff writes to the project page and M3 page because authorization named the M2 destination. Those two remote pages retain their older handoffs; this local README and M2 are current.

M2 review correction: each entrance return is a single 45-degree pane meeting the door directly. Model, drawings, schedules, images and walkthrough reflect this approved geometry. The right-hand pane will use the explicitly approved concealed top hinge and 15-degree inward tilt in M3.

M2 approval complete: Brian explicitly approved both the window mechanism and uploading the HTML to M2. M3 has since started; its current state and next action are recorded above and in its own Notion task.
