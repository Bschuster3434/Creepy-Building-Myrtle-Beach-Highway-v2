# M4 — Complete building and environment

[Notion issue](https://app.notion.com/p/3d2488886d578105935cd7ff2897d3e4) · [Local walkthrough](http://127.0.0.1:5173/)

Status: complete. Brian authorized issue creation and local completion. M3's revision 3 visual benchmark is retained. Device and performance budgets remain provisional; M4 authorization does not change M3's separate pending decision. [Open the visual review](m4-review/index.html).

## User acceptance — September 5, 2026

Brian approved the corrected scene and fuller trees, said “This looks great,” and requested closing the ticket. M4 and its corrective review follow-ups are accepted and closed; the Notion ticket is Done. Recorded loading measurements remain available for later optimization. M5 is the next planned milestone.

## Scope and provenance

The front room retains the approved shallow customer area, service counter, empty front-right chair, produce fixtures and quiet, long-unused mood. The left rear room holds empty crate racks, retained slatted boxes and a tally board. The right room has a packing bench, paper roll, twine spool, sorting trays and hand truck. These are invented interpretations of produce-store use, not verified historical furnishings.

The rear passage, room finishes, cornices, skirting, door hardware, lighting fixtures, rear frame, landing and steps complete the interior and rear access. Room functions and interior finishes are invented. M2's shell, openings, parapets, canopy and chimney remain the researched basis. Vent louvres, guttering, drainpipes, hardware and infill seams are plausible inferred details. Rear landing dimensions are provisional.

The immediate site includes service paths, rear yard, apron joints, the divided highway, grassy median, cut verges, branching broadleaf trees, utility detail and a finished neighboring agricultural building. Road and tree relationships follow M2's contextual layout. Exact positions, species, dimensions, lane markings and neighboring construction are inferred or invented. They are not surveyed boundaries. Vegetation represents late summer / early autumn with limited muted yellowing and clear walking paths.

All added geometry is original deterministic procedural work. Foliage uses individual bent leaf meshes and branch geometry. Existing M3 procedural PBR textures are reused at the same physical scale. No third-party model, texture pack or new photographic evidence was introduced.

## Source and reproduction

From the repository root:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python-exit-code 1 --python model/build_full.py
cd app
npm.cmd test
npm.cmd run build
npm.cmd run preview -- --port 5173
```

`build_full.py` reuses the approved M3 construction recipe before its UV/batching/export stage, extends that unbatched geometry and uses the same finish pipeline. It reads the M2 blockout and writes separate M4 Blender, texture and GLB files. M2/M3 Blender files and M3 exports remain unchanged. The script records individual construction names before combining static geometry by material. Interactive pivot trees remain separate.

Outputs: `model/myrtle-beach-v2-complete.blend`, `app/public/assets/complete.glb`, `complete.json`, and `planning/m4-review/asset-report.json` / `construction-inventory.json`.

The front doors, approved return window and sample light switch remain operational. Rear fixtures share the sample light circuit for inspection; independent room switching and full door controls belong to M5. Rear and storeroom doors are held open so the whole scene can be inspected. The roadway is scenery beyond the walking boundary. Orbit and top-down user modes remain M5 work; public release remains M6.

## Initial M4 verification (superseded by the September 5 revision below)

The production build and all nine Node tests pass. Route checks use a 0.50 m walking body, sampling every 4 cm and checking movement endpoints through both furnished storerooms, out the rear door, down the steps and around the exterior. Existing M3 tests retain the counter and entrance coverage. Retained sample crates were relocated and the route avoids parked open door leaves.

Chrome 152 passes all 27 sample-interaction regression checks. Chrome and Edge 152 each pass 13 complete-scene checks: metadata, rear pivots/fixtures, ten real-keyboard route segments and absence of runtime errors. QA places the camera at each segment start; travel inside segments uses real keyboard input. The final Blender source also passes 320 sampled entrance door/window poses with no intersections and 108 glazing-grid rays with no failures. These are discrete geometric samples, not continuous engineering clearance verification.

Conditions: production preview, Windows Intel Graphics through ANGLE D3D11, headless Chrome/Edge, 1920 × 1080 at DPR 1. Cold loading: cache disabled, 25 Mbps down, 5 Mbps up and 40 ms latency. Each accepted timing run has one scene actively rendering.

| Measurement | Chrome | Edge | Provisional target |
| --- | ---: | ---: | ---: |
| Navigation to ready | 4.04 s | 4.12 s | ≤ 5 s |
| Walking p95 frame interval | 12.2 ms | 18.1 ms | ≤ 20 ms |
| Transfer through ready | 10.89 MB | 10.89 MB | ≤ 15 MB |
| Full-scene checks | 13/13 | 13/13 | All pass |

The final GLB is 10,462,996 bytes. Source geometry has 151,809 triangles, 99 render meshes and 105 collision boxes; 1,549 construction objects are inventoried before batching. Eight branching trees and all four interior spaces are present. The conservative estimate for 25 generated 512² images including unused source images is 33.33 MiB with mipmaps. The browser reports 24 textures including its shadow map. Maximum sampled draw submissions across the retained profiles are 189; rendered triangles peak at 303,222 including shadow passes.

An initial Edge run with Chrome simultaneously rendering recorded p95 42.4 ms. That run is preserved in `edge-concurrent-report.json`; the isolated repeat above resolves the test-condition issue. These measurements establish the tested configuration, not device-wide guarantees. M3 device/budget acceptance remains pending. Vite retains its Three.js chunk-size advisory; measured loading meets the working target.

Evidence: [Chrome regression](m4-review/browser-report.json), [Chrome full scene](m4-review/full-scene-report.json), [Edge full scene](m4-review/edge-report.json), [entrance geometry](m4-review/window-clearance.json), [assets](m4-review/asset-report.json), and [gallery with original exterior reference pairs](m4-review/index.html).

Room-by-room review checks crate storage, packing tools, rear circulation, the retained front room and switched lighting. Front/left/right comparisons retain M2 shell proportions, glazing, canopy, stepped silhouette and chimney. Exact camera matches are not claimed. No public deployment was made. M5 remains the next planned milestone.

### Final material and export pass

`build_full.py` calls `full_scene_finish.py` after batching. That shared pass supplies original asphalt, gravel and bark textures, broader lawn texture scale and smooth branch normals. It can also be reapplied to the saved M4 source without rebuilding geometry. Draco compresses geometry at level 6 with 16-bit positions, 10-bit normals and 14-bit UVs; the authoritative Blender geometry remains uncompressed. The browser loads its decoder locally from `public/draco/`, with Apache license and attribution. [Three.js implementation reference](https://threejs.org/docs/pages/DRACOLoader.html).

The Blender source saves review cameras and daylight; the browser defines its own daylight, bounce and switched lights. Lighting is not baked. Run `model/verify_full.py` with Blender for the entrance checks, then `python planning/build_m4_review.py` to rebuild the gallery. Playwright callbacks in `planning/m4-review/` return their JSON reports and save screenshots. Pause other rendering scene pages before profiling.

### Review follow-up ? sideways controls, September 5

Brian reported being unable to move left/right while reviewing. A browser reproduction showed that clicking Return to the apron left focus on its button, causing the keyboard handler to ignore walking keys. UI buttons now allow movement keys, returning to the apron or clicking the canvas focuses the view, and keyup clears movement even if focus changed. Editable fields retain their own keyboard input. On-screen help explicitly identifies A/D and left/right arrows as sideways movement.

The production build and all 13 targeted browser checks pass: both key pairs, movement after UI clicks, movement relative to a turned view, key release across focus changes, text input protection and mouse capture. See `m4-review/sideways-controls-check.js` and `sideways-controls-report.json`. The request was interpreted as lateral walking; a clarification about turning the view was offered but no reply had arrived during the fix.

### Review follow-up ? mouse looking, September 5

Brian clarified that the obstacle was turning the view with the mouse, rather than lateral walking. The prior keyboard-focus fix remains valid but did not address this concern. A simulated mouse-capture rejection reproduced an opening panel that stayed over the view. Entry state is now independent of mouse-capture state, and an explicit Explore by dragging option lets the user hold left mouse and drag horizontally or vertically without requiring capture. Escape and rejected capture leave the scene unobstructed, with persistent instructions and an Enable mouse look button. Pointer capture keeps a drag working across overlay boundaries and ends it cleanly on release/cancel/focus loss.

Production build passes. Chrome passes 16 mouse-look checks; Edge passes the same checks plus two first-entry capture-rejection checks (18 total). Checks use real mouse movement and inspect camera yaw/pitch, covering horizontal/vertical drag, captured horizontal look, fallback after rejection, Escape, movement without camera translation, overlay crossing, sideways walking and E interaction. Reports: `m4-review/mouse-look-report.json` and `mouse-look-edge-report.json`. The shared callback includes the additional first-entry cases. Original interaction regression expectations for returning from Escape are updated to the new Enable mouse look control.

Implementation references: [Pointer capture](https://developer.mozilla.org/en-US/docs/Web/API/Element/setPointerCapture), [Pointer Lock API](https://developer.mozilla.org/en-US/docs/Web/API/Pointer_Lock_API).

### Review follow-up — adversarial geometry pass, September 5

Brian requested repairs for wall/trim gaps, a floating rear switch, raised squares on the right wall and fuller trees, plus a wider adversarial inspection. [Before/after comparisons](m4-adversarial/index.html) show the same six viewpoints. The complete gallery is refreshed from the revised asset; original revision metrics are retained in `m4-review/revision-1/`.

The screenshot's dark baseboard marks came from paint-loss details, including an overly broad name match that stretched small decals when extending the side trim. Those misleading strips are removed. Side plaster, passage/room baseboards and cornices now overlap their backing walls and ceiling instead of leaving visible slivers. The passage switch moves out of the rear doorway onto the right passage wall. Room switches, outlet plates, tally board, vents, fixing details and pipe straps now meet their supporting surfaces. The right-wall rectangles remain subtle seams around inferred masonry infill; their former 18–25 mm projections are reduced to at most 1.5 mm.

The wider pass also closes gaps under crate stacks and the hand truck, gives the trolley collision coverage for its full body, connects pendant conduit to the ceiling and utility wires to insulators, and removes duplicate neighboring gable faces and conspicuous repeated paint damage. Tree canopies now use 50,400 leaves across eight trees, up from 14,560, with modestly broader leaves. These remain invented procedural vegetation and site details.

`model/audit_full.py` runs construction contact checks before batching and separately probes the actual saved mesh along wall/floor seams, behind fixtures and through the rear portal. This complements visual inspection and route tests; sampling does not establish that every triangle is defect-free. Reproduce the saved audit with Blender `--background --python-exit-code 1 --python model/audit_full.py`, then rebuild both galleries with `planning/build_m4_review.py` and `planning/build_m4_adversarial.py`.

Latest measurements and verification for this revision are recorded below. M3 device/budget acceptance remains pending.

Production build and nine Node tests pass. Chrome interaction regression passes 27 checks; final-asset route verification passes 13 checks in each of Chrome and Edge with no runtime errors. Construction contact checks pass 100/100; the saved geometry passes 2,444 wall/floor/backing probes with no rear-portal obstruction. Final entrance geometry retains 320 clear sampled poses and 108 passing glazing-grid rays. Close-up browser captures inspect the tally-board edge, room switch, side vents and ceiling corner in addition to the six comparison views.

| Revised measurement | Chrome | Edge | Provisional target |
| --- | ---: | ---: | ---: |
| Navigation to ready | 5.04 s | 5.31 s | ≤ 5 s |
| Walking p95 frame interval | 18.1 ms | 18.2 ms | ≤ 20 ms |
| Transfer through ready | 13.76 MB | 13.76 MB | ≤ 15 MB |
| Full-scene checks | 13/13 | 13/13 | All pass |

The final asset is 13,331,756 bytes, with 298,883 source triangles, 99 render meshes, 105 colliders and 1,623 inventoried construction objects. Conservative texture memory remains 33.33 MiB; the browser reports 24 textures. The six-view capture samples up to 198 draw submissions and approximately 598k rendered triangles including shadow passes. Conditions match the initial isolated 1080p profiles above. Fuller canopies add about 2.87 MB and put cold readiness slightly beyond the provisional five-second target; this is a recorded loading tradeoff, not a claim that every working budget passes. Preliminary profiles from this revision are retained in `m4-adversarial/initial-*-profile.json`.

The 27 interaction checks were run after the first rebuilt revision; the final minor wall-mount adjustments were followed by both browser route checks, the production build, Node tests and independent geometry audits. No interaction code changed in this visual pass. Final artifact hashes are in `m4-review/verification-summary.json`.
