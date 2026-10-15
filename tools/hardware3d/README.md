# Quantum Simulator hardware study

Opt-in illustration study: the default wallpaper generator and installed theme
retain the accepted artwork. Enable with `PBLOOM_HARDWARE_STUDY=1`.

1. `KICAD_CONFIG_HOME=/tmp/p-bloom-kicad python tools/hardware3d/carrier.py`
2. `blender -b --factory-startup -t 4 --python tools/hardware3d/build.py`
3. `PBLOOM_HARDWARE_STUDY=1 python tools/make_wallpapers.py --only 1 --out concepts/hardware-study/ultrawide`
4. Add `--size 5120x2880` and use a separate output directory for 16:9.

Blender contains an original assembly with cutaway shield sectors, six cold plates,
rods/collars, fasteners, coax looms, thermal anchors, an exchanger coil, optical
fibres and six populated carrier boards. A 24-degree azimuth / 13-degree elevation
orthographic view is exported as visible sharp/silhouette edges and tube paths.
The existing Cairo renderer provides typography, grain and native resolution.
Shell, structural, plate, wiring, electronic and fine-detail paths have separate
weights and opacity. Callouts use projected 3-D feature coordinates.

`tools/assets/hardware3d/carrier.kicad_pcb` is an editable KiCad illustration
asset. Its shared carrier.json drives the Blender boards and enlarged vector
inset. It is NOT a routed, electrically checked or fabrication-ready board; no
DRC or functional cryogenic-machine validation is claimed. The speculative
wallpaper's existing performance numbers are narrative, not engineering results.

The editable Blender scene is `concepts/hardware-study/quantum-assembly.blend`.
Rendered studies, KiCad SVG plot, layout audit and before/after live beside it.
