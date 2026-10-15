# Deterministic construction details

For the current production rules and accumulated user feedback, read
[the production guide](../docs/WALLPAPER-PRODUCTION-GUIDE.pl.md) first.
This file also contains historical implementation notes; early descriptions
of figure conventions and studies do not all describe the present generator.

All 14 main views now receive a boxed A caption from `Sheet.end_main()`, using
the same `view_label()` convention as B/C. Per-model A captions were removed.
The label audit captures centred single glyphs and requires exactly one A in
both formats, plus exactly one B and C in ultrawide. Review renders:
`concepts/main-view-labels/` (both formats); development viewer uses the wide set.
Main-view captions name each device or depicted use specifically; generic
"assembly", "unit" and "configuration" captions are disallowed. The audit
also checks caption uniqueness across the collection. The revised name set
and both rendered formats are in `concepts/unique-main-captions/`.

The original 14 Fable concepts, annotations, legends, service dates, palette
order, Nimbus Sans typography and Omarchy SVG remain the source of truth.
`fidelity.py` adds authored vector geometry, not generated raster imagery.

Render native, lossless masters without changing the installed wallpaper:

```sh
python3 tools/make_wallpapers.py --size 5120x2160 \
  --out concepts/starmap-collection/native --ext png
```

Coordinates remain in the original 1080-unit drawing space. Cairo rasterizes
the paths at the requested output size; there is no intermediate enlargement.
PNG and the default WebP export are lossless. JPEG remains available but is not
appropriate for the master artwork's fine coloured strokes.

The default device style is now `starmap`: the accepted Truth Lamp treatment
applied throughout the collection. `starmap.py` selects the focal component of
each device; `starmap_study.py` contains the shared line treatment. Primary
outlines stay bright, secondary construction is quieter, and auxiliary strokes
have smooth spatial ink-density variation. Decorative emblem rings are dimmer;
the Omarchy SVG and all typography retain their original settings. Existing
authored sections remain in place; the extra reflector and field sections are
specific to Truth Lamp. Use `--style original` to reproduce the clear-labels
masters. Neither render command installs a wallpaper or changes the desktop.

`tools/build_starmap_collection.py` renders the full native set, checks every
text call and its transform against the original style, verifies Truth Lamp
against the accepted study, and creates collection previews. Check label
clearance with `tools/verify_wallpaper_layout.py --out REPORT.json`; add
`--size 1920x1080` for the compact layout.

Each main view calls `enrich()` before its annotations, inside `begin_main()`.
Details belong to identifiable parts: bearings, threaded caps, panel fasteners,
heat-sink fins, fluid routes, circuit fan-out, joints and structural seams.
Avoid adding free-floating decorative machinery, invented labels or clutter
in the legend and secondary plots. Do not consume `s.rng` in an added detail
pass: that would change the original downstream simulation/plot samples.

