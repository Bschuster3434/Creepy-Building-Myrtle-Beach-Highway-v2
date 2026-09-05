# The old store — interactive walkthrough

React / Three.js reconstruction of the approved produce service shop, crate storeroom, packing room, rear passage and immediate roadside environment. M5 provides all required desktop interactions and walking, orbit and top-down modes.

## Run

From this directory, with Node 22.12+ or 24:

```powershell
npm.cmd ci
npm.cmd run dev
```

Production verification:

```powershell
npm.cmd test
npm.cmd run build
npm.cmd run preview -- --port 5173
```

Open http://127.0.0.1:5173/. Vercel setup is unnecessary for local M5 verification. Public deployment and verification of that deployment belong to M6.

## Controls

| View | Mouse | Keyboard |
| --- | --- | --- |
| Walk | Move the mouse to look immediately after Explore or selecting Walk. Click operates the aimed object. Escape releases the cursor; click the view to resume. | W/S forward/back, A/D or left/right arrows sideways, E operates the aimed object. |
| Orbit | Scroll horizontally on the trackpad to orbit without clicking; scroll vertically to zoom. Left or right drag also orbits. Horizontal direction is reversed from the previous build. | Hold A/D or Left/Right to orbit; W/S or Up/Down to zoom in/out. + / − also zoom. |
| Top-down | Left or right drag pans the site; wheel zooms. | Arrow keys pan; + / − zoom. |

Use the bottom buttons or 1 / 2 / 3 to select Walk / Orbit / Top-down. Each mode activates immediately, without a secondary enable button. Returning to Walk restores the walking position/orientation and requests mouse capture from that same click or keypress. A browser that rejects capture gets an automatic left-drag fallback; press 1 to retry capture. Inspection input cannot walk the body or operate objects. Field notes → Return to the apron resets walking safely. Editable controls retain their own keyboard input; focus loss clears held movement. Brian accepted M5 on September 5, 2026; M5 is Done.

Click/E reaches objects within 2.4 m and respects opaque walls and glazing. The front pair retains its paired operation; the crate-room, packing-room and rear doors each operate separately. All doors begin closed. Collision follows each moving leaf and includes rear/interior hardware clearance. Unsafe swings are refused; if the player enters an already moving door's path, the leaf pauses until the player clears. Walk beyond the tip of an open storeroom leaf before turning down its aisle.

The approved 15-degree inward-tilting entrance pane works from either side. Its complete mesh sweep reserves a small walking clearance so the player cannot stand in the opening envelope. The sales-room switch is just inside the entrance on the right. Each storeroom switch is on its front wall; the passage switch is on the right near the rear exit. The four circuits independently update real point lights, bulb emission and switch feedback. The pendant behind the storeroom fronts belongs to the passage circuit.

The orbit camera is bounded to 15–65 m from its fixed building target and stays above ground. Top-down uses an orthographic camera with 0.65–4× zoom and bounded panning. It shows the roof and whole site; it is not a cutaway floor plan. The roadway is scenery beyond the walking boundary. Desktop keyboard/mouse and WebGL 2 are required. Mobile input and day/night mode remain outside the first release.

## Rebuild assets

From the repository root:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python-exit-code 1 --python model/build_full.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python-exit-code 1 --python model/verify_full.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python-exit-code 1 --python model/audit_full.py
```

`build_full.py` reads the M2 blockout and reuses the approved M3 construction recipe, M4 furnishing/site additions and `full_scene_finish.py`. `walkthrough_data.py` preserves switches and bulbs before static batching, associates lighting circuits, removes frozen door colliders, and exports door dimensions and angles from the same pivots used for rendering. It writes `model/myrtle-beach-v2-complete.blend`, packed textures, `app/public/assets/complete.glb`, schema-3 `complete.json`, and M5 asset/inventory reports. Generated complete-scene files are overwritten; preserve manual edits separately. M2/M3 sources and separate sample exports remain available.

GLB uses meters, Y up and -Z toward the rear. Geometry uses Draco with 16-bit positions, 10-bit normals and 14-bit UVs; the local decoder and Apache license live in `public/draco/`. Static meshes are batched by material. Interactive parts retain names and metadata. Browser lights and the mesh-derived window clearance are constructed in `src/world.js`; Blender stores source geometry, daylight and review cameras. Lighting is not baked.

## Browser verification and review

The Node suite covers closed/open travel in both directions, the complete furnished route, moving-leaf collision, swing rejection and thresholds. Playwright callbacks in `planning/m5-review/` run against the production preview with `?qa=1`:

- `interaction-check.js`: repeated aimed click/E controls, independent circuits and bulbs, window clearance, render/physics parity, occlusion, refusal/pausing of unsafe door motion.
- `controls-review-check.js`: direct entry into mouse-look, immediate 2/1 transitions, left/right mouse orbit, smooth unrestricted turns, scrolling, continuously held keys, bounded inspection, capture rejection/recovery and E regression. `mode-check.js` / `mode-report.json` are historical evidence from the pre-review control scheme.
- `route-check.js`: one continuous route through every room, rear exit and both side paths, all circuits enabled; cold-load and frame-time profiles, screenshots and resource checks.

Run each file through the Playwright `browser_run_code_unsafe` tool's `filename` argument. They test Chrome first, navigate it to a blank page, then launch headless installed Edge, avoiding concurrent rendering. Each returns JSON; save it as the corresponding `*-report.json`. Screenshots are written directly into that directory. QA hooks are absent from ordinary URLs. M4 callbacks remain historical; they assume storeroom doors were held open and should not replace M5 tests.

After saving current reports, run `python planning/build_m5_review.py` to rebuild the gallery and artifact hash summary. The retained Blender audits write their original M4 report locations; the review builder copies those current geometry results into M5 evidence.

The accepted baseline is Chrome/Edge desktop keyboard/mouse at 1920 × 1080, p95 frame interval ≤20 ms, initial transfer ≤15 MB, and approximately 5.5 seconds ready at 25 Mbps. Loading is a quality measure rather than a rigid cutoff when interaction is smooth. Full-scene ceilings are 750k triangles, 350 draw calls and 256 MiB estimated texture memory. See [M5 review](../planning/m5-review.md) and [gallery and verification evidence](../planning/m5-review/index.html) for final measurements and limitations.

## Provenance and release handoff

All geometry and textures remain original deterministic procedural work. M1/M2 support the visible shell; rear furnishings, undocumented exterior details and exact site dressing are inferred or invented. M5 changes control metadata and application behavior while retaining the accepted scene and appearance. Draco retains its Apache license; React, Three.js and Vite retain their package licenses. Google Fonts have system fallbacks.

The accepted source/assets are packaged in the M5 commit on main. M6 must verify a clean checkout, create the separate V2 Vercel project, and validate the deployed URL. This M5 closeout does not establish a public deployment. V1 remains preserved.

[M5 Notion ticket](https://app.notion.com/p/3d2488886d5781079825c661301c3c2c) · [M6 release ticket](https://app.notion.com/p/3d2488886d57814b90fdd6b8571462e4)
