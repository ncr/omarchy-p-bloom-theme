#!/usr/bin/env python3
"""Export the portable silent loop. Originals and desktop settings are untouched."""
import argparse,subprocess,sys,threading,http.server,json
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--id',default='o03');p.add_argument('--width',type=int,default=1920);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[2];profiles=json.loads((root/'tools/ambient/profiles.json').read_text())
if a.id not in profiles:p.error('Unknown wallpaper id')
if a.width<320 or a.width%2:p.error('Use an even width of at least 320')
height=round(a.width*2160/5120/2)*2;a.out.parent.mkdir(parents=True,exist_ok=True)
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
encoder=None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page(viewport={'width':a.width,'height':height},device_scale_factor=1)
  page.goto('http://127.0.0.1:'+str(server.server_port)+'/tools/ambient/?id='+a.id);page.wait_for_function('window.wallpaper?.ready')
  encoder=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate','24','-vcodec','png','-i','-','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(a.out)],stdin=subprocess.PIPE)
  for frame in range(24*24):
   page.evaluate('(t)=>window.wallpaper.render(t)',frame/24);encoder.stdin.write(page.screenshot(type='png'))
  encoder.stdin.close();code=encoder.wait();browser.close()
  if code:raise RuntimeError('ffmpeg failed: '+str(code))
 print(str(a.out.resolve()))
finally:
 server.shutdown()
 if encoder and encoder.poll() is None:encoder.terminate()
