from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'tools'))
try:
    import cairo
    import numpy as np
    import settings_ui
except (ImportError, ValueError) as exc:  # GTK 4 / python-gobject missing
    settings_ui = None
    REASON = str(exc)

PLAN = dict(profile='big', optimal='big', label='16:9 · 3840 × 2160', setting='auto', setting_level='vivid',
            monitors=[dict(name='DP-1', width=3840, height=2160, scale=1)],
            options=[dict(profile='big', size=[3840, 2160]), dict(profile='small', size=[1920, 1080])],
            packs=[dict(profile='big', level=lv, set=f'big-{lv}', label='16:9 · 3840 × 2160', bytes=20_000_000,
                        local=lv == 'default') for lv in ('muted', 'default', 'vivid')])
DONE = {**PLAN, 'packs': [{**k, 'local': True} for k in PLAN['packs']]}


@unittest.skipIf(settings_ui is None, 'GTK 4 not available')
class SettingsUI(unittest.TestCase):
    def test_the_action_downloads_what_is_missing(self):
        self.assertEqual(settings_ui.action(PLAN), ('download', 40.0))
        self.assertEqual(settings_ui.keys(PLAN)[0][1], 'DOWNLOAD OPTIMAL · 40 MB')
        self.assertIsNone(settings_ui.action(DONE))
        self.assertEqual(settings_ui.keys(DONE), ((('ESC',), 'CLOSE'),))
        self.assertEqual(settings_ui.action({**DONE, 'setting': 'small'}), ('optimal', 0))

    def test_the_panel_fits_every_screen(self):
        many = {**PLAN, 'monitors': [dict(name=f'DP-{i}', width=1920, height=1080, scale=1) for i in range(6)]}
        for plan in (PLAN, DONE, many, {**PLAN, 'monitors': []}):
            for W, H in ((1920, 1080), (5120, 2160), (1080, 1920), (1280, 720), (1024, 768)):
                surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
                settings_ui.draw_settings(cairo.Context(surface), W, H, plan)
                alpha = np.ndarray((H, W, 4), np.uint8, surface.get_data())[..., 3]
                ys, xs = np.nonzero(alpha > 230)              # the panel, not the dimmed screen around it
                self.assertTrue(xs.min() > 0 and ys.min() > 0 and xs.max() < W - 1 and ys.max() < H - 1, (W, H))

    def test_enter_downloads_the_optimal_set_keeping_the_intensity(self):
        self.assertEqual(settings_ui.Menu(PLAN).key('Return'),
                         ('save', {'profile': 'auto', 'level': 'vivid', 'download': 'optimal'}))
        self.assertIsNone(settings_ui.Menu(DONE).key('Return'))          # nothing to do
        self.assertEqual(settings_ui.Menu({**DONE, 'setting': 'small'}).key('Return'),
                         ('save', {'profile': 'auto', 'level': 'vivid'}))   # back to the optimal set
        for name in ('Up', 'Down', 'Left', 'Right'):
            self.assertIsNone(settings_ui.Menu(PLAN).key(name))
        for name in ('Escape', 's'):
            self.assertEqual(settings_ui.Menu(PLAN).key(name), ('cancel', None))

    def test_progress_stays_in_its_box(self):
        for info in (dict(phase='download', done=0, total=22_000_000, label='21:9 · 5120 × 2160', level='vivid'),
                     dict(phase='download', done=22_000_000, total=22_000_000, label='16:9 · 2560 × 1440'),
                     dict(phase='install', done=1, total=1, label='32:9 · 5120 × 1440', level='muted')):
            for u in (0.7, 1.0, 2.0):
                W, H = (round(v*u) for v in settings_ui.PROGRESS_SIZE)
                surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W + 2, H + 2)
                cr = cairo.Context(surface)
                cr.translate(1, 1)
                for t in (0.0, 0.37):
                    settings_ui.draw_progress(cr, u, t, info)
                alpha = np.ndarray((H + 2, W + 2, 4), np.uint8, surface.get_data())[..., 3]
                self.assertEqual(int(alpha[0].max()) + int(alpha[-1].max()) + int(alpha[:, 0].max())
                                 + int(alpha[:, -1].max()), 0, (info['phase'], u))


if __name__ == '__main__':
    unittest.main()
