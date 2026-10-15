"""Accepted line treatment, with the focal part selected for each device.

The Truth Lamp rendering is identical to the accepted isolated study at
5120x2160. Other sheets retain their existing authored sections and geometry.
"""
from starmap_study import StudySheet, install_study

# Focal regions in the original main-view coordinates, relative to centres().
# These select existing paths; they do not add arbitrary decorative geometry.
FOCUS = {
    'quantum-simulator': ((-102, 48, 72, 264),),  # processor stack
    'sky-racer': ((-66, -200, 66, 192),),  # cockpit/pod
    'fusion-transport': ((396, -88, 736, 132),),  # reactor and magnetic nozzle
    'greener': ((-110, -205, 122, -126),),  # competing optical heads
    'cortical-mesh': ((-84, -84, 84, 84),),  # central electronics
    'bounder': ((-54, -292, 130, 26),),  # hip drive and knee cam
    'air-refinery': ((-228, -398, 228, -246),),  # air contactor
    'aroma-organ': ((-92, -122, 92, 62),),  # mixing chip, my shifted -30
    'tether-climber': ((-136, -104, 136, 156),),  # traction drive
    'truth-lamp': ((-145, -260, 145, -150),),
    'organ-foundry': ((-108, -244, 134, 80),),  # print front and organ
    'volumetric-stage': ((-245, -260, 245, 210),),  # luminous volume
    'proxy': ((106, -224, 236, -128),),  # watched wrist
    'presence-rig': ((-46, -342, 46, -266), (-28, -220, 28, -152)),
}


class StarmapSheet(StudySheet):
    def begin_main(self,*args,**kwargs):
        super().begin_main(*args,**kwargs)
        self._main_inverse=self.c.get_matrix()
        self._main_inverse.invert()

    def primary_focus(self,gx,gy):
        if self.role!='main':return False
        # Keep the accepted native Truth Lamp byte-for-byte.
        if self.subject=='truth-lamp' and self.wide:
            return super().primary_focus(gx,gy)
        x,y=self._main_inverse.transform_point(gx*self.s,gy*self.s)
        x-=self.cx-120;y-=self.cy-25
        return any(x0<x<x1 and y0<y<y1 for x0,y0,x1,y1 in FOCUS[self.subject])


_installed=False
def install():
    global _installed
    if not _installed:
        install_study(StarmapSheet)
        _installed=True
