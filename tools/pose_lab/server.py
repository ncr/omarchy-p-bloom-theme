#!/usr/bin/env python3
"""Local pose/mask editor and ComfyUI client for wallpaper reference studies."""
import argparse
import base64
import io
import json
import math
import mimetypes
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'concepts/pose-lab/runs'
CHECKPOINT = 'sd_xl_base_1.0.safetensors'
CONTROLNET = 'xinsir-openpose-sdxl.safetensors'

def models_ready():
    from verify_models import ROOT as model_root, MODELS
    return all((model_root/name).is_file() and (model_root/name).stat().st_size==spec[0]
               for name,spec in MODELS.items())
# COCO/OpenPose-18 order. Colours and thick ellipses follow xinsir's model card.
JOINTS = ['Nose', 'Neck', 'R shoulder', 'R elbow', 'R wrist', 'L shoulder',
          'L elbow', 'L wrist', 'R hip', 'R knee', 'R ankle', 'L hip',
          'L knee', 'L ankle', 'R eye', 'L eye', 'R ear', 'L ear']
LIMBS = [(1,2),(1,5),(2,3),(3,4),(5,6),(6,7),(1,8),(8,9),(9,10),
         (1,11),(11,12),(12,13),(1,0),(0,14),(14,16),(0,15),(15,17)]
COLORS = [(255,0,0),(255,85,0),(255,170,0),(255,255,0),(170,255,0),
          (85,255,0),(0,255,0),(0,255,85),(0,255,170),(0,255,255),
          (0,170,255),(0,85,255),(0,0,255),(85,0,255),(170,0,255),
          (255,0,255),(255,0,170),(255,0,85)]
NEGATIVE = ('human skin, flesh, hair, clothing, expressive face, muscular superhero, '
            'armor, weapons, extra limbs, extra joints, detached limbs, twisted wrists, '
            'splayed fingers, distorted anatomy, cropped feet, cropped head, text, lettering, '
            'watermark, logo, busy background, dramatic perspective, fisheye')
REFERENCE_PROMPT = ('Industrial design reference of a full body automotive crash test dummy, '
                    'matte ivory moulded polymer shell, realistic adult proportions, symmetrical '
                    'manufactured limb components, recessed metal pivot joints, flexible black '
                    'neck and lumbar bellows, smooth simplified head, compact moulded hands with '
                    'grouped fingers, small circular black and yellow calibration targets, '
                    'precise silhouette, orthographic technical product photography, soft diffuse '
                    'studio lighting, plain light grey background, entire figure visible. ')


def presets():
    import sys
    sys.path.insert(0, str(ROOT / 'tools'))
    from human_figures import proxy_pose
    p = proxy_pose()
    def absxy(pt): return (2320+pt[0]*2, 1030+pt[1]*2)
    proxy = [(2412,470),(2388,640),absxy(p['shoulder']),
             absxy(p['far']['elbow']),absxy(p['far']['wrist']),
             (2398,678),absxy(p['near']['elbow']),absxy(p['near']['wrist']),
             (2298,1070),absxy(p['far']['knee']),absxy(p['far']['ankle']),
             (2318,1070),absxy(p['near']['knee']),absxy(p['near']['ankle']),
             None,(2407,461),None,(2375,468)]
    presence = [(2320,422),(2320,522),(2148,558),(2068,794),(2020,1018),
                (2492,558),(2572,794),(2620,1018),(2248,970),(2220,1238),
                (2216,1470),(2392,970),(2420,1238),(2424,1470),
                (2306,410),(2334,410),(2286,425),(2354,425)]
    seated = [(1557,938),(1520,1008),(1522,1060),(1554,1194),(1682,1192),
              (1530,1060),(1562,1194),(1690,1192),(1518,1308),(1752,1336),
              (1754,1580),(1526,1308),(1760,1336),(1762,1580),
              None,(1544,921),None,(1504,932)]
    result = {}
    for key,title,file,box,size,pose,description in [
        ('presence','Presence Rig','14-presence-rig.webp',(1920,280,2736,1572),
         (768,1216),presence,'Standing upright, frontal view, relaxed arms slightly away from the body, feet facing forward.'),
        ('proxy','Proxy','13-proxy.webp',(1840,352,2864,1696),
         (832,1088),proxy,'Running toward the right, strict side view, trailing arm bent backwards and leading arm bent forwards. Study the complete dummy first; its physical head will be omitted in the final blueprint.'),
        ('truth','Truth Lamp — przy stole','10-truth-lamp.webp',(1392,816,1904,1680),
         (704,1184),seated,'Strict right-facing side view, seated upright on a simple chair, forearms horizontal on a table, thighs horizontal, shins vertical, feet flat on the floor.')]:
        x0,y0,x1,y1=box
        result[key]={'id':key,'title':title,'file':file,'box':box,'size':size,
                     'points':[None if q is None else [(q[0]-x0)/(x1-x0),(q[1]-y0)/(y1-y0)] for q in pose],
                     'prompt':REFERENCE_PROMPT+description}
    return result


