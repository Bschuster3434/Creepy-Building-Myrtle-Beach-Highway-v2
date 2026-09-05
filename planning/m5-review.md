# M5 — Complete interactive walkthrough

**Current status: Done, accepted by Brian on September 5, 2026.** After reviewing the revised no-click trackpad orbit and keyboard controls, Brian requested committing and pushing the work to `main` and closing M5. The review gate is satisfied by his explicit approval. Latest verification: production build, 16 Node tests, and 82 control checks in each of Chrome and Edge pass.

The latest control revision makes 2 immediately activate orbit: horizontal trackpad scrolling rotates without clicking; vertical scrolling zooms. A/D or Left/Right orbit continuously; W/S or Up/Down zoom in/out instead of tilting. Left- and right-button dragging also work. Horizontal orbit direction is reversed from the previous build. Orbit damping eases motion and permits unrestricted horizontal turns. Pressing 1 or clicking Walk immediately requests first-person mouse capture, retaining the walking pose. The single Explore button does the same on entry. Escape releases the cursor; clicking the view resumes. If capture is rejected, an automatic drag fallback keeps the view usable. `controls-review-check.js` / `controls-review-report.json` verify the revised flow in Chrome and Edge. The initial mode suite and performance evidence below describe the earlier implementation.

Brian authorized completion of M5 on September 5, 2026. This milestone delivers the local desktop experience; the separate V2 Vercel project and public deployment remain M6.

## Implementation

The paired front doors retain their accepted behavior. The crate storeroom, packing room and rear doors now each respond independently to aimed click/E, with clear open/close feedback and repeatable animation. All doors start closed. Physics and render poses use the same exported pivot positions, widths and signed angles. Static collision for the formerly held-open leaves is removed; moving collision includes door hardware. A request is rejected if its sweep would cross the walking body. A leaf already moving pauses if the visitor enters its path and resumes once clear, including while the visitor is in an inspection view.

Four independent circuits serve the sales room, crate storeroom, packing room and rear passage. Named switches and bulbs survive material batching. Each circuit updates its point lights, bulb emission and switch feedback without changing other circuits. The third original pendant, behind the room fronts, belongs to the passage circuit. The switches retain the wall-mounted positions accepted during M4.

The approved right entrance pane retains its concealed top hinge and 15-degree inward tilt. A small conservative walking boundary covers the complete animated mesh envelope, including its latch and sash, so the body cannot occupy the pane's opening sweep. The entry and aisle routes remain clear.

Walking, orbit and top-down viewing are exposed through buttons and 1 / 2 / 3. The walking camera remains separate and retains its position/orientation when inspecting the site. Orbit has a fixed building target, bounded distance/elevation and mouse/keyboard rotation and zoom. Top-down uses an orthographic camera with bounded pan and zoom. Inspection input does not move the walking body or operate doors/lights. Both captured mouse look and drag look work; short clicks in drag mode operate the centered object, while dragging only turns the view. Escape explicitly releases capture and clears movement. Field notes documents controls, switch locations and a return-to-apron reset.

## Source and asset inspection

Initial inspection found that M4's rear switches/bulbs had been merged into static geometry and the rear leaf retained frozen open-state collision. `model/walkthrough_data.py`, called before batching by `model/build_full.py`, addresses those requirements. The application changes are in `app/src/world.js`, `physics.js`, `main.jsx` and `style.css`. The authoritative complete Blender source and `complete.glb` / schema-3 `complete.json` were rebuilt together. Geometry and visual composition remain the accepted M4 scene: 298,883 source triangles, 1,623 construction objects and eight fuller trees. There are 110 render meshes and 86 static colliders plus five runtime moving leaves and the pane clearance. The GLB is 13,348,244 bytes, about 16.5 kB larger than M4; conservative texture memory remains 33.33 MiB.

All asset provenance remains unchanged: researched M1/M2 shell and site relationships, approved M3 service-shop composition, inferred exterior fittings and invented rear furnishings/site dressing. No new historical claim or third-party visual asset was introduced. V1 was not changed.

## Verification evidence

