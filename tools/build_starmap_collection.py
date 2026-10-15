#!/usr/bin/env python3
"""Render and verify the accepted 14-sheet collection, without installing it."""
import copy
import gc
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import devices, foibles, leisure
from order import ORDER
from sheet import Sheet
from starmap import install

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'concepts/starmap-collection'
SIZE=(5120,2160)


def main():
    for folder in ('native','review'):
        (OUT/folder).mkdir(parents=True,exist_ok=True)
    fns=dict(devices.SHEETS+foibles.SHEETS+leisure.SHEETS)
    original_text=Sheet.text
    calls=[]
    def capture(self,*args,**kwargs):
        # Freeze the mutable shared palette and capture transforms as well.
        calls.append(copy.deepcopy((args,kwargs,tuple(self.c.get_matrix()))))
        return original_text(self,*args,**kwargs)
    Sheet.text=capture
    baseline={}
    for name,_ in ORDER:
        calls.clear()
        s=fns[name](SIZE)
        baseline[name]=copy.deepcopy(calls)
        del s
        gc.collect()
    print('Captured original text content, fonts, positions and transforms.',flush=True)
    install()
    report=[]
    font=ImageFont.truetype('/usr/share/fonts/gsfonts/NimbusSans-Regular.otf',22)
    # Two panels (eight and six sheets) keep the preview manageable.
    boards=[Image.new('RGB',(2048,4*470),'#0c1016') for _ in range(2)]
    for i,(name,palette) in enumerate(ORDER,1):
        calls.clear()
        s=fns[name](SIZE)
        assert calls==baseline[name],f'Text/placement changed: {name}'
        s.end_lines()
        path=OUT/'native'/f'{i:02d}-{name}.png'
        s.save(path)
        if name=='truth-lamp':
            assert path.read_bytes()==(ROOT/'concepts/starmap-study/native/after.png').read_bytes(), 'Accepted Truth Lamp changed'
        report.append({'name':name,'palette':palette,'resolution':SIZE,
                       'text_calls':len(calls),'text_content_style_position_transform_unchanged':True,
                       'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        with Image.open(path) as im:
            im.resize((2560,1080),Image.Resampling.LANCZOS).save(OUT/'review'/path.name)
            thumb=im.resize((1024,432),Image.Resampling.LANCZOS)
            board=boards[(i-1)//8];slot=(i-1)%8
            x,y=(slot%2)*1024,(slot//2)*470
            board.paste(thumb,(x,y+38))
            ImageDraw.Draw(board).text((x+16,y+7),f'{i:02d}  {name.upper().replace("-"," ")}',font=font,fill='#dae1e8')
        print(f'{i:02d}/14 {name}: rendered; {len(calls)} text calls unchanged',flush=True)
        del s
        gc.collect()
    Sheet.text=original_text
    boards[0].save(OUT/'preview-01-08.jpg',quality=94,subsampling=0)
    boards[1].crop((0,0,2048,3*470)).save(OUT/'preview-09-14.jpg',quality=94,subsampling=0)
    combined=Image.new('RGB',(2048,7*470),'#0c1016')
    combined.paste(boards[0],(0,0))
    combined.paste(boards[1].crop((0,0,2048,3*470)),(0,4*470))
    combined.save(OUT/'all-14.jpg',quality=94,subsampling=0)
    (OUT/'verification.json').write_text(json.dumps({'style':'starmap',
        'accepted_truth_lamp_byte_identical':True,'sheets':report},indent=2)+'\n')


if __name__=='__main__':main()