PRESETS = presets()


def pose_image(points, size):
    im=Image.new('RGB',size);draw=ImageDraw.Draw(im);w,h=size
    pts=[None if p is None else (p[0]*w,p[1]*h) for p in points]
    radius=12 if max(size)>=1000 else 8
    for (a,b),col in zip(LIMBS,COLORS):
        if pts[a] is None or pts[b] is None:continue
        x,y=pts[a];u,v=pts[b];dx,dy=u-x,v-y;length=math.hypot(dx,dy)
        if length<1:continue
        # Elliptical limb, tapered at both ends, rather than a flat stroke.
        polygon=[]
        for i in range(40):
            t=i*math.tau/40
            along=math.cos(t)*length/2;across=math.sin(t)*radius
            polygon.append(((x+u)/2+along*dx/length-across*dy/length,
                            (y+v)/2+along*dy/length+across*dx/length))
        draw.polygon(polygon,fill=tuple(int(c*.6) for c in col))
    for p,col in zip(pts,COLORS):
        if p:draw.ellipse((p[0]-radius,p[1]-radius,p[0]+radius,p[1]+radius),fill=col)
    return im


def source_image(preset):
    im=Image.open(ROOT/'backgrounds'/preset['file']).convert('RGB')
    if im.size != (5120,2160):
        raise ValueError('Te kadry wymagają tapet 5120×2160 z brancha ultrawide.')
    return im


def default_mask(points,size):
    im=Image.new('L',size);d=ImageDraw.Draw(im);w,h=size
    pts=[None if p is None else (p[0]*w,p[1]*h) for p in points]
    radius=round(w*.067)
    for a,b in LIMBS[:12]:
        if pts[a] and pts[b]:d.line((pts[a],pts[b]),fill=255,width=radius*2)
    for p in pts[:14]:
        if p:d.ellipse((p[0]-radius,p[1]-radius,p[0]+radius,p[1]+radius),fill=255)
    torso=[pts[i] for i in (2,5,11,8) if pts[i]]
    if len(torso)==4:d.polygon(torso,fill=255)
    if pts[0]:
        x,y=pts[0];d.ellipse((x-radius,y-radius*1.3,x+radius,y+radius*1.3),fill=255)
    return im


def composite(original, generated, mask, box):
    """Change only the painted region, in original wallpaper coordinates."""
    x0,y0,x1,y1=box;size=(x1-x0,y1-y0)
    hard=mask.resize(size,Image.Resampling.NEAREST)
    # Feather inwards, so blur cannot expand the user's authorized mask.
    soft=ImageChops.darker(hard,hard.filter(ImageFilter.GaussianBlur(4)))
    patch=Image.composite(generated.resize(size,Image.Resampling.LANCZOS),original.crop(box),soft)
    out=original.copy();out.paste(patch,(x0,y0));return out


