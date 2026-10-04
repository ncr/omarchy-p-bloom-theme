import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import wallpaper_profiles as wp
import wallpaper_desktop as wd


class Profiles(unittest.TestCase):
    def setUp(self):
        notify=patch.object(wp,'notify_selection')
        self.notify=notify.start()
        self.addCleanup(notify.stop)
        # Hermetic: no test reaches the network unless it injects an opener.
        offline=patch.object(wp,'fetch',side_effect=OSError('offline'))
        self.fetch=offline.start()
        self.addCleanup(offline.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        state=patch.object(wp,'setup_path',return_value=self.root/'state/setup.json')
        state.start()
        self.addCleanup(state.stop)
        docs = self.root/'docs/collection'
        docs.mkdir(parents=True)
        (docs/'catalog.json').write_text(json.dumps({'finalized': [{'id': 'one'}, {'id': 'two'}]}))
        data=patch.dict(wp.os.environ,{'XDG_DATA_HOME':str(self.root/'data')})
        data.start()
        self.addCleanup(data.stop)
        self.manifest = {'default': '16-9', 'profiles': []}
        # 16-9 is the bundled set in backgrounds/; wide is an installed download.
        for name, size in [('wide', [5120, 2160]), ('16-9', [5120, 2880])]:
            entries = []
            folder = self.root/'backgrounds' if name == '16-9' else wp.sets_dir()/name
            folder.mkdir(parents=True, exist_ok=True)
            for id in ['one', 'two']:
                path = folder/f'{id}.webp'
                path.write_bytes(f'{name}-{id}'.encode())
                entries.append(dict(id=id, name=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(), bytes=path.stat().st_size))
            if name != '16-9':
                (folder/wp.MARKER).write_text(wp.set_digest(entries))  # installed from the files the manifest names
            self.manifest['profiles'].append(dict(id=name, label=name, files=entries, packs=dict(default=dict(objects=entries)), size=size,
                                                  min_text_px=14, bundled=name == '16-9'))
        self.save()

    def save(self):
        (self.root/'docs/collection/profiles.json').write_text(json.dumps(self.manifest))

    def screen(self, w=1920, h=1080):
        return dict(name='DP-1', width=w, height=h, scale=1, focused=True)

    def plan(self, **kwargs):
        return wp.plan(self.root, detected=[self.screen()], **kwargs)

    def test_selection_and_honest_readability(self):
        p = self.plan()
        self.assertEqual(p['profile'], '16-9')
        self.assertIn('5.2 screen pixels', p['warnings'][0])
        self.assertEqual(wp.plan(self.root, detected=[self.screen(5120, 2160)])['profile'], 'wide')
        self.assertEqual(self.plan(requested='wide')['profile'], 'wide')
        self.assertEqual(wp.plan(self.root, detected=[])['profile'], '16-9')
        self.assertEqual(wp.plan(self.root, detected=[self.screen(5120, 2880)])['warnings'], [])

    def test_normalize_rotation_scaling_invalid(self):
        rows = [dict(name='portrait', width=2560, height=1440, scale=1.5, transform=1),
                dict(name='off', width=1920, height=1080, disabled=True), {}, None,
                dict(name='FALLBACK', width=1920, height=1080),
                dict(name='bad', width=1920, height=1080, scale=float('nan'))]
        self.assertEqual(wp.normalize_monitors(rows), [dict(name='portrait', width=1440, height=2560, scale=1.5, focused=False)])

    def test_all_monitors_and_manual(self):
        a, b = self.screen(), {**self.screen(5120,2160), 'name':'DP-2', 'focused':False}
        self.assertEqual(wp.plan(self.root, detected=[b,a])['profile'], 'wide')
        self.assertEqual(wp.plan(self.root, detected=[a,b], monitor='DP-2')['profile'], 'wide')
        with self.assertRaisesRegex(ValueError, 'not connected'):
            self.plan(monitor='missing')

    def test_focus_and_order_do_not_change_recommendation(self):
        a, b = self.screen(), {**self.screen(5120,2160), 'name':'DP-2', 'focused':False}
        p = wp.plan(self.root, detected=[a,b])
        a['focused'], b['focused'] = False, True
        self.assertEqual(wp.plan(self.root, detected=[b,a])['recommended'], p['recommended'])

    def test_largest_monitor_prevents_low_resolution_choice(self):
        self.add_sized_profile('1080-test', [1920,1080], 1)
        screens = [self.screen(), {**self.screen(3840,2160), 'name':'DP-2'}]
        p = wp.plan(self.root, detected=screens)
        self.assertEqual(p['recommended'], '16-9')
        low_result = next(x for x in p['options'] if x['profile']=='1080-test')
        self.assertTrue(low_result['upscale'])
        self.assertEqual(low_result['displays'][1]['factor'], 2)
        self.assertFalse(p['options'][0]['upscale'])

    def add_sized_profile(self, id, dimensions, bytes_per_file, installed=True):
        entries = []
        folder = wp.sets_dir()/id
        for key in ['one', 'two']:
            data = b'x'*bytes_per_file
            if installed:
                folder.mkdir(parents=True, exist_ok=True)
                (folder/f'{key}.webp').write_bytes(data)
            entries.append(dict(id=key, name=f'{key}.webp', bytes=bytes_per_file,
                                sha256=hashlib.sha256(data).hexdigest()))
        if installed:
            (folder/wp.MARKER).write_text(wp.set_digest(entries))
        self.manifest['profiles'].append(dict(id=id, label=id, packs=dict(default=dict(objects=entries)), size=dimensions,
                                              min_text_px=11))
        self.save()

    def test_smallest_sufficient_set_for_every_monitor(self):
        # Sizes are controlled test data: 1080p < 4K < 5K.
        self.add_sized_profile('1080', [1920,1080], 1)
        self.add_sized_profile('4k', [3840,2160], 3)
        self.assertEqual(self.plan()['recommended'], '1080')
        screens = [self.screen(), {**self.screen(3840,2160), 'name':'DP-2'}]
        p = wp.plan(self.root, detected=screens)
        self.assertEqual(p['recommended'], '4k')
        self.assertFalse(p['options'][0]['upscale'])

    def test_a_set_from_an_older_manifest_is_fetched_again(self):
        # after a theme update the old files are still on disk, but the manifest names other files
        self.add_sized_profile('4k', [3840,2160], 3)
        screens = [{**self.screen(3840,2160), 'name':'DP-2'}]
        self.assertTrue(next(o for o in wp.plan(self.root, detected=screens)['options'] if o['profile']=='4k')['local'])
        (wp.sets_dir()/'4k'/wp.MARKER).write_text('1'*64)
        self.assertFalse(next(o for o in wp.plan(self.root, detected=screens)['options'] if o['profile']=='4k')['local'])
        (wp.sets_dir()/'4k'/wp.MARKER).unlink()
        self.assertFalse(next(o for o in wp.plan(self.root, detected=screens)['options'] if o['profile']=='4k')['local'])

    def test_file_sizes_are_measured_not_estimated(self):
        self.add_sized_profile('4k', [3840,2160], 1234)
        option = next(o for o in self.plan()['options'] if o['profile']=='4k')
        self.assertEqual(option['total_bytes'], 2468)
        self.assertEqual(option['average_bytes'], 1234)
        self.assertEqual(option['file_count'], 2)
        (wp.sets_dir()/'4k/one.webp').write_bytes(b'x'*4321)
        option = next(o for o in self.plan()['options'] if o['profile']=='4k')
        self.assertEqual(option['total_bytes'], 5555)

    def test_equal_file_sizes_prefer_fewer_sufficient_pixels(self):
        self.add_sized_profile('4k', [3840,2160], 8)  # Same bytes as 16-9 fixture.
        self.assertEqual(self.plan()['recommended'], '4k')

    def test_tiny_cropped_set_does_not_beat_full_sheet(self):
        self.add_sized_profile('tiny-wide', [5120,2160], 1)
        self.assertEqual(self.plan()['recommended'], '16-9')

    def test_more_than_two_screens_and_portrait_crop(self):
        screens = [self.screen(), {**self.screen(3840,2160), 'name':'DP-2'},
                   {**self.screen(1080,1920), 'name':'DP-3'},
                   {**self.screen(3440,1440), 'name':'DP-4'}]
        p = wp.plan(self.root, detected=screens)
        self.assertTrue(all(len(o['displays'])==4 for o in p['options']))
        self.assertGreater(p['options'][0]['displays'][2]['crop'], .5)

    def test_when_all_are_too_small_choose_least_enlargement(self):
        p = wp.plan(self.root, detected=[self.screen(7680,4320)])
        self.assertTrue(all(o['upscale'] for o in p['options']))
        self.assertEqual(p['recommended'], '16-9')
        self.assertEqual(p['options'][0]['displays'][0]['factor'], 1.5)

    def test_previous_biggest_policy_migrates_to_optimal(self):
        self.add_sized_profile('1080', [1920,1080], 1)
        p = wp.plan(self.root, requested='biggest', detected=[self.screen()])
        self.assertEqual(p['profile'], '16-9')
        previous=dict(version=4,root=str(self.root),profile='biggest')
        with patch.object(wp, 'read_setup', return_value=previous), patch.object(wp, 'announce', return_value='auto') as announce, \
             patch.object(wp, 'sync',return_value=False) as sync, patch.object(wp, 'save_setup') as save:
            result = wp.initialize(self.root, p, requested='biggest')
            self.assertEqual(result['profile'], '1080')
            announce.assert_not_called()
            self.assertEqual(sync.call_args.args[0]['profile'], '1080')
            self.assertEqual(save.call_args.args[0]['profile'], 'auto')
            self.assertEqual(save.call_args.args[0]['version'],6)

    def test_reason_explains_larger_file_and_biggest_keeps_proportions(self):
        self.add_sized_profile('cheap-wide', [5120,2160], 1)
        self.assertIn('crops 25%', self.plan()['reason'])
        self.assertIn('whole sheet', self.plan()['reason'])
        p = wp.plan(self.root, requested='biggest', detected=[self.screen(5120,2160)])
        self.assertIn(p['profile'], ('wide', 'cheap-wide'))

    def test_incomplete_download_not_mixed_and_escape_rejected(self):
        (wp.sets_dir()/'wide/one.webp').unlink()
        p = wp.plan(self.root, detected=[self.screen(5120, 2160)])
        self.assertEqual(p['profile'], 'wide')
        self.assertFalse(p['local'])
        self.assertEqual(wp.plan(self.root, detected=[self.screen(5120, 2160)], local_only=True)['profile'], '16-9')
        self.manifest['profiles'][0]['files'][0]['name'] = '../outside.webp'
        self.save()
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            self.plan()

    def stage(self):
        current = self.root/'current'
        dest = current/'theme/backgrounds'
        dest.mkdir(parents=True)
        (current/'theme.name').write_text('p-bloom\n')
        (dest/'one.webp').write_bytes(b'old')
        (dest/'custom.webp').write_bytes(b'keep')
        (current/'background').symlink_to(dest/'one.webp')
        return current, dest

    def test_desktop_watcher_updates_without_gallery_and_on_monitor_change(self):
        current,dest=self.stage()
        screens=[self.screen()]
        watcher=wd.DesktopWatcher(self.root)
        with patch.object(wp,'current_dir',return_value=current), patch.object(wp,'monitors',side_effect=lambda:screens), patch.object(wp,'refresh_desktop') as refresh, patch.object(wp,'announce',side_effect=AssertionError('No gallery setup allowed')):
            self.assertTrue(watcher.tick())
            self.assertEqual((dest/'one.webp').read_bytes(),b'16-9-one')
            self.assertFalse(watcher.tick())
            self.assertEqual(refresh.call_count,1)
            screens[0]['focused']=False
            self.assertFalse(watcher.tick())
            screens[:]=[self.screen(5120,2160)]
            self.assertTrue(watcher.tick())
            self.assertEqual((dest/'one.webp').read_bytes(),b'wide-one')
            self.assertEqual((current/'background').resolve(),dest/'one.webp')
            self.assertEqual((dest/'custom.webp').read_bytes(),b'keep')
            self.assertEqual(refresh.call_count,2)
            screens.clear()
            self.assertFalse(watcher.tick())
            screens[:]=[self.screen()]
            self.assertTrue(watcher.tick())
            self.assertEqual((dest/'one.webp').read_bytes(),b'16-9-one')

    def test_sync_preserves_custom_and_selected_idempotently(self):
        current, dest = self.stage()
        with patch.object(wp,'refresh_desktop') as run:
            self.assertTrue(wp.sync(self.plan(), current))
            self.assertEqual(run.call_args.args[0],dest/'one.webp')
            self.assertFalse(wp.sync(self.plan(), current))
            self.assertEqual(run.call_count, 1)
        self.assertEqual((dest/'custom.webp').read_bytes(), b'keep')
        self.assertEqual((dest/'one.webp').read_bytes(), b'16-9-one')
        self.assertFalse((dest/'one.webp').is_symlink())

    def test_refresh_uses_uncached_snapshot_and_preserves_canonical_path(self):
        current,dest=self.stage()
        target=dest/'one.webp'
        calls=[]
        def run(args,**kwargs):
            calls.append(args)
            if 'themeTransition' in args:
                snapshot=Path(args[6])
                self.assertNotEqual(snapshot,target)
                self.assertEqual(snapshot.read_bytes(),target.read_bytes())
                self.assertEqual(args[7],str(target))
            return subprocess.CompletedProcess(args,0)
        with patch.object(wp.shutil,'which',return_value='/usr/bin/omarchy-shell'),patch.object(wp.subprocess,'run',side_effect=run),patch.object(wp.time,'sleep'):
            wp.refresh_desktop(target,current)
        self.assertEqual(calls[0],['omarchy','theme','bg','set',str(target)])
        self.assertEqual(len(calls),2)

    def test_refresh_sends_the_staged_theme_colors_and_shell(self):
        # An empty shell payload makes the shell drop the theme's bar, menu and lock styling (#1)
        current,dest=self.stage()
        (current/'theme/colors.toml').write_text('accent = "#4cc9ff"\n')
        (current/'theme/shell.toml').write_text('[bar]\nbackground-alpha = 0.90\n')
        calls=[]
        def run(args,**kwargs):
            calls.append(args)
            return subprocess.CompletedProcess(args,0)
        with patch.object(wp.shutil,'which',return_value='/usr/bin/omarchy-shell'),patch.object(wp.subprocess,'run',side_effect=run),patch.object(wp.time,'sleep'):
            wp.refresh_desktop(dest/'one.webp',current)
        transition=calls[1]
        self.assertEqual(base64.b64decode(transition[8]).decode(),'accent = "#4cc9ff"\n')
        self.assertEqual(base64.b64decode(transition[9]).decode(),'[bar]\nbackground-alpha = 0.90\n')

    def test_other_theme_and_no_monitor_are_untouched(self):
        current, dest = self.stage()
        self.assertFalse(wp.sync(wp.plan(self.root, detected=[]), current))
        (current/'theme.name').write_text('other')
        self.assertFalse(wp.sync(self.plan(), current))
        self.assertEqual((dest/'one.webp').read_bytes(), b'old')

    def test_hash_failure_before_any_replacement(self):
        current, dest = self.stage()
        p = self.plan()
        Path(p['files'][-1]).write_bytes(b'tampered')
        with self.assertRaisesRegex(ValueError, 'changed since packaging'):
            wp.sync(p, current)
        self.assertEqual((dest/'one.webp').read_bytes(), b'old')

    def test_symlink_stage_refused(self):
        current = self.root/'current'
        current.mkdir()
        (current/'theme.name').write_text('p-bloom')
        (current/'theme').symlink_to(self.root/'16-9', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'regular staged'):
            wp.sync(self.plan(), current)

    def test_cancel_does_not_sync_or_save(self):
        with patch.object(wp, 'read_setup', return_value={}), patch.object(wp, 'announce', return_value=False), \
             patch.object(wp, 'sync',return_value=False) as sync, patch.object(wp, 'save_setup') as save:
            self.assertFalse(wp.initialize(self.root, self.plan(),configure=True))
            sync.assert_not_called()
            save.assert_not_called()

    def test_setup_once_and_retry_when_detection_unavailable(self):
        with patch.object(wp, 'read_setup', return_value={'version':6, 'root':str(self.root),'selected':'16-9','desktop_selected':'16-9'}), \
             patch.object(wp, 'announce') as announce, patch.object(wp, 'sync',return_value=False), patch.object(wp, 'save_setup') as save:
            self.assertTrue(wp.initialize(self.root, self.plan()))
            announce.assert_not_called()
            save.assert_called_once()
            self.notify.assert_not_called()
        with patch.object(wp, 'read_setup', return_value={}), patch.object(wp, 'announce', return_value='auto'), \
             patch.object(wp, 'sync',return_value=False), patch.object(wp, 'save_setup') as save:
            wp.initialize(self.root, wp.plan(self.root, detected=[]))
            save.assert_not_called()

    def test_manual_settings_persist_and_notification_does_not_repeat(self):
        previous={}
        def save(value):previous.update(value)
        with patch.object(wp,'read_setup',side_effect=lambda:dict(previous)), patch.object(wp,'save_setup',side_effect=save), patch.object(wp,'sync',return_value=False), patch.object(wp,'announce',return_value='wide') as prompt:
            wp.initialize(self.root,self.plan())
            prompt.assert_not_called()
            self.notify.assert_called_once()
            wp.initialize(self.root,self.plan())
            self.notify.assert_called_once()
            result=wp.initialize(self.root,self.plan(),configure=True)
            self.assertEqual(result['profile'],'wide')
            self.assertEqual(previous['profile'],'wide')
            self.assertEqual(self.notify.call_count,2)
            result=wp.initialize(self.root,self.plan(),requested=previous['profile'])
            self.assertEqual(result['profile'],'wide')
            self.assertEqual(self.notify.call_count,2)


class Notifications(unittest.TestCase):
    def test_notification_opens_settings(self):
        p=dict(size=[3840,2160],profile='4k',recommended='4k')
        with patch.object(wp.shutil,'which',side_effect=lambda name:'/usr/bin/'+name), patch.object(wp.subprocess,'run') as run:
            wp.notify_selection(p,True)
            args=run.call_args.args[0]
            self.assertEqual(args[-3:],['--exec','/usr/bin/p-bloom-wallpapers','--configure'])
            self.assertTrue(any('3840 × 2160' in x for x in args))
            self.assertIn('Click to change settings.',args)

    def test_notification_failure_does_not_block_launch(self):
        with patch.object(wp.shutil,'which',return_value='/usr/bin/notifier'), patch.object(wp.subprocess,'run',side_effect=OSError('No bus')):
            wp.notify_selection(dict(size=[3840,2160],profile='4k',recommended='4k'),False)


if __name__ == '__main__':
    unittest.main()
