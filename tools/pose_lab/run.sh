#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
RUNTIME="$ROOT/concepts/pose-lab/standalone"
PY="$RUNTIME/venv/bin/python"
mkdir -p "$RUNTIME/input" "$RUNTIME/output" "$RUNTIME/user" "$RUNTIME/cache"
export HF_HOME="$RUNTIME/cache/huggingface"
export TORCH_HOME="$RUNTIME/cache/torch"
export PYTHONNOUSERSITE=1
"$PY" -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",8190)); s.close(); s=socket.socket(); s.bind(("127.0.0.1",8191)); s.close()'
cd "$RUNTIME/ComfyUI"
"$PY" main.py --listen 127.0.0.1 --port 8190 --disable-all-custom-nodes --disable-api-nodes --reserve-vram 3 --input-directory "$RUNTIME/input" --output-directory "$RUNTIME/output" --user-directory "$RUNTIME/user" > "$RUNTIME/backend.log" 2>&1 &
BACKEND_PID=$!
trap 'kill "$BACKEND_PID" "${PANEL_PID:-}" 2>/dev/null || true' EXIT INT TERM
"$PY" "$ROOT/tools/pose_lab/server.py" --port 8191 --comfy http://127.0.0.1:8190 &
PANEL_PID=$!
wait -n "$BACKEND_PID" "$PANEL_PID"