The human figures follow the visual approach of NASA's human-factors drawings:
neutral lateral/frontal envelopes, anatomical proportions, supported posture,
subordinate segment axes and joint landmarks. The source reference is
[OCHMO-HB-004, figures on pages 47 and 77](https://www.nasa.gov/wp-content/uploads/2023/12/ochmo-hb-004-rev-a-dec2023.pdf).
The paths are original illustrative studies, not certified percentile models.
Hair, costume, expressive faces and decorative anatomy hatching are omitted.
The Truth Lamp table height and chair geometry follow the revised seated pose.

Opaque contours restore the aligned background underneath them. Objects retain
physical layering; table settings are drawn after the figures. Mechanical
shells (Proxy) and wearable reference bodies (Presence Rig) share the accepted
crash-dummy convention; Bounder retains its quiet anatomical leg envelope.
Shared view frames use quiet registration corners and datum axes. Magnified
views retain their boundaries but lose unrelated circular graduations. Do not
invent dimensions, degree values or NASA branding. Preserve the original
Omarchy mark, text content, palettes and the fictional devices' narrative.

The accepted crash-dummy refinement adds quartered amber/dark optical targets,
mould seams, segmented neck boots and joint caps. These accents belong on the
reference bodies and wearable/mechanical figures (Truth Lamp, Presence Rig,
Proxy, Bounder), not arbitrarily across every device. Preserve the accepted
anthropometric envelope. Heads use a smooth, featureless shell: omit ears,
facial lines and head fasteners, retaining one tracking target. The user's
crash-dummy photo references inform a separate rigid head shell, one subdued
rear access-cap seam in profile, and a recessed neck shaft with curved collars.
Keep the accepted blank frontal face, a minimal lateral nose cue and original narrative text; the
dummy treatment is a drawing convention, not a rewrite of the fictional story.

`human_figures.py` owns the articulated Proxy and Presence Rig reference bodies.
Paired components share dimensions and contours. Proxy's elbows and knees are
solved from fixed segment lengths; their bend direction must remain consistent
in the side elevation. Hands are compact moulded envelopes with an integral
thumb and a connected wrist spigot. Preserve the reviewed thumb orientation.
The rear hand follows its forearm axis. Presence Rig uses mirrored front-view
shoes, with soles on the roller crowns; Proxy uses rotated side-view shoes.
Keep Proxy's dashed, cancelled head symbol and the original NONE FITTED caption.
Truth Lamp's seated soles meet the floor. After figure changes, review the
whole silhouette as well as enlarged joints, and run the label audit at both
5120x2160 and 5120x2880.
Visual references: [NHTSA crash-test dummies](https://www.nhtsa.gov/nhtsas-crash-test-dummies)
and [Humanetics THOR-50M](https://www.humaneticsgroup.com/products/anthropomorphic-test-devices/frontal-impact/thor-50m/thor-50m).

Postprocessing combines restrained two-scale halation, seeded multiscale
monochrome grain and slight ink-density variation. It does not warp geometry
or fonts. The crisp raster stays underneath the halation. Grain does not
replace authored geometry. Matching source, size, seed and rendering environment
produce the same output; font/Cairo/Pillow changes may affect rasterization.

The review directory contains native masters, a contact sheet and a matched
Truth Lamp comparison. It is separate from `backgrounds/` and the live desktop.

Callout text must occupy clear space beside the artwork. Check both title and
the complete subtitle, as well as later-drawn geometry and other text. Keep
the attachment dot on its original part; move the elbow and text together.
`label_layout.py` records reviewed offsets, including compact-view clearance
from the emblem. Do not hide clashes with background rectangles. Dimension
labels can shift along their line to clear datum axes; detail scale captions
sit outside the detail circle. The audit under `concepts/clear-labels/` checks
actual glyph bounds on a render without text, plus text-to-text intersections,
at 5120x2160 and 1920x1080. Explicit exceptions cover identifiers inside their
own filled symbols; no callout or legend is exempt. Follow with visual review.

### Shared 3D dummy projections

Presence Rig, Proxy and the five Truth Lamp participants now use the same
original molded 3D component definitions in `mannequin3d/build.py`. Identical
upper-arm, forearm, thigh and calf castings retain lengths 116/88/146/140 in
every pose. Blender subdivision geometry and BVH visibility produce the checked-in
vector paths under `assets/mannequin3d`; `projected_dummy.py` composites these
with the original equipment. The head remains intentionally absent in Proxy.

To change anatomy or articulation, edit the shared 3D definitions and regenerate
all views. Do not patch one limb's 2D outline independently. The head remains a
schematic molded shell, hands a closed palm/finger group with integral thumb.
Both shoes share one casting. Model/license/projection notes and rebuild commands
are in `mannequin3d/README.md`. No diffusion-generated image participates in these
wallpapers, and typography continues to be drawn only by the original renderer.

### Retrofuturist hardware assemblies

The default hardware family uses sculpted cast bases, rolled lips, rounded
service covers, analog controls and exposed mechanisms. Ten primary assemblies
are modeled independently in Blender by `hardware3d/family_build.py`; Quantum
Simulator uses the accepted radial cryostat in `hardware3d/radial.py`.
`hardware3d/accessories_build.py` supplies the lamp and camera housings.
Presence Rig and Proxy retain the accepted shared figure projections.

Checked-in JSON contains orthographic visible vector paths, not raster traces.
The exporter evaluates bevels, removes hidden edges through a scene BVH and
refines visibility transitions. Primary contours, internal construction,
wiring and optical components have distinct line weights. Typography, legends
and the Omarchy SVG are still rendered by Cairo. Original main-view callout
wording is kept in `assets/hardware-family/labels.json`; callouts are placed
outside the assembly bounds.

Rebuild geometry, then render and audit both page formats:

```sh
blender -b --python tools/hardware3d/family_build.py
blender -b --python tools/hardware3d/accessories_build.py
blender -b --python tools/hardware3d/radial.py
python3 tools/make_wallpapers.py --out concepts/retro-family/ultrawide
python3 tools/make_wallpapers.py --size 5120x2880 --out concepts/retro-family/16-9
python3 tools/verify_wallpaper_layout.py --out concepts/retro-family/layout-wide.json
python3 tools/verify_wallpaper_layout.py --size 5120x2880 --out concepts/retro-family/layout-16-9.json
```

Set `HARDWARE_ONLY=sky-racer` (or another family slug) when rebuilding one
assembly. Set `PBLOOM_HARDWARE_SET=legacy` when rendering to compare the older
primary hardware drawings; this does not revert accessory or figure refinements.
The review renders and Blender scenes live under `concepts/retro-family/`.
Rendering does not install the theme or change the desktop wallpaper.

Greener uses a full axonometric garden scene with shared telescopic cameras,
a raised fence and exposed antenna loops. Stage uses four restrained hologram
contours instead of a densely overdrawn luminous ribbon.

### Auxiliary hardware views

Run `blender -b --python tools/hardware3d/secondary_build.py` after changing
the primary assemblies. This reuses their geometry for Sky Racer's side
elevation, Fusion Transport's front elevation, Stage's plan, Aroma Organ's
section and the Cortical Mesh capsule section. Sections evaluate modifiers and
bisect solids and wire paths at one shared plane; they are not independent
silhouette approximations. `secondary_drawing.py` fits them at a uniform scale
and maintains readable page-space stroke widths. Existing analytical diagrams,
biological illustrations and data plots retain their subject and captions.
These auxiliary views appear only on ultrawide pages.

Sky Racer's replacement race-aircraft geometry lives in
`hardware3d/sky_racer.py`, called by the shared family builder. Its lofted
monocoque, framed canopy, swept folding wings, energy cassettes and paired
canted fins replace the earlier ellipsoid and tubular outriggers. Rebuild with
`HARDWARE_ONLY=sky-racer blender -b --python tools/hardware3d/family_build.py`,
then rebuild auxiliary projections with `secondary_build.py`.
The review is under `concepts/sky-racer-redesign/`; installed masters remain
unchanged pending selection.

The Sky Racer review's left inset is now a longitudinal cockpit cutaway,
generated by `hardware3d/sky_racer_section.py` (also called by
`secondary_build.py`). The near hull half is bisected; seat, harness,
pedals, controls, bulkhead frames, avionics and aft cells are authored inside
the retained envelope. The subtitle explicitly states that outboard drives
are omitted. It replaces the earlier side elevation in the reviewed poster.

Fusion Transport's replacement geometry lives in `hardware3d/fusion_transport.py`.
It separates the segmented rotating habitat, four-chord service truss, four
propellant tanks, swept droplet radiators, shielded coil reactor and open magnetic
nozzle. Rebuild with `HARDWARE_ONLY=fusion-transport` using the family builder,
then rebuild secondary projections. Its front view omits the forward dust shields.
Solid axial discs use capped cylinders; annuli are reserved for open rings to
avoid degenerate centre faces in the hidden-line export.
`fusion_transit.py` retains the left orbital diagram while distinguishing the
powered arc from a tangent coasting ellipse, with direction markers and outside
labels. The caption identifies it as schematic; retained transit times are poster
content, not results of an orbital simulation. Review renders in both formats and
before/after crops are under `concepts/fusion-transport-redesign/`.

Bounder's ultrawide left inset uses an equipped runner in flight phase instead
of the high-jump chart. `mannequin3d/bounder_runner.py` poses the shared dummy
with equal limb lengths, opposite arm/leg swing and 90-degree elbow flexion.
Both legs receive identical B-4 components transformed to their joints:
outboard rails, actuator bundles, cuffs, joint housings, foot cradles and
extruded spring blades. The near-side three-quarter projection resolves
occlusion in the combined body/equipment scene. `bounder_wearing.py` places
the result and identifies the dummy as a human athlete in the annotation.
Rebuild only this asset with
`MANNEQUIN_ONLY=bounder blender -b --factory-startup -t 4 --python tools/mannequin3d/build.py`,
then render sheet 6. The other dummy projections are not rebuilt by that
command. Review output is under `concepts/bounder-runner/`.

Tether Climber's auxiliary review is in `concepts/tether-details/`.
`hardware3d/tether_details_build.py` exports the ocean anchor, GEO transfer
station, counterweight, peeled ribbon sample and hollow CNT bundle.
`tether_details.py` assembles these projections with the original TC-20 geometry
in a broken-altitude system diagram and a two-level material study. Both panels
are ultrawide-only. Labels identify the schematic scales and exaggerated ribbon
thickness. The three separated strata are an authored future ribbon construction,
not a measured specimen; no atomic-scale resolution or defect-free length is
claimed in the new inset.

The material hierarchy follows CNT bundles/fibres rather than the previous two
overlaid graphene hexagon grids. References: NASA's space-elevator architecture
report (https://ntrs.nasa.gov/citations/20000105202), hierarchical CNT fibre
morphology (https://www.nature.com/articles/s41524-022-00705-x) and flattened CNT
ribbons (https://www.nature.com/articles/ncomms4848). Rebuild auxiliary assets with
`blender -b -t 4 --python tools/hardware3d/tether_details_build.py`, then render
sheet 9 and run the layout audit. Rendering does not update installed wallpapers.

The Air Refinery and Truth Lamp right-panel review lives in
`concepts/right-panel-review/`. `right_panel_studies.py` replaces the refinery's
box flowchart with projected equipment and separate material/utility lines.
`hardware3d/refinery_process_build.py` builds these process symbols. The enzyme
route remains part of the speculative AR-1 design; this is a concept flow sheet,
not an engineered process or mass/energy balance. General CO2/hydrogen/energy
separation is informed by DOE's solar-fuels overview:
https://www.energy.gov/science/doe-explainssolar-fuels.
Truth Lamp retains all six original phrases, percentages and the fictional
11,000-dinner sample, now with larger less widely spaced text and proportional
bars (one common linear scale). Both changes affect ultrawide auxiliary panels
only. Accepted or in-review development renders are surfaced through
`concepts/development/` without installing them as desktop wallpapers.

Proxy, Sky Racer and Organ Foundry right-side studies are authored in
`hardware3d/right_aux_build.py` and placed by `right_aux_panels.py`.
Rebuild with `blender -b --factory-startup -t 4 --python
tools/hardware3d/right_aux_build.py`, then render sheets 2, 11 and 13.
Optional Blender arguments after `--` select `owner`, `course` or `kidney`.
Review renders and the previous versions live in `concepts/right-panel-redesign/`.

Proxy reuses the actual molded human stand-in head and shoulders with a supine
transform, a draped duvet, pillow, cast bed frame and bedside receiver. The human
annotation and 06:40 / 10.0 km joke remain explicit. Sky Racer uses nine physical
gates perpendicular to the trajectory, directional course segments and ground
height witnesses. Its projection is schematic, with exaggerated vertical scale;
the caption's race distance is retained poster content, not a simulated course.

Organ Foundry now depicts a conceptual coronal half-section, with cortex,
medullary pyramids, branching vascular supply and a separate collecting system.
The anatomical hierarchy follows NIDDK's kidney overview:
https://www.niddk.nih.gov/health-information/kidney-disease/kidneys-how-they-work
and the NCBI InformedHealth anatomy explanation:
https://www.ncbi.nlm.nih.gov/books/NBK279385/.
This authored print concept does not claim measured branching, a particular
patient's anatomy, realistic nephron resolution, or a validated printable kidney.
Major channels have modeled walls; cortical branches remain fine vector strokes.

PX-1 running-pose correction: `mannequin3d/proxy_pose.py` is now the common
source of joint locations for Blender and all 2D wrist/foot/hand annotations.
It replaces independent inverse-kinematics targets that put the same-side arm
and leg forward and allowed the trailing knee to bend the wrong way. The new
authored flight pose uses opposite arm/leg swing, 45/90-degree knee flexion and
90-degree elbow flexion, retaining equal 146/140 leg and 116/88 arm segments.
Foot pitch follows the selected gait phase; the trailing foot recovers above
the floor. The leg shell frame places calf fullness posteriorly. This is an
illustrative still, not validated motion capture or dynamic gait simulation.
General phase reference: https://journals.biologists.com/jeb/article/215/11/1944/10883/Muscular-strategy-shift-in-human-running.
Review renders in both aspect ratios, before/after and layout audits are in
`concepts/proxy-gait-review/`. Rebuild this pose only with
`MANNEQUIN_ONLY=proxy blender -b --factory-startup -t 4 --python tools/mannequin3d/build.py`.

Bounder's left running inset had the rear boot and spring rotated 180 degrees
toward the shin. `bounder_runner.foot_frame()` now derives the frame from the
proximal tibial direction plus plantar flexion and is shared by boot and gear.
Build-time assertions check that their plantar normals agree and point away
from the shin; equal segment lengths alone cannot detect inverted footwear.
Review: `concepts/bounder-spring-fix/`. Main hardware and right inset are unchanged.


## Biological right-panel studies — 2026-09-24

Organ Foundry and Cortical Mesh now use `hardware3d/bio_details_build.py`.
Rebuild both with `blender -b --factory-startup -t 4 --python tools/hardware3d/bio_details_build.py`;
`right_aux_build.py -- kidney` delegates to the same renal definition.

The kidney study separates seven medullary lobes, minor/major calyces, ureter,
interlobar/arcuate vessels and selected enlarged cortical corpuscles/tubules.
Lobes have different papilla positions instead of converging on one rotor-like
centre. The external print strata remain subordinate to the coronal cut.
Cortical Mesh uses a physical exploded stack: compliant carrier, metal-routing
film, windowed passivation and porous recording contact, with mesh tethers.
Hidden lines are removed in 3D; leaders and keys remain outside the silhouette.
The obsolete scale bar was removed: film thickness and exploded separation
are exaggerated and this authored concept does not have a calibrated scale.

Basis: [NIDDK kidney overview](https://www.niddk.nih.gov/health-information/kidney-disease/kidneys-how-they-work)
and [mesh-electronics layer/material diagram, Nature Methods](https://www.nature.com/articles/nmeth.3969).
These inform anatomy and layer vocabulary, not the fictional printing capability,
million-channel specifications, or a validated fabrication-ready implant.
The spike raster, original story, main and left illustrations are unchanged.
Review renders and before/after crops: `concepts/bio-detail-upgrade/`.
Status: user accepted both biological right-panel versions ("super").


## Greener — neighbourhood axonometric, 2026-09-24

The right panel now comes from `hardware3d/greener_street_build.py` and the
`greener-street.json` hidden-line asset. The original eight properties and
numbers remain: 2, 6, 10, 14 / 3, 7, 11, 15. Each house uses shared wall,
pitched-roof, seam, window, doorway, porch and drainpipe geometry. Low garden
fences, footways, kerbs, storm drains and sparse turf establish scale.
Seven gardens have optical masts; No. 7 instead has staggered paving joints.
No. 14 retains the quiet gold boundary. Numbers and the key sit outside the
scene; the original story and growth graph are preserved byte-for-byte in
the raster outside the right illustration region.

Build: `blender -b --factory-startup -t 4 --python tools/hardware3d/greener_street_build.py`.
Review: `concepts/greener-street-upgrade/comparison.jpg`.
Status: new study, awaiting artistic feedback.


## Cortical Mesh and Truth Lamp — new left studies, 2026-09-24

`hardware3d/left_studies_build.py` authors both 3D insets, exported as
`cortical-tissue-section.json` and `truth-dinner-seating.json`.
`left_aux_panels.py` owns their numbered external leaders and separate keys.

Cortical: a local bone recess with a sectioned implant can, acoustic layers,
decoder and recording strands; scalp, diploe/compact bone, a simplified
meningeal envelope, cortex and white matter are spatially distinguished.
The tissue cut includes schematic laminae, selected neuron morphologies and
axonal fascicles. This is a speculative implant concept with exaggerated
histological detail, not a measured surgical section. Anatomy vocabulary is
based on [NCBI Neuroscience: meninges](https://www.ncbi.nlm.nih.gov/books/NBK10877/)
and [cortical organization](https://www.ncbi.nlm.nih.gov/books/NBK575742/).
Preserve the 22+13 legacy RNG draws after the left panel: later spike data must
not change merely because the drawing was redesigned.

Truth: shared chair geometry faces six place settings on a thick boat-shaped
tabletop with pedestal feet, dishes, cutlery and stemware. Seat identifiers
lead to chairs; original people and fictional counts remain in an external key:
grandmother 0, uncle 14, aunt 9, host 22, guest 17, teenager 11. These source
counts are preserved despite their inconsistency with the original generic
“40 untruths per dinner” table; the redesign does not invent replacement data.
Leader ends stop short of number glyphs from whichever direction they approach.

Rebuild: `blender -b --factory-startup -t 4 --python tools/hardware3d/left_studies_build.py`.
Review: `concepts/left-panels-upgrade/`. Status: new studies awaiting review.


## Proxy and Truth Lamp — spatial main scenes, 2026-09-24

New mains use `hardware3d/main_scenes_build.py` → hidden-line geometry in
`tools/assets/hardware-family/`, composed by `main_scene_panels.py`.
The previous main-only code in `foibles.py` is replaced; auxiliary panels and
narrative legends remain unchanged. Shared mannequin molds are reused without
changing the accepted assets used by other wallpapers.

PX-1: a new running phase in a three-quarter orthographic view, opposite arm/leg
swing, matching rigid segment lengths, correct plantar orientation, conformal
service covers, physically mounted watch/skin sleeve, shoe laces, and a real
chest bib. The bib's CITY 10K / 114 typography uses three projected model anchors.
The absent head is still a separate cancellation symbol above the neck.
The builder checks that both plantar normals point away from their shins; the
initial rear-foot angle was rejected and corrected by 180 degrees.

TL-1: six human stand-ins around one modeled table, not five independent frontal
figures. Seated body molds share chairs, plates and stemware in the same space.
The host raises one forearm rigidly about its elbow. Heads have small authored
turns; no photoreal faces. A continuous dog mesh replaces the flat outline.
The elevated pendant has separate rim-mounted camera barrels and microphones.
The HUMAN FAMILY / NO ROBOTS note preserves the intended interpretation.

The build checks measured foot, hand and pelvic heights from evaluated meshes:
feet at floor level, resting hand undersides above the table, pelvis meeting the
chair cushion. This is illustrative posing, not a validated dynamics simulation.
Report: `concepts/retro-family/main-scenes-geometry.json`.
Build: `blender -b --factory-startup -t 4 --python-exit-code 1 --python tools/hardware3d/main_scenes_build.py`.
Review: `concepts/main-scenes-upgrade/`, including native 5120×2160 and 5120×2880.
Status: new main-scene studies, pending user review.
