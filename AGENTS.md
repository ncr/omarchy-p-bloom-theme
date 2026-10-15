# Wallpaper work

Before designing, regenerating or extending this wallpaper collection, read
[the production guide](docs/WALLPAPER-PRODUCTION-GUIDE.pl.md). It records the
user's decisions and failures discovered during review. Follow the current
user request when it supersedes the guide.

Inspect the relevant images in `docs/references/` and their manifest; distinguish
accepted style references from pending studies. `tools/FIDELITY.md` supplies
technical history, but its early descriptions are not all current defaults.

Use the deterministic Blender → visible vector paths → Cairo pipeline, with
shared typography and original Omarchy SVG. Preserve narrative facts when
redesigning an existing sheet. Validate pose, labels and both aspect ratios.
Review output belongs in `concepts/`; the development viewer reads
`concepts/development/`. Desktop installation and Git publication follow the
user's requested scope. Do not infer approval of a study merely from its being
present in the viewer. Do not use the unrelated `imagen` directory.

Screens other than the two 5K masters get composed sets from
`tools/aspect_layout.py` (release matrix, type floor, block templates; guide
section 28). Render with `tools/render_wallpaper_sets.py`, review with
`tools/aspect_matrix_review.py`, package with
`tools/package_wallpaper_profiles.py`. Layout fixes for enlarged type must be
conditional (`layer_mode` / `Sheet.type_growth`) so the masters stay
byte-identical.

The exported drawing geometry in `tools/assets/` is not in Git (about 170 MB of
JSON). Run `python3 tools/fetch_render_assets.py` to restore it from the
`render-assets-v6` release before rendering; after regenerating geometry,
publish a new release (`render-assets-v7`, …) and update the tag and checksum
in that script. Build the archive deterministically from `tools/assets/`:
`find . -type f | LC_ALL=C sort > list` and `tar --format=gnu --mtime=@0
--owner=0 --group=0 --numeric-owner --mode=644 --no-recursion -cf - -T list |
xz -9e -T0` (this reproduces v5 and v6 byte for byte).

Every set also exists at three ground levels, Muted / Default / Vivid
(`Sheet.ground_level`, `--level` on the render and audit tools; values in
`docs/collection/palettes.json` → `levels`, derived and checked by
`tools/ground_levels.py`; review sheets by `tools/ground_level_review.py` in
`concepts/ground-levels/`). Only the ground changes. Default must stay
byte-identical; every resolution ships three packs (`packs` → muted, default, vivid in
`profiles.json`), each a group of per-file objects.
The layout audit includes a per-label contrast check at every level.

Shipped wallpapers are per-file objects on Cloudflare R2 (bucket `media`, key
`p-bloom/<sha256>.webp`, served at `objects_base` in
`docs/collection/profiles.json`). An object is never replaced or deleted:
checkouts in the wild download the files their own manifest names. To fix
wallpapers: `tools/run_matrix.sh o02,b13` (those sheets in every set, all
levels; it accepts the new 5K masters), audit, `python3
tools/package_wallpaper_profiles.py`, `python3 tools/publish_wallpaper_objects.py`
(uploads only new files with Wrangler, then downloads them to check), and only
then commit the manifest and `backgrounds/`. `backgrounds/` holds only the
starter, one sheet per background colour (`STARTER` in the packaging script,
`starter` in the manifest); the README image tools read the full set from
`dist/wallpaper-release/16x9-2880p/`. The `files`/`archive` entries and
the `wallpapers-v1` release are the frozen first release for older companion
apps; leave them as they are.