Final result: **216 checks pass in each of Chrome and Edge** — 90 interactions, 57 camera/input and 69 reverse-side door access plus continuous-route/performance checks. No runtime errors were reported. The final window-clearance change was followed by both browsers' interaction and route suites; camera/input had already passed with the same camera controls and explicit Escape handler.

The production build and 16 Node tests pass. The tests include open/closed passage in both directions for all four door controls, 101 collision poses per leaf, swing rejection, long-frame substeps, furnishing collision, the complete building/site route and thresholds. A left-room route was adjusted to walk beyond the open door handle's conservative collision envelope before turning down the aisle.

The Blender rebuild passed 100 construction-contact checks. Retained geometry verification passes 320 sampled window/front-door poses, 108 glazing-grid rays and 2,444 saved-mesh wall/floor/backing probes, with no reported intersections, gaps or rear portal obstructions in those samples. Browser animation checks independently compare actual rendered leaf endpoints with their physics endpoints.

The three browser reports and screenshots are in [the review gallery](m5-review/index.html): [interactions](m5-review/interaction-report.json), [camera/input](m5-review/mode-report.json), and [continuous route/performance](m5-review/route-report.json). Each callback runs Chrome and then installed Edge, with only one scene rendering at a time. The interaction suite uses real aimed clicks/E and checks independent light intensities and bulb emission. Camera tests cover rejected pointer capture, drag fallback, explicit Escape, focus changes, editable fields, repeated transitions and preservation of the walking pose. The route suite verifies door use from both sides and walks one continuous path through every room, rear exit, both side paths and back inside. Only orientation is set between continuous route segments; movement uses keyboard input from the actual prior position.

The explicit Escape handler resolves a regression-test failure where a simulated Escape key did not cause the browser to release pointer capture on its own. The final interaction pass also verifies that approaching the operable pane stops the body before its full opening envelope.

## Performance and limits

| Final measurement | Chrome | Edge | Accepted baseline |
| --- | ---: | ---: | ---: |
| Navigation to ready | 5.01 s | 5.14 s | Approximately 5.5 s |
| Transfer through ready | 13.78 MB | 13.78 MB | ≤15 MB |
| Walking p95, all circuits on | 12.2 ms | 18.2 ms | ≤20 ms |
| Browser checks | 216/216 | 216/216 | All pass |

Final measured values are recorded in `m5-review/route-report.json` and displayed by the gallery. Conditions are production preview, desktop keyboard/mouse, Chrome/Edge at 1920 × 1080 and DPR 1, 25 Mbps down / 5 Mbps up / 40 ms latency with cache disabled for cold loading. All four lighting circuits are on during the continuous walking profile. Accepted limits are p95 frame interval ≤20 ms, transfer ≤15 MB, approximately 5.5 seconds ready, ≤350 draw calls, ≤750k triangles and ≤256 MiB estimated textures. Loading is a quality measure rather than a rigid cutoff when interaction is smooth.

These are measurements on the recorded local configuration, not guarantees for every device. Geometry and route sampling do not prove every possible user path is defect-free. Lighting still uses the accepted daylight/bounce approximation with a single shadow-casting sun; room lights are unshadowed. Top-down shows the roof/site, not an interior cutaway. Desktop-only controls, original procedural foliage, Google Fonts with system fallbacks and the Vite chunk-size advisory remain documented characteristics. No Vercel environment was needed or configured for M5.

## M6 handoff

Use [application instructions](../app/README.md), this review and [artifact hashes](m5-review/verification-summary.json) to identify and reproduce the release candidate. Run the Node tests and production build, then the three M5 browser callbacks. Rebuild the model only when source/asset changes require it; the saved complete Blender scene and GLB are already aligned. `planning/build_m5_review.py` rebuilds the gallery from the current reports and hashes source/assets for pickup.

Brian authorized packaging the accepted application, model/generators, assets, review evidence and research into the M5 commit on `main`. M6's next action is to verify that source state from a clean checkout, create the separate V2 Vercel project and verify its deployed URL in Chrome and Edge. Local tool settings, dependencies, caches and generated build output are excluded from version control. M6 remains To Do and the overall project remains In progress until its public-release gates pass.
