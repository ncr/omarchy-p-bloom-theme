# Authored articulated crash-test dummy

A self-contained Blender model, posed in 3D and projected into deterministic
Cairo line art. No diffusion image, OpenPose inference, raster tracing, downloaded
third-party asset or external image-generation installation participates.

The model is an original schematic design, not a certified Hybrid III replica.
Molded torso, pelvic shell, head, hands, feet and four limb castings are smooth
subdivision surfaces. Left/right sides share their mesh definitions. A rigid
armature provides joints; scripted poses preserve physical part lengths. The
shared profile and pose definitions are in `build.py`.

```sh
blender -b --factory-startup -t 4 --python tools/mannequin3d/build.py
python tools/mannequin3d/check_geometry.py
python tools/mannequin3d/preview.py
python tools/make_wallpapers.py --out concepts/mannequin3d/ultrawide
python tools/make_wallpapers.py --size 5120x2880 --out concepts/mannequin3d/16-9
```

Blender is needed only to rebuild the model/projections. Wallpaper rendering
reads `tools/assets/mannequin3d/*.json` using `projected_dummy.py`.

Silhouette edges are classified in evaluated subdivided geometry. BVH ray tests
remove hidden contours and seams. Dense vector paths retain native-resolution
sharpness; opaque projected silhouettes clear background construction lines.
The exported anatomy is combined with the original authored apparatus, labeling,
fonts, branding, line treatments and grain.

Scenes for inspection/posing are saved in `concepts/mannequin3d/*.blend` (ignored).
Use Pose Mode on `Pose skeleton` to inspect articulation. Reproducible wallpaper
exports use the scripted poses; interactive Blender edits are not automatically
imported into the generator. JSON records limb endpoints, projection scale and
visible paths. Presence is frontal; Proxy is lateral with the head intentionally
omitted; Truth Lamp uses lateral and frontal projections of the same seated pose.

Model studies and before/after galleries live under `concepts/mannequin3d`.

## Hybrid dummy / humanoid robot treatment

The revised common shells combine crash-test registration targets with a smooth
Optimus-inspired sensor face, a tapered thorax, slimmer limb covers and shorter
neck/waist interfaces. The wraparound visor is a separate 3D surface, projected
into a dark vector panel; it is not a painted raster overlay. Paired part lengths,
poses, compact grouped-finger hands and the headless Proxy convention remain.
Visual reference: https://www.tesla.com/en_au/AI (Tesla Optimus).

The Gen 2 reference study replaces the long barrel torso with a short breastplate,
a separate dark shoulder yoke and abdominal housing, a narrow spine actuator,
and two hip drives. The head has straighter sides and a broad dark face; thighs
and especially shins are slender. Housing tints are projected visible mesh faces,
not hand-painted silhouettes. Crash-test targets and grouped hands are intentional
hybrid features rather than an exact Optimus replica.

Photographic study: Tesla Gen 2 promotional still, viewed at
https://i.gzn.jp/img/2023/12/14/tesla-optimus-gen2/01.jpg
and https://www.journaldugeek.com/app/uploads/2023/12/Optimus.jpg .
Study outputs and previous-version comparisons: `concepts/optimus-study/`.

The line-shell revision uses faint light washes instead of contrasting black
housings and visor fills. A shallow shoulder yoke and separate neck coupling
replace the tall conical neck transition. Shared hand and foot meshes use rounded
rectangular sections with support rings for flatter palms, toes and soles; compact
thumb wedges replace spherical lobes. Outputs: `concepts/line-shell-study/`.

Neutral Presence pose uses outward thumb wedges; the running and seated hand
orientations are independent. End-ring creases preserve planar shell caps under
subdivision, avoiding scalloped contours. Visibility distinguishes own-shell
silhouettes from detail paths and uses a grazing-normal tolerance. Projection
paths receive bounded simplification (0.12 design units for outlines, 0.1 for
seams), and fragments shorter than 3.5 units are omitted; calibration targets
are exempt. This remains direct geometry projection, not bitmap tracing.

Contour closure: silhouette visibility ignores self-occlusion of its own shell;
other parts still occlude it. Visibility transitions are located by 12 bisection
steps instead of dropping whole sample intervals. Visible runs crossing the
start of a closed contour are joined before simplification. This fixes small
breaks at hands, soles and shell junctions without joining unrelated parts.
Reviewed outputs: `concepts/closed-lines-study/`.
