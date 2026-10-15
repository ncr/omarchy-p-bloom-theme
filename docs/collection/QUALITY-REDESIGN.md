# Quality redesign — twelve sheets

Requested after the 34-sheet ranking: redesign the twelve below the proposed
cutoff. These are new review versions, not an automatic promotion or a new
ranking. The other 22 masters remain byte-for-byte unchanged. All 34 stay in
the local collection; no desktop installation, commit or push is part of this pass.

[Before / after gallery](../../concepts/century/quality-redesign/index.html)
— B switches versions, arrows navigate, F toggles fullscreen, Esc closes.
Both 5120×2160 and 5120×2880 are native renders. Original typography, palette,
Omarchy SVG, stable IDs, dates and narrative parameters are retained.

## Architecture changes

| Wallpaper | Revision |
|---|---|
| Queue Garden | Open crescent plinth, exposed event latches, offset index train and ticket optics. Each deployed leaf still records one actual completion. |
| Coral Cradle | Horseshoe nursery with removable radial cassettes. Short transfer gantry and compliant three-contact collar replace the generic arm and flat tray. |
| Tidal Loom | Staggered matched rotor cartridges, triangulated swept support, recoverable seabed shoes and one dedicated service side. |
| Presence Rig | Spatial roller deck, swept load columns, captive overhead tether reel and suit interfaces. Component views now show a roller cassette and mechanical release. |
| Sleep Cocoon | Shaped acoustic side petals, structural canopy ribs, headrest adjustment and rear air service. The existing shared seated mannequin remains; canopy clearance is measured from its actual mesh. |
| Wind Kite | Swept airfoil with canted tips and an exposed structural bay, stronger bridle attachments, and a compact outrigger-supported generator. |
| Meeting Buoy | Visible clockwork comparator and rack-driven semaphore. Separate microphone perimeter and reset paddle. The flag still cannot mute the room. |
| Manta Foil | Fine twin bows, raised passenger salon and recessed boarding access. Matched foil roots and longitudinal propulsors replace the blunt single-hull silhouette. |
| Seam Surgeon | Short pipe ends establish scale around a double orbital track. Preparation, filler-fed welding and trailing inspection now carry the drawing. Service views remove actual carriage covers. |
| Volumetric Stage | Deep trusses, seventeen optical heads, alignment gimbals, service ladders, coolant routes, haze distribution and shared timing. Quiet image contours replace the dominant field. |
| Aroma Organ | Unsupported receptor data replaced with a spatial metering bank and explicitly illustrative six-channel valve schedule. |
| Quiet Stair | Four independently guided vertical tread carriages, manual release, gate interlocks and a three-state sequence using the model's exact tread coordinates. |

## Corrections to explanatory content

- **Aroma Organ:** the random matrix labelled as an orange-peel response has
  been removed. The new inset explains fictional hardware addressing, explicitly
  showing six of 96 channels. It does not pretend to be biological receptor data.
  The original speculative synthesis targets remain in the narrative.
  Real olfaction uses combinations of receptor responses; a hardware recipe is
  not itself a validated perception model. See the primary
  [Nobel presentation of Axel and Buck's discoveries](https://www.nobelprize.org/prizes/medicine/2004/7422-nobelpriset-i-fysiologi-eller-medicin-2004/).
- **Quiet Stair:** the unsupported diagonal linkage has been replaced. Tread
  centres stay at x = −66, −22, 22, 66 model units; the tread width is 43, so a
  one-unit gap remains. Stair heights are 16, 33, 50, 67. Empty levelling brings
  all treads to 16; a locked level deck then travels to 67. The miniature
  elevation sequence uses those same numbers. Entry-gate logic is an explicit
  concept requirement, not a validated control system or certification.
- **Presence Rig / Stage:** existing fictional curve values are preserved but
  now labelled as illustrative or fictional on the sheet.
- Component captions change where the actual component changed. Original
  names, service years, stories, quantitative design targets and fictional
  service logs otherwise remain intact.

## Review and validation

- Every revised sheet checked in both native aspect ratios for text/geometry
  collisions, text overlaps, boundaries and unique A/B/C captions.
- Shared mannequin segment lengths checked by the existing capture routine.
  Presence feet use the measured sole minimum placed on the z=20 roller top.
  Sleep Cocoon's canopy clearance has a direct mesh-bound assertion.
- Quiet Stair endpoint equations and the level-state equality are checked and
  saved in `concepts/century/qa/quiet-stair-kinematics.json`. This does not replace
  a full collision, load, interlock or public-access engineering assessment.
- Visual QA includes every ultrawide sheet, compact contact sheets, native detail
  crops, and fullscreen browser review. A visible canopy collision and overly
  faint structural columns were corrected after the first visual pass.
- Before/after native hashes and resolutions are in `quality-redesign/review.json`.
  The three original-series compact BEFORE files were regenerated from untouched
  pre-edit source at the beginning of this pass because no matching compact
  development master existed. Ultrawide BEFORE files are exact current masters.

## Source and reproduction

- `tools/century/quality_geometry.py`: nine replacement device architectures.
- `tools/century/build.py`: chooses these architectures in place of the earlier
  recipe plus additive detail passes for the nine selected IDs.
- `tools/hardware3d/quality_scenes.py`: Presence Rig, Stage and Aroma metering bank.
- `tools/quality_panels.py`, `tools/leisure.py`: original-sheet composition.
- `tools/century/editorial_second.py`: corrected Quiet Stair state diagram.
- `tools/century/quality_review.py` and `.html`: before/after review.

```sh
blender -b --factory-startup -t 4 --python-exit-code 1 --python tools/century/build.py -- --ids 2,6,38,42,44,60,65,70,99 --force --maintenance
blender -b --factory-startup -t 4 --python-exit-code 1 --python tools/hardware3d/quality_scenes.py
python tools/century/render.py --ids 2,6,38,42,44,60,65,70,99 --force --maintenance
python tools/century/audit.py --ids 2,6,38,42,44,60,65,70,99
```

Original-series renders use `make_wallpapers.py --only 8`, `12`, `14`, with
separate `--out` directories and `--size 5120x2880` for the compact form.
Their local development masters are updated after review, not installed into
the active desktop theme. Never replace the frozen BEFORE files when rerunning.
