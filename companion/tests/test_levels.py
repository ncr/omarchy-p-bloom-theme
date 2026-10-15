"""Background levels (Muted / Default / Vivid): manifest, selection, download, fallback."""
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import wallpaper_profiles as wp


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


BASE = 'https://objects.test/p-bloom/'
SCREEN = dict(name='DP-1', width=3840, height=2160, scale=1)


class Levels(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.real_notify = wp.notify_selection
        for p in (patch.dict(wp.os.environ, {'XDG_DATA_HOME': str(self.root/'data')}),
                  patch.object(wp, 'setup_path', return_value=self.root/'state/setup.json'),
                  patch.object(wp, 'notify_selection')):
            p.start()
            self.addCleanup(p.stop)
        docs = self.root/'docs/collection'
        docs.mkdir(parents=True)
        (docs/'catalog.json').write_text(json.dumps({'finalized': [{'id': 'one'}, {'id': 'two'}]}))
        # 1440 publishes only Default; the theme's backgrounds/ holds its first wallpaper (the starter).
        (self.root/'backgrounds').mkdir()
        (self.root/'backgrounds/one.webp').write_bytes(b'1440-one')
        default_only = [dict(id=k, name=f'{k}.webp', sha256=sha(f'1440-{k}'.encode()), bytes=8) for k in ('one', 'two')]
        self.images, self.store, files = {}, {}, {}
        self.store.update({f'{BASE}{sha(f"1440-{k}".encode())}.webp': f'1440-{k}'.encode() for k in ('one', 'two')})
        for level in ('default', 'muted', 'vivid'):
            self.images[level] = {f'{k}.webp': f'4k-{level}-{k}'.encode() for k in ('one', 'two')}
            files[level] = [dict(id=n.split('.')[0], name=n, sha256=sha(d), bytes=len(d))
                            for n, d in self.images[level].items()]
            self.store.update({f'{BASE}{sha(d)}.webp': d for d in self.images[level].values()})
        self.manifest = {'default': '1440', 'objects_base': BASE,
                         'starter': dict(profile='1440', objects=default_only[:1]), 'profiles': [
            dict(id='1440', label='16:9 · 2560 × 1440', size=[2560, 1440], min_text_px=11,
                 packs=dict(default=dict(objects=default_only))),
            dict(id='4k', label='16:9 · 3840 × 2160', size=[3840, 2160], min_text_px=11,
                 packs={level: dict(objects=files[level], min_text_px=11) for level in wp.LEVELS}),
        ]}
        self.save()
        self.urls = []

    def save(self):
        (self.root/'docs/collection/profiles.json').write_text(json.dumps(self.manifest))

    def opener(self, request, timeout):
        self.urls.append(request.full_url)
        if request.full_url not in self.store:
            raise OSError('HTTP Error 404: Not Found')
        return Response(self.store[request.full_url])

    def fake_fetch(self, fail=()):
        """fetch() from the test objects; levels in `fail` behave like a 404."""
        real = wp.fetch

        def fetch(root, pid, level='default'):
            if level in fail:
                raise OSError('HTTP Error 404: Not Found')
            return real(root, pid, opener=self.opener, level=level, attempts=1)
        return fetch

    # -- manifest ------------------------------------------------------------

    def test_manifest_levels_resolve_to_their_own_files_and_folder(self):
        _, every = wp.profiles(self.root, 'vivid')
        four = next(p for p in every if p['id'] == '4k')
        self.assertEqual((four['level'], four['level_missing'], four['local']), ('vivid', False, False))
        self.assertEqual({f['sha256'] for f in four['files']}, {sha(d) for d in self.images['vivid'].values()})
        self.assertEqual({p.parent for p in four['paths']}, {wp.sets_dir()/'4k-vivid'})
        self.assertNotIn('packs', four)
        # 1440 publishes no Vivid files: offered at Default, marked.
        default_only = next(p for p in every if p['id'] == '1440')
        self.assertEqual((default_only['level'], default_only['level_missing'], default_only['local']),
                         ('default', True, False))

    def test_unknown_level_means_default_and_broken_level_entry_is_refused(self):
        _, every = wp.profiles(self.root, 'neon')
        self.assertTrue(all(p['level'] == 'default' for p in every))
        self.manifest['profiles'][1]['packs']['muted'] = {'files': [], 'archive': {}}
        self.save()
        with self.assertRaisesRegex(ValueError, 'Invalid muted set'):
            wp.profiles(self.root, 'muted')

    def test_level_does_not_change_the_resolution_choice(self):
        for level in wp.LEVELS:
            p = wp.plan(self.root, detected=[SCREEN], level=level)
            self.assertEqual((p['profile'], p['level'], p['set']), ('4k', level, wp.set_name('4k', level)))
            self.assertEqual(p['warnings'], [])

    # -- download ------------------------------------------------------------

    def test_level_downloads_into_its_own_set(self):
        target = wp.fetch(self.root, '4k', opener=self.opener, level='muted')
        self.assertEqual(target, wp.sets_dir()/'4k-muted')
        self.assertEqual(sorted(self.urls), sorted(f'{BASE}{sha(d)}.webp' for d in self.images['muted'].values()))
        self.assertEqual({p.name: p.read_bytes() for p in target.iterdir() if p.name != wp.MARKER}, self.images['muted'])
        p = wp.plan(self.root, detected=[SCREEN], level='muted')
        self.assertTrue(p['local'])
        # The Default set of the same profile is a different folder, still absent.
        self.assertFalse(wp.plan(self.root, detected=[SCREEN])['local'])

    def test_level_files_are_checked_against_their_own_hashes(self):
        # Vivid's objects served with Muted's bytes (the same size): refused, nothing installed
        for name, data in self.images['vivid'].items():
            self.store[f'{BASE}{sha(data)}.webp'] = self.images['muted'][name]
        with self.assertRaisesRegex(ValueError, 'SHA-256'):
            wp.fetch(self.root, '4k', opener=self.opener, level='vivid', attempts=1)
        self.assertFalse((wp.sets_dir()/'4k-vivid').exists())

    def test_unpublished_level_cannot_be_fetched(self):
        with self.assertRaisesRegex(ValueError, 'No Muted background'):
            wp.fetch(self.root, '1440', opener=self.opener, level='muted')

    # -- settings and fallback -----------------------------------------------

    def test_changing_the_level_downloads_that_set_and_is_remembered(self):
        with patch.object(wp, 'fetch', side_effect=self.fake_fetch()), \
             patch.object(wp, 'sync', return_value=True) as sync, \
             patch.object(wp, 'announce', return_value={'profile': 'auto', 'level': 'vivid'}):
            p = wp.initialize(self.root, wp.plan(self.root, detected=[SCREEN]), configure=True)
        self.assertEqual((p['profile'], p['level'], p['local']), ('4k', 'vivid', True))
        self.assertEqual(Path(sync.call_args.args[0]['files'][0]).parent, wp.sets_dir()/'4k-vivid')
        saved = wp.read_setup()
        self.assertEqual((saved['level'], saved['selected_level'], saved['profile']), ('vivid', 'vivid', 'auto'))
        self.assertEqual(wp.saved_level(saved, self.root), 'vivid')
        # Later launches and the desktop watcher keep the level without asking.
        with patch.object(wp, 'fetch', side_effect=AssertionError('already installed')), \
             patch.object(wp, 'sync', return_value=False):
            p = wp.initialize(self.root, wp.plan(self.root, detected=[SCREEN]))
        self.assertEqual(p['level'], 'vivid')

    def test_settings_screen_gets_every_levels_resolution_list(self):
        wp.fetch(self.root, '4k', opener=self.opener, level='muted')
        seen = {}
        def announce(p, desktop):
            seen.update(p)
            return None
        with patch.object(wp, 'fetch', side_effect=OSError('offline')), patch.object(wp, 'sync', return_value=False), \
             patch.object(wp, 'announce', side_effect=announce):
            wp.initialize(self.root, wp.plan(self.root, detected=[SCREEN]), configure=True)
        local = {lv: {o['profile']: o['local'] for o in opts} for lv, opts in seen['options_by_level'].items()}
        self.assertEqual(local['muted']['4k'], True)
        self.assertEqual(local['vivid']['4k'], False)
        self.assertEqual(set(local), set(wp.LEVELS))

    def test_download_optimal_fetches_every_intensity_of_the_optimal_set(self):
        seen = {}
        def announce(p, desktop):
            seen.update(p)
            return {'profile': 'auto', 'level': 'default', 'download': 'optimal'}
        progress = []
        with patch.object(wp, 'fetch', side_effect=self.fake_fetch(fail=('vivid',))), \
             patch.object(wp, 'sync', return_value=False), patch.object(wp, 'announce', side_effect=announce), \
             patch.object(wp, 'progress', lambda **info: progress.append(info)):
            p = wp.initialize(self.root, wp.plan(self.root, detected=[SCREEN]), configure=True)
        # the menu is told the set in use and its packs, one per intensity (Default came with the first start)
        self.assertEqual(seen['optimal'], '4k')
        self.assertEqual([(k['set'], k['local']) for k in seen['packs']],
                         [('4k-muted', False), ('4k', True), ('4k-vivid', False)])
        # every pack is fetched; one that fails is reported, the others stay
        self.assertTrue((wp.sets_dir()/'4k').is_dir() and (wp.sets_dir()/'4k-muted').is_dir())
        self.assertFalse((wp.sets_dir()/'4k-vivid').exists())
        self.assertTrue(any('Vivid set could not be downloaded' in w for w in p['warnings']))
        self.assertEqual({(i['pack'], i['packs']) for i in progress if 'pack' in i}, {(1, 2)})  # Vivid fails at once
        saved = wp.read_setup()
        self.assertEqual((saved['profile'], saved['level']), ('auto', 'default'))
        self.assertEqual(saved['pinned'], ['4k-muted', '4k', '4k-vivid'])

    def test_old_string_setting_keeps_the_current_level(self):
        with patch.object(wp, 'fetch', side_effect=self.fake_fetch()), patch.object(wp, 'sync', return_value=False), \
             patch.object(wp, 'announce', return_value='1440'):
            p = wp.initialize(self.root, wp.plan(self.root, detected=[SCREEN]), configure=True, level='muted')
        # 1440 publishes no Muted set: its Default is used, with a warning.
        self.assertEqual((p['profile'], p['level']), ('1440', 'default'))
        self.assertIn('Muted background is not published', ' '.join(p['warnings']))
        self.assertEqual(wp.read_setup()['level'], 'muted')

    def test_invalid_level_setting_is_refused(self):
        with patch.object(wp, 'fetch', side_effect=self.fake_fetch()), patch.object(wp, 'sync', return_value=False), \
             patch.object(wp, 'announce', return_value={'profile': 'auto', 'level': 'neon'}):
            with self.assertRaisesRegex(ValueError, 'Invalid wallpaper setting'):
                wp.initialize(self.root, wp.plan(self.root, detected=[SCREEN]), configure=True)

    def test_missing_level_set_keeps_the_current_set_and_retries(self):
        with patch.object(wp, 'fetch', side_effect=self.fake_fetch()), patch.object(wp, 'sync', return_value=False):
            p = wp.initialize(self.root, wp.plan(self.root, detected=[SCREEN]))
        self.assertEqual((p['profile'], p['level']), ('4k', 'default'))
        fetch = self.fake_fetch(fail=('vivid',))
        with patch.object(wp, 'fetch', side_effect=fetch) as calls, patch.object(wp, 'sync', return_value=False) as sync:
            p = wp.initialize(self.root, wp.plan(self.root, detected=[SCREEN]), level='vivid')
            # The 4k Default set already on the desktop stays; nothing else is fetched.
            self.assertEqual((p['profile'], p['level'], p['fallback']), ('4k', 'default', '4k-vivid'))
            self.assertIn('Vivid background, set could not be downloaded', p['warnings'][0])
            self.assertEqual(Path(sync.call_args.args[0]['files'][0]).parent, wp.sets_dir()/'4k')
            self.assertIn('4k-vivid', wp.read_setup()['failed'])
            self.assertEqual(wp.read_setup()['level'], 'vivid')
            wp.initialize(self.root, wp.plan(self.root, detected=[SCREEN]))
            self.assertEqual(calls.call_count, 1)  # within the retry window
            with patch.object(wp.time, 'time', return_value=wp.time.time()+wp.RETRY_SECONDS+1):
                wp.initialize(self.root, wp.plan(self.root, detected=[SCREEN]))
            self.assertEqual(calls.call_count, 2)

    def test_offline_first_choice_falls_back_to_the_starter(self):
        with patch.object(wp, 'fetch', side_effect=OSError('network is unreachable')), \
             patch.object(wp, 'sync', return_value=False):
            p = wp.initialize(self.root, wp.plan(self.root, detected=[SCREEN]), level='muted')
        self.assertEqual((p['profile'], p['level'], p['requested_level'], p['starter']), ('1440', 'default', 'muted', True))
        self.assertEqual(p['files'], [str(self.root/'backgrounds/one.webp')])
        self.assertIn("using the theme's own 1 wallpapers", p['warnings'][0])

    def test_notification_names_the_level(self):
        with patch.object(wp.shutil, 'which', side_effect=lambda name: '/usr/bin/'+name), \
             patch.object(wp.subprocess, 'run') as run:
            self.real_notify(dict(size=[3840, 2160], profile='4k', recommended='4k', level='vivid'), True)
        self.assertTrue(any('Vivid background' in x for x in run.call_args.args[0]))

if __name__ == '__main__':
    unittest.main()
