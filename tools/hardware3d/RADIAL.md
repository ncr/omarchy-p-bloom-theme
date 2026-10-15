# Independent interpretation of the Quantum Simulator poster

This study starts from the poster's words and numerical narrative, not from its
previous hardware drawing or plate-stack arrangement. Shared code is limited to
mesh primitives, vector projection and the existing poster typography/texture.

Inputs: molecular/material simulation; 10,200 logical qubits; six 1,700-qubit
modules; superconducting devices; local 4 K control electronics; optical links
between cryostats; an 8 mK base; closed-cycle cooling; magnetic/thermal shielding.
These remain the fictional product brief, not independently verified specifications.

Design decisions:
- Horizontal vacuum capsule on vibration-isolated saddles.
- Six removable radial compute cassettes surrounding a common cold manifold.
- Local controller tiles on the next concentric thermal stage.
- Curved thermal shields shown with an upper sector removed.
- Optical service connections grouped in an exterior bulkhead.
- A lower service carriage beneath the removable cold assembly.
- A detailed cassette inset generated from the SAME cassette constructor.

`radial.py` builds this scene from scratch, including its original board geometry.
It does not load the first hardware study's KiCad carrier, assembly or projections.
The board and machine are illustration concepts, not fabrication-ready designs.

Rebuild:

```sh
blender -b --factory-startup -t 4 --python tools/hardware3d/radial.py
PBLOOM_HARDWARE_STUDY=radial python tools/make_wallpapers.py --only 1 --out concepts/radial-quantum/ultrawide
PBLOOM_HARDWARE_STUDY=radial python tools/make_wallpapers.py --only 1 --size 5120x2880 --out concepts/radial-quantum/16-9
```

Editable scene: `concepts/radial-quantum/radial-quantum.blend`.
Vector data: `tools/assets/radial-quantum/{main,detail}.json`.
Default wallpaper generation and the installed desktop remain the accepted set.

## Retro-industrial design revision

The current model uses a flared cast pedestal with rolled trim and a recessed
foot, crescent saddles on waisted cast supports, a flush service drawer with a
tubular pull, analog service dials, rounded side housings, double front rim lips,
and domed cooler caps. These are modeled surfaces, not raster embellishments.
Robust polygon normals support the bevelled housings without degenerate faces.
Before/after studies live in `concepts/retro-quantum/`; the previous builder is
preserved in that study's `before` directory. The scientific narrative and radial
compute architecture are retained.
