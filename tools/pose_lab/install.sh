#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
RUNTIME="$ROOT/concepts/pose-lab/standalone"
mkdir -p "$RUNTIME"
if [[ ! -d "$RUNTIME/ComfyUI/.git" ]]; then
  git init "$RUNTIME/ComfyUI"
  git -C "$RUNTIME/ComfyUI" remote add origin https://github.com/Comfy-Org/ComfyUI.git
  git -C "$RUNTIME/ComfyUI" fetch --depth 1 origin 1568e6cfd04586a4b3c4e1817ea7dde09b1bf9e7
  git -C "$RUNTIME/ComfyUI" checkout --detach FETCH_HEAD
fi
if [[ ! -x "$RUNTIME/venv/bin/python" ]]; then
  uv venv --python 3.12 "$RUNTIME/venv"
fi
export UV_HTTP_TIMEOUT=300
uv pip install --python "$RUNTIME/venv/bin/python" 'torch==2.7.1' 'torchvision==0.22.1' 'torchaudio==2.7.1' --index-url https://download.pytorch.org/whl/cu128
uv pip install --python "$RUNTIME/venv/bin/python" -r "$RUNTIME/ComfyUI/requirements.txt" pycairo
fetch() {
  local dest="$1" url="$2"
  if [[ ! -f "$dest" ]]; then
    curl -fL --retry 5 -C - -o "$dest.part" "$url"
    mv "$dest.part" "$dest"
  fi
}
fetch "$RUNTIME/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors" https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors
fetch "$RUNTIME/ComfyUI/models/controlnet/xinsir-openpose-sdxl.safetensors" https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors
uv pip freeze --python "$RUNTIME/venv/bin/python" > "$RUNTIME/requirements-installed.txt"
git -C "$RUNTIME/ComfyUI" rev-parse HEAD > "$RUNTIME/comfy-revision.txt"

"$RUNTIME/venv/bin/python" "$ROOT/tools/pose_lab/verify_models.py"