def graph(preset,mode,prompt,seed,strength,denoise,names,steps=30):
    g={
        '1':{'class_type':'CheckpointLoaderSimple','inputs':{'ckpt_name':CHECKPOINT}},
        '2':{'class_type':'CLIPTextEncode','inputs':{'clip':['1',1],'text':prompt}},
        '3':{'class_type':'CLIPTextEncode','inputs':{'clip':['1',1],'text':NEGATIVE}},
        '4':{'class_type':'ControlNetLoader','inputs':{'control_net_name':CONTROLNET}},
        '5':{'class_type':'LoadImage','inputs':{'image':names['pose']}},
        '6':{'class_type':'ControlNetApplyAdvanced','inputs':{'positive':['2',0],'negative':['3',0],
             'control_net':['4',0],'image':['5',0],'strength':strength,'start_percent':0.,'end_percent':.85}},
        '7':{'class_type':'EmptyLatentImage','inputs':{'width':preset['size'][0],'height':preset['size'][1],'batch_size':1}},
        '8':{'class_type':'KSampler','inputs':{'model':['1',0],'positive':['6',0],'negative':['6',1],
             'latent_image':['7',0],'seed':seed,'steps':steps,'cfg':5.5,'sampler_name':'dpmpp_2m_sde',
             'scheduler':'karras','denoise':1. if mode=='reference' else denoise}},
        '9':{'class_type':'VAEDecode','inputs':{'samples':['8',0],'vae':['1',2]}},
        '10':{'class_type':'SaveImage','inputs':{'images':['9',0],'filename_prefix':'p-bloom-pose/reference'}}}
    if mode=='inpaint':
        g['11']={'class_type':'LoadImage','inputs':{'image':names['source']}}
        g['12']={'class_type':'LoadImageMask','inputs':{'image':names['mask'],'channel':'red'}}
        # Generic SDXL checkpoint: preserve the source latent at low denoise.
        # Blanking the region is suitable for full repainting, but leaves grey
        # silhouettes when the user requests only a modest correction.
        g['13']={'class_type':'VAEEncode','inputs':{'pixels':['11',0],'vae':['1',2]}}
        g['7']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['13',0],'mask':['12',0]}}
    return g


def comfy(path, data=None):
    req=Request(COMFY+path, None if data is None else json.dumps(data).encode(),
                {'Content-Type':'application/json'})
    with urlopen(req,timeout=20) as r:return json.load(r)


def upload(path):
    boundary='pose'+uuid.uuid4().hex
    body=(f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="{path.name}"\r\n'
          'Content-Type: image/png\r\n\r\n').encode()+path.read_bytes()+f'\r\n--{boundary}--\r\n'.encode()
    req=Request(COMFY+'/upload/image',body,{'Content-Type':'multipart/form-data; boundary='+boundary})
    with urlopen(req,timeout=20) as r:
        data=json.load(r);return '/'.join(p for p in (data.get('subfolder'),data['name']) if p)


JOBS={};LOCK=threading.Lock()


