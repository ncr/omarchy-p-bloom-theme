# p(bloom) Pose Lab

Independent local OpenPose + masked SDXL reference generator. No files, models,
environments, or configuration are loaded from another image-generation project.
Only the wallpaper repository's current vector geometry supplies the starting poses.

## Install and launch

Requires NVIDIA CUDA-capable GPU (tested target: RTX 5080 16 GB), `uv`, `git`, `curl`.

```bash
tools/pose_lab/install.sh
tools/pose_lab/run.sh
```

Open http://127.0.0.1:8191. Backend: 127.0.0.1:8190. Ctrl-C stops both owned
processes. No service, desktop changes, cloud keys, extensions, or custom nodes.
Runtime, fresh model downloads, caches and backend state are isolated under
`concepts/pose-lab/standalone/`. This directory and all studies are Git-ignored.
Installation records the Comfy commit and installed package versions there.

## Workflow

1. Select Presence Rig, Proxy, or Truth Lamp. Drag coloured joints to adjust pose.
2. For a standalone reference, select “Osobna referencja postaci”. Mask is ignored.
3. For inpainting, select “Poprawka wewnątrz maski”. Paint white broadly over the
   desired character region using a finger or mouse; erase to protect nearby items.
   Cover both old and new silhouette if moving a limb. Undo and Reset are available.
4. Generate. Seed, prompt, pose, mask and API workflow are saved in the run folder.
5. Review the reference before manually tracing approved contours into Cairo curves.
   Generated raster images are studies, not replacement wallpaper artwork.

Generation is around one megapixel, limited to the figure crop. The masked study
is composited into the original wallpaper at native resolution. Feathering goes
inward: every pixel outside the mask remains unchanged. Labels inside a painted
mask can change, so exclude legends when painting. Original branding and lettering
remain authored by the existing deterministic renderer in final wallpapers.

Presets currently target this branch's 5120×2160 wallpapers. They do not
infer crop coordinates for 16:9 or arbitrary files. Proxy references include a
complete dummy for anatomy study; final artwork retains its headless joke.
OpenPose constrains joints, not limb volume, hand shape, symmetry or physical
plausibility: inspect generated references before tracing. No automatic vector
tracing is claimed or performed.

## Models and provenance

- [SDXL Base 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0),
  original single-file checkpoint; see its OpenRAIL++ license/model card.
- [Xinsir OpenPose SDXL](https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0),
  Apache 2.0; standard OpenPose18 colour sequence and thick elliptical limbs.
- [ComfyUI](https://github.com/Comfy-Org/ComfyUI), core nodes only.

About 9.4 GB model weights plus Python/CUDA runtime. Downloads happen directly
from the authors. Installer resumes `.part` downloads and renames on completion.
Generation binds only to loopback. Existing source wallpapers are never written.

## Checks

```bash
concepts/pose-lab/standalone/venv/bin/python tools/pose_lab/test_geometry.py
```

Backend log: `concepts/pose-lab/standalone/backend.log`.
Each run contains `recipe.json`, `openpose.json`, `workflow-api.json`, pose/source/
mask PNGs, `reference.png` and (in masked mode) `wallpaper-study.png`.

## Local validation (2026-09-24)

RTX 5080, fresh PyTorch 2.7.1+cu128, ComfyUI commit
`1568e6cfd04586a4b3c4e1817ea7dde09b1bf9e7`. Both model SHA256 values
matched the authors' published LFS records. Reference trials took 25–52 seconds
at 768×1216, 30 steps, including loading/offloading overhead.

The base SDXL trials are **not approved tracing references**: they tend toward
robotic anatomy and sometimes crop the head or feet despite pose conditioning.
This is a working minimal experimentation setup, not a guarantee of anatomically
correct crash-test-dummy images. Review every result. The masked mode uses source
VAE latents plus a noise mask (masked img2img) with final exact pixel compositing.
