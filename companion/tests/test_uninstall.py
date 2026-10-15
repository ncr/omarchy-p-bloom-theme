"""Removing the companion: by its installer, and by itself when the theme is gone (Omarchy's Remove > Theme)."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'tools'))
import wallpaper_desktop
import wallpaper_uninstall as wu


class Uninstall(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        for p in (patch.dict(os.environ, {'HOME': str(self.home), 'XDG_DATA_HOME': str(self.home/'.local/share'),
                                          'XDG_STATE_HOME': str(self.home/'.local/state')}),
                  patch.object(wu.subprocess, 'run'), patch.object(wu, 'notify')):
            p.start()
            self.addCleanup(p.stop)
        self.prefix = self.home/'.local'
        p = wu.paths(self.prefix)
        p['app'].mkdir(parents=True)
        for name in wu.RUNTIME:
            (p['app']/name).write_text('#')
        (p['app']/'install.json').write_text('{}')
        (p['app']/'sets/16x9-1440p').mkdir(parents=True)
        p['launcher'].parent.mkdir(parents=True)
        p['launcher'].write_text('#!/bin/sh\n' + wu.MARKER + '\n')
        p['desktop'].parent.mkdir(parents=True)
        p['desktop'].write_text('[Desktop Entry]\nStartupWMClass=p-bloom-wallpapers\n')
        for icon in p['icons']:
            icon.parent.mkdir(parents=True)
            icon.write_bytes(b'png')
        p['service'].parent.mkdir(parents=True)
        p['service'].write_text(wu.MARKER + '\n[Unit]\n')
        p['hook'].parent.mkdir(parents=True)
        p['hook'].write_text('#!/bin/sh\n' + wu.MARKER + '\n')
        self.state = self.home/'.local/state/p-bloom-wallpapers'
        self.state.mkdir(parents=True)
        (self.state/'setup.json').write_text('{}')
        self.p = p

    def gone(self):
        p = self.p
        return not any(x.exists() for x in (p['app'], p['launcher'], p['desktop'], p['service'], p['hook'], *p['icons']))

    def test_uninstall_keeps_downloads_and_settings_unless_purged(self):
        foreign = self.p['desktop'].parent/'other.desktop'
        foreign.write_text('[Desktop Entry]\n')
        wu.remove(self.prefix)
        self.assertTrue((self.p['app']/'sets/16x9-1440p').is_dir() and (self.state/'setup.json').is_file())
        self.assertFalse(any(x.exists() for x in (self.p['launcher'], self.p['service'], self.p['hook'], *self.p['icons'])))
        self.assertTrue(foreign.exists())
        wu.remove(self.prefix, purge=True)
        self.assertTrue(self.gone() and not self.state.exists())

    def test_the_service_removes_the_app_once_the_theme_has_been_gone_a_minute(self):
        clock = [1000.0]
        def sleep(seconds):
            clock[0] += seconds
        app_file = self.p['app']/'wallpaper_desktop.py'
        with patch.object(wallpaper_desktop.time, 'time', side_effect=lambda: clock[0]), \
             patch.object(wallpaper_desktop.time, 'sleep', side_effect=sleep), \
             patch.object(wallpaper_desktop, '__file__', str(app_file)), \
             patch.object(sys, 'argv', ['wallpaper_desktop.py', '--root', str(self.home/'gone-theme')]):
            wallpaper_desktop.main()
        self.assertGreaterEqual(clock[0] - 1000, 60)                # waited out a reinstall first
        self.assertTrue(self.gone() and not self.state.exists())
        wu.notify.assert_called_once()
        disable = [c.args[0] for c in wu.subprocess.run.call_args_list if 'disable' in c.args[0]]
        self.assertEqual(disable, [['systemctl', '--user', 'disable', wu.SERVICE]])   # not --now: it is the caller


if __name__ == '__main__':
    unittest.main()
