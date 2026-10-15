"""Verify model bytes against the authors' published Hugging Face LFS SHA256."""
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/'concepts/pose-lab/standalone/ComfyUI/models'
MODELS={
 'checkpoints/sd_xl_base_1.0.safetensors':(6938078334,'31e35c80fc4829d14f90153f4c74cd59c90b779f6afe05a74cd6120b893f7e5b'),
 'controlnet/xinsir-openpose-sdxl.safetensors':(2502139104,'b8524e557a7df60d081f5d4a0eb109967d107df217943bf88c2d99b9ebcc06c5')}
if __name__=='__main__':
    for name,(size,digest) in MODELS.items():
     p=ROOT/name
     if not p.is_file() or p.stat().st_size!=size:raise SystemExit(f'Incomplete model: {p}')
     with p.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
     if actual!=digest:raise SystemExit(f'SHA256 mismatch: {p}')
     print(f'OK {name}',flush=True)
