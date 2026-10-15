import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import wallpaper_setup_cli as cli

PLAN = dict(recommended='small', biggest='big', reason='Smallest set that fits both screens.',
            options=[dict(profile='small',size=[1920,1080],total_bytes=80_000_000,displays=[]),
                     dict(profile='big',size=[3840,2160],total_bytes=280_000_000,displays=[])])


class CLI(unittest.TestCase):
    def test_settings_include_auto_and_real_profiles(self):
        self.assertEqual(cli.settings(PLAN),[('auto','Automatic · Optimal set'),('small','1920 × 1080 /  80.0 MB'),('big','3840 × 2160 / 280.0 MB')])

    def test_automatic_names_the_set_it_picks(self):
        rows=cli.settings({**PLAN,'profile':'big'})
        self.assertEqual(rows[0],('auto','Automatic · Optimal set (3840 × 2160)'))
        self.assertEqual(rows[2],('big','3840 × 2160 / 280.0 MB · optimal'))

    def test_tui_navigation_and_cancel(self):
        class Screen:
            def __init__(self, keys, size=(33,110)):
                self.keys=iter(keys); self.size=size; self.lines=[]
            def getmaxyx(self):return self.size
            def erase(self):self.lines=[]
            def addstr(self,y,x,text,style):
                assert 0<=y<self.size[0] and x+len(text)<self.size[1]
                self.lines.append(text)
            def refresh(self):pass
            def keypad(self,value):pass
            def get_wch(self):return next(self.keys)
        with patch.object(cli.curses,'curs_set'),patch.object(cli.curses,'has_colors',return_value=False):
            screen=Screen([cli.curses.KEY_DOWN,'2','\n'])
            self.assertEqual(cli.tui(screen,PLAN,True),{'profile':'small','level':'default'})
            self.assertTrue(any('Optimal set' in text for text in screen.lines))
            self.assertIsNone(cli.tui(Screen(['\x1b']),PLAN,True))
            self.assertEqual(cli.tui(Screen(['\n'],(10,35)),PLAN,False),{'profile':'auto','level':'default'})

    def test_tui_background_level_is_a_three_way_choice(self):
        class Screen:
            def __init__(self, keys):
                self.keys=iter(keys); self.lines=[]
            def getmaxyx(self):return (33,110)
            def erase(self):self.lines=[]
            def addstr(self,y,x,text,style):self.lines.append(text)
            def refresh(self):pass
            def keypad(self,value):pass
            def get_wch(self):return next(self.keys)
        right,left=cli.curses.KEY_RIGHT,cli.curses.KEY_LEFT
        with patch.object(cli.curses,'curs_set'):
            screen=Screen([right,right,right,'\n'])
            self.assertEqual(cli.tui(screen,PLAN,True),{'profile':'auto','level':'vivid'})
            self.assertIn('How strong the background colour is.',screen.lines)
            self.assertTrue(any('[ Vivid ]' in text for text in screen.lines))
            plan={**PLAN,'setting':'big','setting_level':'vivid'}
            self.assertEqual(cli.tui(Screen([left,left,left,'\n']),plan,True),{'profile':'big','level':'muted'})

    def test_resolution_list_follows_the_chosen_level(self):
        plan={**PLAN,'options_by_level':{
            'default':PLAN['options'],
            'vivid':[dict(profile='small',size=[1920,1080],total_bytes=90_000_000,local=False,displays=[]),
                     dict(profile='big',size=[3840,2160],total_bytes=300_000_000,displays=[])]}}
        self.assertEqual(cli.settings(plan,'vivid')[1],('small','1920 × 1080 /  90.0 MB · download'))
        self.assertEqual(cli.settings(plan,'muted'),cli.settings(PLAN))  # not listed: the plan's own options
        class Screen:
            def __init__(self, keys):
                self.keys=iter(keys); self.frames=[]; self.lines=[]
            def getmaxyx(self):return (33,110)
            def erase(self):
                if self.lines:self.frames.append(self.lines)
                self.lines=[]
            def addstr(self,y,x,text,style):self.lines.append(text)
            def refresh(self):pass
            def keypad(self,value):pass
            def get_wch(self):return next(self.keys)
        with patch.object(cli.curses,'curs_set'):
            screen=Screen([cli.curses.KEY_RIGHT,'\n'])
            self.assertEqual(cli.tui(screen,plan,True),{'profile':'auto','level':'vivid'})
        first,second=screen.frames[0],screen.lines
        self.assertTrue(any('80.0 MB' in x and 'download' not in x for x in first))
        self.assertTrue(any('90.0 MB · download' in x for x in second))
        with patch.object(cli.shutil,'which',return_value=None),patch('sys.stdout',new_callable=io.StringIO) as out, \
             patch('builtins.input',side_effect=['3','2']):
            self.assertEqual(cli.prompt(plan,False),{'profile':'small','level':'vivid'})
        self.assertIn('90.0 MB · download',out.getvalue())

    def test_plain_default_and_cancel(self):
        with patch.object(cli.shutil,'which',return_value=None),patch('sys.stdout',new_callable=io.StringIO):
            with patch('builtins.input',return_value=''):
                self.assertEqual(cli.prompt(PLAN,False),{'profile':'auto','level':'default'})
            with patch('builtins.input',side_effect=['3','2']):
                self.assertEqual(cli.prompt(PLAN,False),{'profile':'small','level':'vivid'})
            with patch('builtins.input',return_value='q'):
                self.assertIsNone(cli.prompt(PLAN,False))

    def test_desktop_terminal_passes_choice_back(self):
        def terminal(args, **kwargs):
            result=Path(args[args.index('--result')+1])
            request=json.loads(Path(args[args.index('--request')+1]).read_text())
            self.assertEqual(request['plan'],PLAN)
            result.write_text('{"profile": "auto", "level": "muted"}')
            return subprocess.CompletedProcess(args,0)
        with patch('sys.stdin.isatty',return_value=False),patch.dict(os.environ,{'WAYLAND_DISPLAY':'wayland-1'}), \
             patch.object(cli.shutil,'which',return_value='/usr/bin/xdg-terminal-exec'), \
             patch.object(cli.subprocess,'run',side_effect=terminal):
            self.assertEqual(cli.choose_profile(PLAN,True),{'profile':'auto','level':'muted'})

    def test_terminal_closed_without_result_is_cancel(self):
        with patch('sys.stdin.isatty',return_value=False),patch.dict(os.environ,{'WAYLAND_DISPLAY':'wayland-1'}), \
             patch.object(cli.shutil,'which',return_value='/usr/bin/xdg-terminal-exec'), \
             patch.object(cli.subprocess,'run',return_value=subprocess.CompletedProcess([],1)):
            self.assertIsNone(cli.choose_profile(PLAN,True))

    def test_the_gallery_menu_gets_the_plan_and_answers_on_stdin(self):
        for answer, expected in (('{"profile": "big", "level": "vivid"}\n', {'profile':'big','level':'vivid'}),
                                 ('null\n', None), ('{"profile": "huge", "level": "vivid"}\n', None), ('', None)):
            out=io.StringIO()
            with patch.dict(os.environ,{'PBLOOM_SETTINGS_PIPE':'1'}), patch('sys.stdout',out), \
                 patch('sys.stdin',io.StringIO(answer)), patch.object(cli,'prompt') as prompt:
                self.assertEqual(cli.choose_profile(PLAN,True),expected)
                prompt.assert_not_called()
            line=out.getvalue().splitlines()[0]
            self.assertTrue(line.startswith(cli.PIPE_PREFIX))
            self.assertEqual(json.loads(line[len(cli.PIPE_PREFIX):]),PLAN)

if __name__=='__main__':unittest.main()
