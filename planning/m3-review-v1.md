# M3 first playable review — September 4, 2026

M3 is **In Progress**. Brian requested “start issue M3.” A runnable front-room sample is ready for visual review; the visual benchmark and target-device budgets have not been accepted. No M4 production or public deployment was started.

- [Open the local sample](http://127.0.0.1:5173/) while the preview server is running.
- [Review captures](m3-review/index.html), [setup instructions](../app/README.md), [M3 Blender source](../model/myrtle-beach-v2-sample.blend), [exported GLB](../app/public/assets/sample.glb).
- [M3 task](https://app.notion.com/p/3d1488886d57812f82abeb392ee5a101).

## Implemented sample

The complete front room contains four empty shelf units, three empty crates, the retained counter and Brian's empty front-right chair. The storefront, canopy, apron and side returns carry the approved shell geometry. Original procedural base-color and normal textures cover brick, wood, floor, plaster, trim, roof and ground. This is a first material/lighting candidate; it does not yet establish the final realistic, long-unused visual standard. Close-range material variation, edge wear and contact shading should be reviewed before expanding production.

The React/Three.js app has keyboard movement, swept-circle collision, level/threshold handling, paired front doors, the approved top-hinged right return pane, and a switch controlling three actual point lights and their bulbs. One shadowed sun, a hemisphere light and one unshadowed daylight-bounce approximation provide daytime illumination. The fixture lights are unshadowed. Lighting is specified in the app, not baked in Blender. The rear remains blockout context, closed off at the passage for this sample.

## Verification and measured limits

Five Node tests pass using the exported collider manifest: closed/open entrance, long-frame collision, the 0.5 m player route, door-sweep protection and thresholds/boundaries. Both Chrome 152 and Edge 152 passed the same 22 browser checks, including repeated door/window/light operation, actual keyboard movement and pointer release/resume. A separate mouse-click test switched the actual light successfully. No browser runtime errors were reported. The production build and development server were verified.

The moving window glass needed a 65 mm inset at each end to clear M2's placeholder door/hinge overlap. Its outer stationary frame and approved 45-degree perimeter are unchanged. [320 sampled mesh checks](m3-review/window-clearance.json), covering 0–15° window tilt and 0–95° door swing, found no pane/door intersections. This is a discrete geometric check, not a measured construction clearance certificate. The exterior pier can obscure the tilted pane; approach from inside to close it. Closed glass is supported by the retained perimeter; detailed concealed hinge engineering is invented.

Profiling used Windows, Intel Graphics through ANGLE/D3D11, 1920 × 1080 CSS pixels, device-pixel ratio 1, headless Chrome/Edge 152, a production Vite preview, cache disabled, and 25 Mbps down / 5 Mbps up / 40 ms latency. Each route uses fixed camera placements between legs and actual keyboard walking within legs. Startup samples were reset before the measured walking route. Browser frame intervals are not isolated GPU timings; these results are specific to this machine and automation conditions.

| Measurement | Chrome | Edge | Provisional target |
| --- | ---: | ---: | ---: |
| Navigation to scene ready | 2.65 s | 2.74 s | ≤ 5 s |
| Walking p50 frame interval | 6.1 ms | 6.1 ms | — |
| Walking p95 frame interval | 12.2 ms | 12.2 ms | ≤ 20 ms, aiming for 60 fps |
| Walking frame samples | 1,208 | 1,134 | Fixed repeatable route |
| Browser checks passed | 22/22 | 22/22 | All required checks |

The GLB is **6,826,048 bytes (6.83 MB)**. Measured resource transfer through scene readiness is approximately **7.04 MB**, below the provisional 15 MB cap; optional font requests may complete later and are not an offline guarantee. The source has **13,448 triangles, 41 mesh objects and 14 × 512² material textures**, estimated at **18.67 MiB RGBA with mipmaps**. The renderer counts 15 textures including its shadow map. One 2048² shadow map adds approximately 16 MiB at four bytes per texel; driver allocations/framebuffers are not included. Observed total draw submissions reached **82 including the shadow pass**, below the sample cap of 150. Rendered triangle submissions can reach **26,896** because shadows submit geometry again. These totals use renderer.info with auto-reset disabled and one explicit reset before the frame.

The first Edge smoke run overlapped another active rendering browser and included startup frames; its p95 was 48.5 ms over only 55 frames. The dedicated Edge run above stopped the other rendering page and used the full repeatable route. This illustrates why device acceptance should use a single active sample and recorded conditions.

Raw evidence: [Chrome](m3-review/browser-report.json), [Edge](m3-review/edge-report.json), [asset report](m3-review/asset-report.json), [geometry clearance](m3-review/window-clearance.json). The Vite build reports a 571 kB uncompressed Three.js vendor chunk (approximately 145 kB gzip); application and React code are separated and total transfer is within the provisional loading budget.

## Full-scene capacity plan

These are planning ceilings, not claims that the finished environment will pass performance targets. The sample's light geometry and sparse props leave substantial geometry capacity; vegetation transparency, additional materials and shadow cost are likely to become the constraints.

| Allocation | Unique triangles | Draw submissions incl. shadows | Estimated texture memory |
| --- | ---: | ---: | ---: |
| Building, all rooms and architectural detail | 150k | 130 | 80 MiB |
| Reused interior props and furnishings | 150k | 60 | 48 MiB |
| Immediate landscape, trees and roadside | 350k | 120 | 96 MiB |
| Reserve | 100k | 40 | 32 MiB |
| Full-scene planning ceiling | 750k | 350 | 256 MiB |

Reuse the existing materials and instance repeated shelving/crates/vegetation. Split rear interior and exterior assets so the initial front-room download remains ≤ 15 MB; load additional areas as needed. Introduce KTX2/Basis texture compression and mesh compression if increased close-view resolution or site detail makes the caps difficult. Limit shadow casters by distance, use vegetation LODs, and measure alpha overdraw before adding trees. Keep one shadowed daylight source; use baked or unshadowed local illumination where plausible. Re-profile the same route after each major room/site addition and add worst-case outdoor views before treating the full-scene budget as credible.

## Handoff

Review the sample with Brian, especially the first-pass materials, light balance and the sparse furnishings. Confirm desktop Chrome/Edge at 1080p and the proposed numeric budgets, or record the preferred hardware/input target. Apply visual revisions within M3 and repeat only affected checks. Keep M3 In Progress until its visual benchmark and device budgets are accepted. Public release, whole-site detail and the rest of the interactive building remain later milestones.

Notion synchronization: M3 is In Progress and the first five implementation checklist items are checked, with visual/device acceptance still unchecked. Automatic approval review rejected the detailed handoff append because it would export local paths and hardware/performance data without explicit authorization for that payload. Brian has been asked whether to append it. This local report is complete; the detailed handoff has not been added remotely.
