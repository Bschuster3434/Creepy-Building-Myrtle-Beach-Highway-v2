# M2 first blockout review — September 4, 2026

M2 is **Done** in Notion. Brian approved the corrected blockout, explicitly approved the concealed top-hinged right entrance pane with a 15-degree inward tilt, and authorized the review HTML upload to M2. All seven checklist items are complete. Functional window implementation remains M3 work.

Open [the review page](m2-review/index.html), [Blender source](../model/myrtle-beach-v2-blockout.blend), [floor plan](m2-review/dimensioned-plan.svg), [section](m2-review/section.svg), or [walkthrough](m2-review/walkthrough.mp4). The authoritative task is [M2 in Notion](https://app.notion.com/p/3d1488886d5781c18428fc814fe8cba4).

## Scale and comparison findings

Use the old GIS envelope as a **provisional wall footprint** of 7.35 × 15.30 m. The canopy adds 1.45 m beyond the front wall. Whether the 1998 mapped outline included the canopy remains unresolved; this choice is a working hypothesis, not an independently measured shell.

The G04 front crop shows approximately 640 pixels across the front wall and about 375 pixels from ground to parapet, with perspective and vegetation affecting the endpoints. Its apparent height/width ratio is roughly 0.59. The blockout's 4.40/7.35 ratio is 0.60. Each photographed display window occupies roughly one quarter of the facade width; the model uses 1.90/7.35 = 0.26. These broad proportions support a first pass but cannot determine absolute scale. A 2.15 m door height is a plausibility assumption. No calibrated brick-course measurement or photogrammetric camera solve has been performed.

- **Front / G04:** paired doors, central recessed entry, two display windows, three canopy posts and tall parapet are present. Canopy elevation and window positions broadly correspond. Current glazing lacks the photographed fine door muntins, distressed framing and shallow trim profiles; those are later detail work. The apron is a simplified slab and appears more regular than the photograph.
- **Front-left / G02:** long solid wall, falling stepped silhouette and large tree beside the wall are represented. Tree mass obscures part of the left elevation, as in the reference. Hidden rear opening count remains unknown.
- **Front-right / G05–G07:** stepped parapets, rearward chimney, front-side vent, closed masonry infill and utility pole are represented. Exact step breaks and infill extents remain approximate. The chimney cap is an unresolved simple placeholder rather than a reconstruction of its photographed hood.
- Camera locations are approximate corresponding angles; the comparisons are not registered overlays. Different trees and lens framing prevent pixel-level claims. Rear elevations and roof structure have no photographic confirmation.

## Geometry decision register

Evidence IDs refer to the [M1 dossier](https://app.notion.com/p/3d1488886d5781839b10f5576dfe98e5). Earlier dossier restoration language is superseded by Brian's confirmed long-unused, clean and lightly abandoned direction.

| ID | Decision | Evidence/class | Remaining uncertainty |
| --- | --- | --- | --- |
| M2-01 | Rectangular shell 7.35 × 15.30 m; front y=0, rear y=15.30 | E03 observed form; E08 weakly inferred dimensions | GIS canopy inclusion, mapping age and scale |
| M2-02 | Wall thickness 0.24 m; partitions 0.12 m | E13; invented construction fit | Actual wall assembly and support system |
| M2-03 | Floor +0.18 m; flat ceiling underside +3.08 m, 2.90 m clear | E13/E19; recollection plus invented levels | No level survey; no basement/upper floor assumed |
| M2-04 | Roof centerline +3.70 front to +3.40 rear (1.96% fall); 0.14 m deck | E07 strong inference of low slope; invented assembly | Framing, drainage and roof finish unresolved; about 0.13–0.43 m clear above ceiling assembly |
| M2-05 | Five parapet segments: 4.40, 4.20, 4.00, 3.80, 3.60 m | E06 observed stepped form; inferred dimensions | Step locations 3.5/7.0/10.8/13.2 m are approximate |
| M2-06 | Recess depth 0.305 m; mouth 1.95 m; single 45-degree return each side; paired doors 1.40 × 2.15 m | E04 observed arrangement; inferred sizes | 45-degree returns confirmed by Brian; recess depth remains an inferred fit; door handedness and frame details remain provisional |
| M2-07 | Display windows 1.90 × 1.82 m; sill 0.66 m above floor | E04 observed openings; inferred sizes | Frame reveal and sill dimensions |
| M2-08 | Canopy projects 1.45 m; front top 3.05 m, back 3.18 m; three 65 mm posts | E05 observed form; inferred size/material | Post section, small fascia details and concealed support |
| M2-09 | Closed right-side infill; surface markers, not traversable openings | E10 observed latest baseline | Number and precise extents remain approximate |
| M2-10 | Centered 1.00 × 2.10 m outward-opening rear door | E18 weak inference from recollection; invented size/swing | Rear construction and threshold |
| M2-11 | Storerooms begin y=8.80 m; each 2.565 × 6.14 m clear; passage 1.50 m clear | E15 invented; Brian's authorized V1 arrangement | Brian reviewed the layout; only entrance correction requested |
| M2-12 | Counter 1.90 × 0.62 × 0.94 m at x=2.20, y=1.95; chair behind at y=2.88 | Brian's placement; invented placeholder dimensions | Placement reviewed; final furniture style remains for M3 |
| M2-13 | Local +Y bearing ~020°, +X ~110°; neighbor left/rear, field right, highway front | E09/E14 strongly inferred/directly observed relationships | Site widths, distances and tree sizes are contextual estimates |
| M2-14 | W04 right angled return proposed as a top-hinged inward-tilting pane | Approved invented mechanism within existing glazed perimeter | Explicitly approved by Brian; implementation remains M3 work |

## Circulation and validation

The modeled passage has 1.50 m clear width. Storeroom openings are 1.00 m before detailed frames; the rear opening is 1.00 m. Each front leaf is 0.70 m, so the recorded route assumes **both front leaves open**. Clear openings will reduce with M3 frame/hardware detail and must be checked again.

The walking route runs from apron through the front shop, into each storeroom, back to the passage and out the rear door. Its sampled 0.50 m diameter body clears modeled walls, furniture and conservative bounds of open door leaves. An initial diagonal route clipped a storeroom leaf; the corrected route clears the leaf end before turning. See [the generated check](m2-review/circulation-check.json) for sample count and duration. Pauses turn the camera at each waypoint. This is a geometric route check, not browser movement or a structural/building-code assessment.

The counter's right edge is 0.285 m from the side wall, so access to its staff side is **around its left end**. Its left edge is x=1.25, leaving the central route clear. The chair front is about 0.39 m behind the counter back; staff can approach the chair from the left. This sparse arrangement preserves Brian's front-right composition.

Interior floors are continuous. The front apron is +0.07 m and floor +0.18 m, represented with small threshold steps; rear landing is +0.18 m with a +0.09 m step down to ground. These levels are inventions, require visual review, and are not a proven accessible route. Blender camera height remains 1.65 m above the interior floor datum; browser step handling belongs to M3.

The scene saves at frame 1 with closed doors and opaque Workbench glass for exterior comparisons. Front doors stay closed through frame 28 and open by frame 40 during the approach; other doors open at frame 2. Glass hides at frame 41 for interior visibility. Select the **Walkthrough** camera to inspect its keyed timeline. This is a review presentation convention; interactive mechanisms and realistic glazing are later work.

## Window proposal and M3 boundary

Brian approved making the existing right angled glazed entrance return (W04) top-hinged, with a concealed hinge and limited 15° inward tilt. Preserve its visible perimeter and whole-pane appearance. At a provisional 1.49 m pane height, bottom movement is approximately 0.39 m. No new side opening is proposed; the photographed side infill remains closed. This is invented, not evidence of an original mechanism. M3 must verify actual hinge/frame geometry, clearance from the right door, and reach. **The approach is explicitly approved by Brian. Detailed mechanism construction and clearance validation remain M3 work.**

Proposed M3 sample: the **entire front store R01**, from the entry to y=8.80 m, with its floor, ceiling, chair/counter, front doors, display windows and glazed returns. Include the entire facade and canopy, apron to y=-4.70 m and side returns to y=3.50 m. Rear rooms and wider site remain blockout context. Performance budgets and target devices remain for M3 kickoff.

## Rebuild and resume

From the V2 repository root:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python-exit-code 1 --python model/build_blockout.py -- --walk
ffmpeg -hide_banner -loglevel error -y -framerate 8 -i planning/m2-review/walk-frames/frame-%04d.png -c:v libx264 -pix_fmt yuv420p -crf 22 -movflags +faststart planning/m2-review/walkthrough.mp4
python planning/build_m2_review.py
```

The script creates a fresh V2 scene and overwrites generated V2 artifacts. Change [parameters](../model/blockout-parameters.json) and rebuild for dimension revisions; some minor feature positions and presentation labels still live in the scripts. Preserve manual scene edits separately before rebuilding. V1 was not opened or modified during this implementation.

**Resume:** M2 is complete. M3 remains To Do. Carry the approved geometry and window approach into the full front-room/storefront sample; refine target devices, checklist and numerical performance budgets at M3 kickoff.

**Notion synchronization:** the review HTML is attached to M2, all seven task checklist items are checked, and M2 is Done. Separate handoff writes to the project and M3 pages were rejected by automatic approval review because the explicit upload authorization named M2. Those remote handoffs remain stale; use M2 and this local record.

## Entrance correction following Brian's review

Each fixed entrance return is one pane at exactly 45 degrees to the front wall, ending directly at the paired door jamb. The previous geometry was approximately 70 degrees. Holding the existing mouth and door widths gives a 0.275 m inward run plus the 0.030 m front offset: door plane y=0.305 m. Each return is about 0.389 m long. No extra glazed bay is present. The revised front-store area is approximately 58.7 m2. A new closed-door close-up and visible front-door opening in the recording distinguish the doors from fixed glazing.

Brian approved the corrected blockout, then separately approved the window mechanism and M2 HTML upload. M3 performance budgets remain to be defined at kickoff.

## Approval recorded

Brian explicitly approved the working-window approach and review HTML upload after approving the corrected blockout. M2 now has the approved HTML, complete checklist and Done status. M3 stays To Do.