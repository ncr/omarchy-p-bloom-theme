"""Verify the native-resolution mask contract and preset bounds (no GPU)."""
import unittest
from PIL import Image, ImageChops
import server

class GeometryTests(unittest.TestCase):
    def test_presets_and_mask_preserve_original(self):
        for p in server.PRESETS.values():
            with self.subTest(preset=p['id']):
                self.assertTrue(all(q is None or all(0 <= v <= 1 for v in q) for q in p['points']))
                original=server.source_image(p)
                mask=server.default_mask(p['points'],p['size'])
                result=server.composite(original,Image.new('RGB',p['size'],'red'),mask,p['box'])
                self.assertEqual(result.size,original.size)
                full=Image.new('L',original.size)
                x,y,u,v=p['box']
                full.paste(mask.resize((u-x,v-y),Image.Resampling.NEAREST),(x,y))
                outside=Image.eval(full,lambda value:255 if value==0 else 0)
                delta=ImageChops.difference(original,result)
                self.assertIsNone(Image.composite(delta,Image.new('RGB',original.size),outside).getbbox())
                self.assertIsNotNone(delta.getbbox())

    def test_empty_mask_changes_nothing(self):
        original=Image.new('RGB',(60,40),(12,34,56))
        result=server.composite(original,Image.new('RGB',(20,20),'red'),Image.new('L',(20,20)),(10,10,30,30))
        self.assertIsNone(ImageChops.difference(original,result).getbbox())

if __name__=='__main__':unittest.main()