def run_job(job_id, data):
    job=JOBS[job_id];folder=OUT/job_id;folder.mkdir(parents=True)
    try:
        p=PRESETS[data['preset']];size=p['size'];original=source_image(p)
        points=data.get('points',p['points'])
        if len(points)!=18 or any(q is not None and (len(q)!=2 or any(not math.isfinite(v) or not 0<=v<=1 for v in q)) for q in points):
            raise ValueError('Poza musi zawierać 18 punktów w obrębie kadru.')
        mode=data.get('mode','reference')
        if mode not in ('reference','inpaint'):raise ValueError('Nieznany tryb.')
        mask=default_mask(points,size)
        if data.get('mask'):
            mask=Image.open(io.BytesIO(base64.b64decode(data['mask'].split(',')[-1])))
            if mask.size!=tuple(size):raise ValueError('Maska ma inny rozmiar niż kadr.')
            mask=mask.convert('L')
        if mode=='inpaint' and mask.getbbox() is None:raise ValueError('Najpierw zamaluj obszar poprawki.')
        prompt=str(data.get('prompt',p['prompt']))[:6000]
        seed=int(data.get('seed',42));strength=float(data.get('strength',.85));denoise=float(data.get('denoise',.85))
        if not 0<=seed<2**53 or not 0<=strength<=2 or not .1<=denoise<=1:raise ValueError('Parametry poza zakresem.')
        files={key:folder/f'{job_id}-{key}.png' for key in ('source','pose','mask')}
        original.crop(p['box']).resize(size,Image.Resampling.LANCZOS).save(files['source'])
        pose_image(points,size).save(files['pose']);mask.save(files['mask'])
        names={key:upload(path) for key,path in files.items()}
        g=graph(p,mode,prompt,seed,strength,denoise,names)
        (folder/'workflow-api.json').write_text(json.dumps(g,indent=2))
        keypoints=[v for pt in points for v in ([0,0,0] if pt is None else [pt[0]*size[0],pt[1]*size[1],1])]
        (folder/'openpose.json').write_text(json.dumps({'canvas_width':size[0],'canvas_height':size[1],
             'people':[{'pose_keypoints_2d':keypoints,'face_keypoints_2d':[],'hand_left_keypoints_2d':[],
                        'hand_right_keypoints_2d':[]}]},indent=2))
        recipe={'preset':p['id'],'mode':mode,'points':points,'crop_box':p['box'],'generation_size':size,
                'original_size':original.size,'prompt':prompt,'negative':NEGATIVE,'seed':seed,
                'strength':strength,'denoise':denoise,'checkpoint':CHECKPOINT,'controlnet':CONTROLNET}
        (folder/'recipe.json').write_text(json.dumps(recipe,indent=2))
        response=comfy('/prompt',{'prompt':g,'client_id':'p-bloom-pose-lab'})
        if response.get('node_errors'):raise RuntimeError(json.dumps(response['node_errors']))
        prompt_id=response['prompt_id'];job.update(status='generating',prompt_id=prompt_id)
        for _ in range(900):
            history=comfy('/history/'+prompt_id).get(prompt_id)
            if history:
                if history.get('status',{}).get('status_str')=='error':
                    raise RuntimeError(str(history['status']['messages'])[-2500:])
                images=history.get('outputs',{}).get('10',{}).get('images',[])
                if images:break
            time.sleep(1)
        else:raise TimeoutError('ComfyUI nie zakończyło zadania w 15 minut. Sprawdź jego kolejkę.')
        with urlopen(COMFY+'/view?'+urlencode(images[0]),timeout=30) as r:
            generated=Image.open(io.BytesIO(r.read())).convert('RGB')
        generated.save(folder/'reference.png')
        job.update(reference=f'/runs/{job_id}/reference.png',recipe=f'/runs/{job_id}/recipe.json',
                   pose=f'/runs/{job_id}/openpose.json',workflow=f'/runs/{job_id}/workflow-api.json')
        if mode=='inpaint':
            result=composite(original,generated,mask,p['box'])
            result.save(folder/'wallpaper-study.png')
            job['wallpaper']=f'/runs/{job_id}/wallpaper-study.png'
        job.update(status='done',elapsed=round(time.time()-job['started'],1))
        (folder/'result.json').write_text(json.dumps(job,indent=2))
    except Exception as e:
        job.update(status='error',error=str(e))
        (folder/'result.json').write_text(json.dumps(job,indent=2))
    finally:
        LOCK.release()


