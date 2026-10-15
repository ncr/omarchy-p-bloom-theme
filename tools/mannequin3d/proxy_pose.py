"""Single source for PX-1's authored running pose and diagram attachment points.

Side elevation: x forward, y down. Segment angles start at vertical down;
positive angles swing forward. Flight before the forward foot lands. This is
an illustrative pose, not sampled motion capture or a dynamics simulation.
"""
import math

LENGTHS={'upper_arm':116, 'forearm':88, 'thigh':146, 'calf':140}


def layout():
    shoulder=(34,-178);hip=(-6,20)
    def step(p,length,angle):
        a=math.radians(angle)
        return (p[0]+length*math.sin(a),p[1]+length*math.cos(a))
    pose={'shoulder':shoulder,'hip':hip}
    # The watch-bearing arm leads while that same side's leg recovers behind.
    for side,arm,forearm,thigh,calf,foot in (
        ('near',35,125,-18,-108,-85),
        ('far',-48,42,50,5,3),
    ):
        elbow=step(shoulder,LENGTHS['upper_arm'],arm)
        wrist=step(elbow,LENGTHS['forearm'],forearm)
        knee=step(hip,LENGTHS['thigh'],thigh)
        ankle=step(knee,LENGTHS['calf'],calf)
        pose[side]={'elbow':elbow,'wrist':wrist,'knee':knee,'ankle':ankle,
                    'foot_angle':foot,'hand_angle':-forearm,
                    'knee_flexion':thigh-calf,'elbow_flexion':forearm-arm}
    return pose
