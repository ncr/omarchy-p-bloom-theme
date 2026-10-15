"""p(bloom) b01-b25: sincere machines (brief: docs/collection/BLOOM-TEN.md).

Each machine has two modules:
  bNN_slug.py        ENTRY (catalogue text), DOSSIER (field notes) and figure()
                     for the two side diagrams. Plain Python, no Blender.
  bNN_slug_model.py  build() -> (azimuth, elevation). Blender only, uses kit.

The series keeps its own registry (docs/bloom/catalog.json, written by
catalog.py) so the shared Century catalogue and the 42 existing sheets are
not touched. Internal numbers 201-225 only select the refined line weights
of draw_view; the printed series id is ENTRY['series'] (B01...B10).
"""
import importlib

MODULES = [
    'b01_canopy_seeder',
    'b02_reef_nursery',
    'b03_sun_still',
    'b04_first_light',
    'b05_cure_cabinet',
    'b06_gravity_shepherd',
    'b07_feeling_hand',
    'b08_bridge_walker',
    'b09_first_garden',
    'b10_library_beacon',
    'b11_clear_sight',
    'b12_wind_freighter',
    'b13_green_forge',
    'b14_night_train',
    'b15_whale_watch',
    'b16_fog_harp',
    'b17_ice_stupa',
    'b18_stellarator_hearth',
    'b19_sky_whale',
    'b20_quiet_scanner',
    'b21_crater_ear',
    'b22_half_moon_plough',
    'b23_mycelium_mason',
    'b24_carousel_lamp',
    'b25_first_postcard',
]


def module(name):
    return importlib.import_module('century.bloom.' + name)


def available():
    """Machines whose text module exists (the series is built incrementally)."""
    out = []
    for name in MODULES:
        try:
            out.append((name, module(name)))
        except ModuleNotFoundError as e:
            if e.name != 'century.bloom.' + name:
                raise
    return out


def ncr_numbers():
    """Permanent NCR ids from docs/collection/ncr-registry.json (b01 -> 111 ...)."""
    import json
    from pathlib import Path
    reg = Path(__file__).resolve().parents[3] / 'docs/collection/ncr-registry.json'
    return json.loads(reg.read_text())['bloom']


def entries(ids=None):
    """Entries in series order. ids: iterable of 'b01' style ids or ints 1-10."""
    want = None
    if ids:
        want = {('b%02d' % int(i)) if str(i).isdigit() else str(i).lower() for i in ids}
    out = []
    ncr = ncr_numbers()
    for name, mod in available():
        e = dict(mod.ENTRY)
        e['module'] = name
        e['ncr'] = ncr[e['id']]
        if want and e['id'] not in want:
            continue
        out.append(e)
    return out


def stem(entry):
    return f"{entry['id']}-{entry['slug']}"
