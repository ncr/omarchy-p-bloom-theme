#!/usr/bin/env python3
"""Download the exported drawing geometry (tools/assets/) needed to re-render wallpapers.

The geometry is about 170 MB of JSON, so it lives in a GitHub Release archive
instead of the theme repository. Installing or using the theme does not need it.
"""
import hashlib
import io
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = 'render-assets-v6'
NAME = 'p-bloom-render-assets.tar.xz'
SHA256 = '1f2ef9b9326702de994ef66c0a30330ebd02fe237763f5f70dae8a2bbd54d4da'
URL = f'https://github.com/ncr/omarchy-p-bloom-theme/releases/download/{TAG}/{NAME}'


def main():
    print(f'Downloading {URL}')
    request = urllib.request.Request(URL, headers={'User-Agent': 'p-bloom-render-assets'})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != SHA256:
        raise SystemExit('Checksum mismatch; nothing was extracted.')
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:xz') as tar:
        members = tar.getmembers()
        for m in members:
            if not (m.isfile() and m.name.startswith('tools/assets/') and '..' not in Path(m.name).parts):
                raise SystemExit(f'Unexpected archive entry: {m.name}')
        tar.extractall(ROOT, members=members, filter='data')
    print(f'Extracted {len(members)} files into {ROOT / "tools/assets"}')


if __name__ == '__main__':
    main()
