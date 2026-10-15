"""The installed app keeps itself in step with the theme checkout it was installed from."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import wallpaper_runtime as rt


class Refresh(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root, self.app = Path(temp.name)/'theme', Path(temp.name)/'app'
        (self.root/'tools').mkdir(parents=True)
        self.app.mkdir()
        for name in rt.RUNTIME:
            shutil.copy2(ROOT/'tools'/name, self.root/'tools'/name)
            shutil.copy2(ROOT/'tools'/name, self.app/name)

    def test_an_identical_copy_is_left_alone(self):
        (self.app/'__pycache__').mkdir()
        self.assertEqual(rt.stale(self.app, self.root), [])
        self.assertEqual(rt.refresh(self.app, self.root, quiet=0), [])
        self.assertTrue((self.app/'__pycache__').is_dir())

    def test_changed_files_are_copied_and_the_bytecode_dropped(self):
        (self.root/'tools/gallery.py').write_text('# new gallery\n')
        (self.app/'__pycache__').mkdir()
        self.assertEqual(rt.refresh(self.app, self.root, quiet=0), ['gallery.py'])
        self.assertEqual((self.app/'gallery.py').read_text(), '# new gallery\n')
        self.assertFalse((self.app/'__pycache__').exists())
        self.assertEqual([p.name for p in self.app.iterdir() if p.name.startswith('.')], [])
        self.assertEqual(rt.stale(self.app, self.root), [])

    def test_a_file_new_in_the_checkout_is_installed(self):
        listing = (self.root/'tools/wallpaper_runtime.py').read_text()
        (self.root/'tools/wallpaper_runtime.py').write_text(listing.replace("'wallpaper_runtime.py')",
                                                                            "'wallpaper_runtime.py', 'extra.py')"))
        (self.root/'tools/extra.py').write_text('X = 1\n')
        self.assertEqual(sorted(rt.refresh(self.app, self.root, quiet=0)), ['extra.py', 'wallpaper_runtime.py'])
        self.assertEqual((self.app/'extra.py').read_text(), 'X = 1\n')

    def test_only_listed_plain_names_are_copied(self):
        listing = (self.root/'tools/wallpaper_runtime.py').read_text()
        (self.root/'tools/wallpaper_runtime.py').write_text(listing.replace("'wallpaper_runtime.py')",
                                                                            "'wallpaper_runtime.py', '../evil.py')"))
        (self.root/'evil.py').write_text('boom\n')
        self.assertEqual(rt.refresh(self.app, self.root, quiet=0), ['wallpaper_runtime.py'])
        self.assertFalse((self.app.parent/'evil.py').exists())
        (self.root/'tools/other.py').write_text('not listed\n')
        self.assertEqual(rt.refresh(self.app, self.root, quiet=0), [])
        self.assertFalse((self.app/'other.py').exists())

    def test_nothing_is_copied_while_the_checkout_is_changing(self):
        (self.root/'tools/gallery.py').write_text('# half-way through a pull\n')
        self.assertEqual(rt.refresh(self.app, self.root), [])        # changed just now
        (self.root/'.git').mkdir()
        (self.root/'.git/index.lock').touch()
        self.assertEqual(rt.refresh(self.app, self.root, quiet=0), [])
        (self.root/'.git/index.lock').unlink()
        self.assertEqual(rt.refresh(self.app, self.root, quiet=0), ['gallery.py'])

    def test_a_broken_or_missing_checkout_keeps_the_installed_copy(self):
        (self.root/'tools/wallpaper_runtime.py').write_text('RUNTIME = (')
        (self.root/'tools/gallery.py').write_text('# new\n')
        self.assertEqual(rt.refresh(self.app, self.root, quiet=0), [])
        shutil.rmtree(self.root)
        self.assertEqual(rt.refresh(self.app, self.root, quiet=0), [])
        self.assertEqual((self.app/'gallery.py').read_bytes(), (ROOT/'tools/gallery.py').read_bytes())


class Launcher(unittest.TestCase):
    """view_wallpapers restarts into the refreshed copy only when it runs installed (outside the checkout)."""

    def setUp(self):
        import view_wallpapers
        self.vw = view_wallpapers

    def test_running_from_the_checkout_never_refreshes(self):
        with patch.dict(self.vw.os.environ, {'PBLOOM_THEME_ROOT': str(ROOT)}), \
                patch.object(rt, 'refresh') as refresh, patch.object(self.vw.os, 'execv') as execv:
            self.vw.follow_checkout()
        refresh.assert_not_called()
        execv.assert_not_called()

    def test_installed_copy_restarts_after_a_refresh(self):
        app = Path('/opt/p-bloom-app')
        with patch.dict(self.vw.os.environ, {'PBLOOM_THEME_ROOT': str(ROOT)}), \
                patch.object(self.vw, '__file__', str(app/'view_wallpapers.py')), \
                patch.object(rt, 'refresh', return_value=['gallery.py']) as refresh, \
                patch.object(self.vw.os, 'execv') as execv:
            self.vw.follow_checkout()
        refresh.assert_called_once_with(app, self.vw.ROOT)
        self.assertEqual(execv.call_args[0][1][1], str(app/'view_wallpapers.py'))

    def test_installed_copy_in_step_does_not_restart(self):
        with patch.dict(self.vw.os.environ, {'PBLOOM_THEME_ROOT': str(ROOT)}), \
                patch.object(self.vw, '__file__', '/opt/p-bloom-app/view_wallpapers.py'), \
                patch.object(rt, 'refresh', return_value=[]), patch.object(self.vw.os, 'execv') as execv:
            self.vw.follow_checkout()
        execv.assert_not_called()


if __name__ == '__main__':
    unittest.main()