class Handler(BaseHTTPRequestHandler):
    def send(self,body,content_type='application/json',status=200):
        if not isinstance(body,bytes):body=json.dumps(body,ensure_ascii=False).encode()
        self.send_response(status);self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store')
        self.end_headers();self.wfile.write(body)

    def do_GET(self):
        path=urlparse(self.path).path
        try:
            if path=='/':return self.send(Path(__file__).with_name('index.html').read_bytes(),'text/html; charset=utf-8')
            if path=='/api/presets':return self.send({'presets':PRESETS,'joints':JOINTS,'limbs':LIMBS,'colors':COLORS})
            if path=='/api/status':
                try:
                    comfy('/system_stats');return self.send({'online':True,'ready':models_ready(),'busy':LOCK.locked()})
                except OSError:return self.send({'online':False,'busy':LOCK.locked()})
            if path.startswith('/api/jobs/'):
                key=path.rsplit('/',1)[-1]
                if key in JOBS:return self.send(JOBS[key])
                saved=(OUT/key/'result.json').resolve()
                if saved.is_relative_to(OUT.resolve()) and saved.is_file():
                    return self.send(json.loads(saved.read_text()))
                return self.send({'error':'Brak zadania'},status=404)
            if path.startswith('/api/source/') or path.startswith('/api/mask/'):
                p=PRESETS[path.rsplit('/',1)[-1]]
                im=default_mask(p['points'],p['size']) if '/mask/' in path else source_image(p).crop(p['box']).resize(p['size'],Image.Resampling.LANCZOS)
                buf=io.BytesIO();im.save(buf,format='PNG');return self.send(buf.getvalue(),'image/png')
            if path.startswith('/runs/'):
                f=(OUT/path.removeprefix('/runs/')).resolve()
                if not f.is_relative_to(OUT.resolve()) or not f.is_file():return self.send({},status=404)
                return self.send(f.read_bytes(),mimetypes.guess_type(f.name)[0] or 'application/octet-stream')
            return self.send({},status=404)
        except (KeyError,ValueError):return self.send({'error':'Nieznany plik lub preset'},status=404)

    def do_POST(self):
        if self.path!='/api/generate':return self.send({},status=404)
        if not models_ready():return self.send({'error':'Modele są jeszcze pobierane. Spróbuj po zakończeniu instalacji.'},status=503)
        if self.headers.get('X-Pose-Lab')!='1':return self.send({'error':'Brak nagłówka panelu'},status=403)
        origin=self.headers.get('Origin')
        if origin and urlparse(origin).netloc!=self.headers.get('Host'):return self.send({},status=403)
        try:n=int(self.headers.get('Content-Length','0'))
        except ValueError:return self.send({'error':'Nieprawidłowy rozmiar'},status=400)
        if not 0<n<=8_000_000:return self.send({'error':'Zbyt duże żądanie'},status=413)
        try:
            data=json.loads(self.rfile.read(n))
            if not isinstance(data,dict):raise ValueError('Oczekiwano obiektu JSON')
            if data.get('preset') not in PRESETS:raise ValueError('Nieznana tapeta')
        except (ValueError,TypeError) as e:return self.send({'error':str(e)},status=400)
        if not LOCK.acquire(blocking=False):return self.send({'error':'Poczekaj na zakończenie bieżącej generacji.'},status=409)
        job_id=time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6]
        JOBS[job_id]={'id':job_id,'status':'preparing','started':time.time()}
        threading.Thread(target=run_job,args=(job_id,data),daemon=True).start()
        self.send(JOBS[job_id],status=202)


COMFY='http://127.0.0.1:8190'
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=8191);ap.add_argument('--comfy',default=COMFY)
    args=ap.parse_args();COMFY=args.comfy.rstrip('/')
    if urlparse(COMFY).hostname not in ('127.0.0.1','localhost','::1'):raise SystemExit('ComfyUI musi być lokalne.')
    OUT.mkdir(parents=True,exist_ok=True)
    print(f'p(bloom) Pose Lab: http://127.0.0.1:{args.port}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
