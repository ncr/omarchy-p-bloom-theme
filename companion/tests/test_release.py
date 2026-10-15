"""Wallpaper sets: per-file downloads and their verification, updates, offline fallback, real-matrix selection."""
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import wallpaper_profiles as wp

BASE = 'https://objects.test/p-bloom/'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def item(key, data):
    return dict(id=key, name=f'{key}.webp', sha256=sha(data), bytes=len(data))


class Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


class Download(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for p in (patch.dict(wp.os.environ, {'XDG_DATA_HOME': str(self.root/'data')}),
                  patch.object(wp, 'setup_path', return_value=self.root/'state/setup.json'),
                  patch.object(wp, 'notify_selection'), patch.object(wp.time, 'sleep')):
            p.start()
            self.addCleanup(p.stop)
        docs = self.root/'docs/collection'
        docs.mkdir(parents=True)
        (docs/'catalog.json').write_text(json.dumps({'finalized': [{'id': 'one'}, {'id': 'two'}]}))
        # the theme ships 1440's first wallpaper (the starter); 1440's second is only in the object store
        (self.root/'backgrounds').mkdir()
        (self.root/'backgrounds/one.webp').write_bytes(b'1440-one')
        self.images = {'one.webp': b'4k-one', 'two.webp': b'4k-two'}
        small = [item(key, f'1440-{key}'.encode()) for key in ('one', 'two')]
        # what the object store holds, by URL
        self.store = {f'{BASE}{sha(d)}.webp': d for d in (*self.images.values(), b'1440-one', b'1440-two')}
        self.manifest = {'default': '1440', 'objects_base': BASE, 'starter': dict(profile='1440', objects=small[:1]),
                         'profiles': [
            dict(id='1440', label='16:9 · 2560 × 1440', size=[2560, 1440], min_text_px=11,
                 packs=dict(default=dict(objects=small))),
            dict(id='4k', label='16:9 · 3840 × 2160', size=[3840, 2160], min_text_px=11,
                 packs=dict(default=dict(objects=[item(n.split('.')[0], d) for n, d in self.images.items()]))),
        ]}
        self.save()
        self.urls = []

    def save(self):
        (self.root/'docs/collection/profiles.json').write_text(json.dumps(self.manifest))

    def opener(self, fail=0):
        """The object store; the first `fail` requests break off like a dropped connection."""
        def open_(request, timeout):
            self.urls.append(request.full_url)
            if len(self.urls) <= fail:
                raise OSError('connection reset')
            if request.full_url not in self.store:
                raise OSError('HTTP Error 404: Not Found')
            return Response(self.store[request.full_url])
        return open_

    def change_two(self, data):
        """A new version of one wallpaper: published as a new object, named in the manifest."""
        self.store[f'{BASE}{sha(data)}.webp'] = data
        self.manifest['profiles'][1]['packs']['default']['objects'][1] = item('two', data)
        self.save()

    def test_objects_are_named_by_their_content(self):
        one = self.manifest['profiles'][1]['packs']['default']['objects'][0]
        self.assertEqual(wp.object_url(BASE, one), f"{BASE}{one['sha256']}.webp")
        for bad in (dict(one, name='../x.webp'), dict(one, name='x.exe'), dict(one, sha256='abc')):
            with self.assertRaises(ValueError):
                wp.object_url(BASE, bad)

    def test_verified_download_installs_the_set(self):
        seen = []
        with patch.object(wp, 'progress', lambda **info: seen.append(info)):
            target = wp.fetch(self.root, '4k', opener=self.opener())
        # the gallery's progress: bytes rising to the set's size, then installing
        total = sum(len(d) for d in self.images.values())
        self.assertEqual(seen[-1]['phase'], 'install')
        self.assertEqual(seen[0]['done'], 0)
        self.assertEqual(max(i['done'] for i in seen), total)
        self.assertTrue(all(i['total'] == total and i['level'] == 'default' for i in seen))
        self.assertEqual(sorted(self.urls), sorted(f'{BASE}{sha(d)}.webp' for d in self.images.values()))
        self.assertEqual({p.name: p.read_bytes() for p in target.iterdir() if p.name != wp.MARKER}, self.images)
        self.assertEqual((target/wp.MARKER).read_text().strip(), wp.set_digest(self.manifest['profiles'][1]['packs']['default']['objects']))
        screen = dict(name='DP-1', width=3840, height=2160, scale=1)
        p = wp.plan(self.root, detected=[screen])
        self.assertEqual((p['profile'], p['local']), ('4k', True))
        self.assertEqual([Path(f).parent for f in p['files']], [target, target])
        self.assertEqual([p.name for p in wp.sets_dir().iterdir()], ['4k'])  # no temporary leftovers

    def test_an_update_downloads_only_the_changed_files(self):
        target = wp.fetch(self.root, '4k', opener=self.opener())
        before = (target/'one.webp').stat().st_ino
        self.change_two(b'4k-two, fixed')
        screen = dict(name='DP-1', width=3840, height=2160, scale=1)
        self.assertFalse(wp.plan(self.root, detected=[screen])['local'])      # the set is out of date
        self.urls.clear()
        target = wp.fetch(self.root, '4k', opener=self.opener())
        self.assertEqual(self.urls, [f"{BASE}{sha(b'4k-two, fixed')}.webp"])
        self.assertEqual((target/'two.webp').read_bytes(), b'4k-two, fixed')
        self.assertEqual((target/'one.webp').stat().st_ino, before)              # reused, not copied
        self.assertTrue(wp.plan(self.root, detected=[screen])['local'])

    def test_a_dropped_connection_is_retried(self):
        target = wp.fetch(self.root, '4k', opener=self.opener(fail=1), workers=1)
        self.assertEqual(len(self.urls), 3)
        self.assertEqual({p.name: p.read_bytes() for p in target.iterdir() if p.name != wp.MARKER}, self.images)

    def test_checksum_mismatch_installs_nothing(self):
        url = f"{BASE}{sha(self.images['two.webp'])}.webp"
        self.store[url] = b'4k-twX'
        with self.assertRaisesRegex(ValueError, 'SHA-256'):
            wp.fetch(self.root, '4k', opener=self.opener())
        self.assertFalse((wp.sets_dir()/'4k').exists())
        self.assertEqual([p.name for p in wp.sets_dir().iterdir()], [])

    def test_oversized_download_is_refused(self):
        url = f"{BASE}{sha(self.images['two.webp'])}.webp"
        self.store[url] = self.images['two.webp'] + b'\0'*64
        with self.assertRaisesRegex(ValueError, 'larger'):
            wp.fetch(self.root, '4k', opener=self.opener())

    def test_a_failed_update_keeps_the_installed_set(self):
        target = wp.fetch(self.root, '4k', opener=self.opener())
        marker = (target/wp.MARKER).read_text()
        self.manifest['profiles'][1]['packs']['default']['objects'][1] = item('two', b'never published')
        self.save()
        with self.assertRaisesRegex(OSError, '404'):
            wp.fetch(self.root, '4k', opener=self.opener())
        self.assertEqual({p.name: p.read_bytes() for p in target.iterdir() if p.name != wp.MARKER}, self.images)
        self.assertEqual((target/wp.MARKER).read_text(), marker)

    def test_unsafe_names_are_refused(self):
        self.manifest['profiles'][1]['packs']['default']['objects'][0]['name'] = '../escape.webp'
        self.save()
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            wp.fetch(self.root, '4k', opener=self.opener())
        self.assertFalse((self.root/'escape.webp').exists())

    def test_the_starters_files_are_not_downloaded_again(self):
        # the set the starter comes from is put together from it and the files it lacks
        target = wp.fetch(self.root, '1440', opener=self.opener())
        self.assertEqual(self.urls, [f'{BASE}{sha(b"1440-two")}.webp'])
        self.assertEqual((target/'one.webp').read_bytes(), b'1440-one')

    def test_offline_shows_the_starter_and_backs_off(self):
        screen = dict(name='DP-1', width=3840, height=2160, scale=1)
        with patch.object(wp, 'fetch', side_effect=OSError('network is unreachable')) as fetch, \
             patch.object(wp, 'sync', return_value=False):
            p = wp.initialize(self.root, wp.plan(self.root, detected=[screen]))
            self.assertEqual((p['profile'], p['fallback'], p['starter']), ('1440', '4k', True))
            self.assertEqual(p['files'], [str(self.root/'backgrounds/one.webp')])
            self.assertIn('could not be downloaded', p['warnings'][0])
            self.assertIn('4k', wp.read_setup()['failed'])
            # Within the retry window the watcher does not try again.
            p = wp.initialize(self.root, wp.plan(self.root, detected=[screen]))
            self.assertEqual(p['profile'], '1440')
            self.assertEqual(fetch.call_count, 1)
            with patch.object(wp.time, 'time', return_value=wp.time.time()+wp.RETRY_SECONDS+1):
                wp.initialize(self.root, wp.plan(self.root, detected=[screen]))
            self.assertEqual(fetch.call_count, 2)

    def test_successful_download_is_used_for_the_desktop(self):
        screen = dict(name='DP-1', width=3840, height=2160, scale=1)
        real = wp.fetch
        with patch.object(wp, 'fetch', side_effect=lambda root, pid: real(root, pid, opener=self.opener())), \
             patch.object(wp, 'sync', return_value=False) as sync:
            p = wp.initialize(self.root, wp.plan(self.root, detected=[screen]))
        self.assertEqual((p['profile'], p['local']), ('4k', True))
        self.assertEqual(sync.call_args.args[0]['profile'], '4k')
        self.assertNotIn('4k', wp.read_setup().get('failed', {}))

    def test_no_monitor_never_downloads(self):
        with patch.object(wp, 'fetch') as fetch, patch.object(wp, 'sync', return_value=False):
            p = wp.initialize(self.root, wp.plan(self.root, detected=[]))
        fetch.assert_not_called()
        self.assertEqual(p['profile'], '1440')

    def test_a_missing_starter_is_reported(self):
        (self.root/'backgrounds/one.webp').unlink()
        with self.assertRaisesRegex(ValueError, 'Reinstall the theme'):
            wp.plan(self.root, detected=[], local_only=True)

    def test_prune_keeps_recent_sets(self):
        for i, name in enumerate(('a', 'b', 'c', 'd')):
            (wp.sets_dir()/name).mkdir(parents=True)
            wp.os.utime(wp.sets_dir()/name, (1000+i, 1000+i))
        wp.prune('a')
        self.assertEqual(sorted(p.name for p in wp.sets_dir().iterdir()), ['a', 'c', 'd'])

    def test_prune_keeps_the_optimal_sets_packs(self):
        # the packs never count towards the three recent sets, however old they are
        for i, name in enumerate(('opt-muted', 'opt-vivid', 'w', 'x', 'y', 'z')):
            (wp.sets_dir()/name).mkdir(parents=True)
            wp.os.utime(wp.sets_dir()/name, (1000+i, 1000+i))
        wp.prune('z', pinned=['opt-muted', 'opt', 'opt-vivid'])
        self.assertEqual(sorted(p.name for p in wp.sets_dir().iterdir()), ['opt-muted', 'opt-vivid', 'x', 'y', 'z'])


class PublishedMatrix(unittest.TestCase):
    """Selection over the real manifest, using its declared (not downloaded) sizes."""

    def setUp(self):
        self.manifest = json.loads((ROOT/'docs/collection/profiles.json').read_text())
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        p = patch.dict(wp.os.environ, {'XDG_DATA_HOME': temp.name})
        p.start()
        self.addCleanup(p.stop)

    def choose(self, *screens):
        rows = [dict(name=f'M{i}', width=w, height=h, scale=1) for i, (w, h) in enumerate(screens)]
        return wp.plan(ROOT, detected=rows)

    def test_manifest_is_complete_and_ships_the_starter(self):
        self.assertEqual(self.manifest['version'], 4)
        self.assertRegex(self.manifest['objects_base'], r'^https://[^ ]+/$')
        for p in self.manifest['profiles']:
            # exactly three packs per resolution: Muted, Default, Vivid
            self.assertEqual(list(p['packs']), ['muted', 'default', 'vivid'])
            for entry in p['packs'].values():
                self.assertEqual(len(entry['objects']), self.manifest['count'])
                for f in entry['objects']:
                    self.assertRegex(f['sha256'], r'^[0-9a-f]{64}$')
            self.assertGreaterEqual(p['min_text_px'], 11)
        # what the theme ships is exactly the starter: one wallpaper per background colour, from the default
        # profile's Default pack
        starter = self.manifest['starter']
        self.assertEqual(starter['profile'], self.manifest['default'])
        default = next(p for p in self.manifest['profiles'] if p['id'] == starter['profile'])
        self.assertLess({json.dumps(f) for f in starter['objects']},
                        {json.dumps(f) for f in default['packs']['default']['objects']})
        grounds = json.loads((ROOT/'docs/collection/palettes.json').read_text())['assignment_42']
        self.assertEqual(sorted(grounds[f['id']] for f in starter['objects']), sorted(set(grounds.values())))
        self.assertEqual({f['name'] for f in starter['objects']}, {p.name for p in (ROOT/'backgrounds').glob('*.webp')})
        for f in starter['objects']:
            self.assertEqual(sha((ROOT/'backgrounds'/f['name']).read_bytes()), f['sha256'])

    def test_nothing_downloaded_shows_the_starter(self):
        p = wp.plan(ROOT, detected=[], local_only=True)
        self.assertEqual((p['profile'], p['starter'], p['count']), (self.manifest['default'], True, 10))

    def test_every_common_screen_gets_its_own_set(self):
        expected = {
            (1920, 1080): '16x9-1080p', (2560, 1440): '16x9-1440p', (3840, 2160): '16x9-2160p',
            (5120, 2880): '16x9-2880p', (1366, 768): '16x9-1080p',
            (1920, 1200): '16x10-1200p', (2560, 1600): '16x10-1600p', (3840, 2400): '16x10-2400p',
            (2880, 1800): '16x10-2400p',
            (2256, 1504): '3x2-1504p', (2880, 1920): '3x2-1920p', (3000, 2000): '16x10-2400p',
            (1600, 1200): '4x3-1200p', (2048, 1536): '4x3-1536p', (1280, 1024): '4x3-1200p',
            (2560, 1080): '64x27-1080p', (5120, 2160): '64x27-2160p',
            (3440, 1440): '43x18-1440p', (3840, 1600): '12x5-1600p',
            (3840, 1080): '32x9-1080p', (5120, 1440): '32x9-1440p', (7680, 2160): '32x9-2160p',
        }
        for screen, profile in expected.items():
            with self.subTest(screen=screen):
                p = self.choose(screen)
                self.assertEqual(p['profile'], profile)
                self.assertFalse(next(o for o in p['options'] if o['profile'] == profile)['upscale'])

    def test_mixed_monitors_avoid_upscaling_everywhere(self):
        p = self.choose((2880, 1920), (3840, 2160))
        chosen = next(o for o in p['options'] if o['profile'] == p['profile'])
        self.assertFalse(chosen['upscale'])
        self.assertEqual(p['profile'], '16x10-2400p')
        p = self.choose((1920, 1080), (2560, 1440))
        self.assertEqual(p['profile'], '16x9-1440p')


if __name__ == '__main__':
    unittest.main()
