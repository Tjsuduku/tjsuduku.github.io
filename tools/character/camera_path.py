# Camera path for the scroll timeline, authored from scratch (no data copied from any other model).
# Every shot is defined by a target, a distance, and a yaw/pitch around the target. Edit CFG and STOPS below,
# then run tools/character/run_all.sh.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
import numpy as np, json
from scipy.spatial.transform import Rotation as Rot
from pygltflib import GLTF2, BufferView, Accessor, Node

# ---------- settings you can edit ----------
CFG = dict(
    head_top_y=0.99,      # highest point of the hair (model units)
    chin_y=0.082,         # chin
    hero_top=0.07,        # where the hair top sits in the hero frame (0 = top edge, 1 = bottom edge)
    hero_chin=0.60,       # where the chin sits in the hero frame
    design_aspect=1.6,    # screen shape used to place subjects (wide laptop)
    stop_screen_x=0.28,   # close-ups: where the sticker lands across the screen (0 left, 1 right) so text sits on the right
    works_screen_x=0.40,  # wide shot and Works section: where the face sits
    bulge=0.30,           # how far the camera swings back when travelling between far apart stickers
)
# name, targets (sticker centres averaged), distance, yaw (deg, + = camera swings to the face's right side), pitch (deg, + = from above)
STOPS = [
    ('jaalik+reframes', ['jaalik', 'reframes'], 1.00,  38, -4),   # 1 right upper cheek
    ('telus',           ['telus'],              0.95,  42, -6),   # 2 right lower cheek
    ('skechers',        ['skechers'],           0.95, -38,  2),   # 3 left upper cheek
    ('cloverdale',      ['cloverdale'],         1.05, -40, -3),   # 4 left lower cheek with the social icons
    ('boopdog',         ['boopdog'],            0.95,  46, -10),  # 5 right jaw
    ('ai',              ['chatgpt', 'claude'],  0.95, -46, -8),   # 6 left jaw
]
WIDE_DIST_MULT = 1.05     # stop 7 (wide, SFU on the nose) is the hero distance times this
TAIL_PULLBACK = 1.07      # during the Works spin the camera drifts back by this factor
TAIL_YAW = -4             # and swings by this many degrees
# --------------------------------------------

g = GLTF2().load_binary(MODEL_V4); blob = bytearray(g.binary_blob())
def rd(i):
    a = g.accessors[i]; bv = g.bufferViews[a.bufferView]; n = {'SCALAR':1,'VEC3':3,'VEC4':4}[a.type]
    return np.frombuffer(bytes(blob), np.float32, a.count*n, (bv.byteOffset or 0)+(a.byteOffset or 0)).reshape(a.count, n).copy()
def add(data, target=None):
    while len(blob) % 4: blob.append(0)
    off = len(blob); blob.extend(data); g.bufferViews.append(BufferView(buffer=0, byteOffset=off, byteLength=len(data), target=target)); return len(g.bufferViews)-1
def addacc(arr, typ):
    arr = arr.astype(np.float32)
    g.accessors.append(Accessor(bufferView=add(arr.tobytes()), componentType=5126, count=len(arr), type=typ,
        min=arr.min(0).tolist() if arr.ndim > 1 else [float(arr.min())], max=arr.max(0).tolist() if arr.ndim > 1 else [float(arr.max())]))
    return len(g.accessors)-1

an = {a.name: a for a in g.animations}
ca = an['CameraAction']; ch = {c.target.path: c for c in ca.channels}
nodes = {n.name: i for i, n in enumerate(g.nodes)}
cam_node = g.nodes[nodes['Camera']]
yfov = g.cameras[cam_node.camera].perspective.yfov
tanh = np.tan(yfov/2)
C = json.load(open(CENTERS)); C = {k: np.array(v) for k, v in C.items()}

# hero: choose distance and height so hair top and chin land on the chosen screen fractions
span = CFG['head_top_y'] - CFG['chin_y']
H = span/(CFG['hero_chin']-CFG['hero_top'])         # visible height in model units
hero_d = H/(2*tanh)
hero_y = CFG['head_top_y'] + (CFG['hero_top']-0.5)*H*-1  # screen centre height  (top edge = centre + H/2)
hero_y = CFG['head_top_y'] + CFG['hero_top']*H - H/2
HERO_T = np.array([0.0, hero_y, 0.30])                # look-at point for hero and wide shot
print('hero distance %.3f, centre y %.3f' % (hero_d, hero_y))

# shots: (target, distance, yaw, pitch, screen_x)
shots = [(HERO_T, hero_d, 0.0, 0.0, 0.5)]
focus = {0: np.array(g.nodes[nodes['focus-0']].translation)}
for k, (nm, names, d, yaw, pit) in enumerate(STOPS, start=1):
    t = np.mean([C[n] for n in names], axis=0)
    shots.append((t, d, yaw, pit, CFG['stop_screen_x'])); focus[k] = t
shots.append((HERO_T, hero_d*WIDE_DIST_MULT, 0.0, 0.0, CFG['works_screen_x'])); focus[7] = C['sfu']
M = len(shots)-1          # 7 timeline stops after the hero

def look(t, d, yaw, pit, sx):
    y, p = np.radians(yaw), np.radians(pit)
    dirv = np.array([np.sin(y)*np.cos(p), np.sin(p), np.cos(y)*np.cos(p)])
    pos = t + dirv*d
    f = (t-pos); f /= np.linalg.norm(f)
    right = np.cross(f, [0, 1, 0]); right /= np.linalg.norm(right)
    up = np.cross(right, f)
    q = Rot.from_matrix(np.stack([right, up, -f], axis=1)).as_quat()   # xyzw (glTF order)
    pos = pos + right*(0.5-sx)*(2*d*tanh*CFG['design_aspect'])          # slide sideways so the subject sits at screen_x
    return pos, q
def slerp(a, b, t):
    dd = np.dot(a, b)
    if dd < 0: b = -b; dd = -dd
    if dd > 0.9995: r = a+(b-a)*t; return r/np.linalg.norm(r)
    th = np.arccos(dd); return (np.sin((1-t)*th)*a+np.sin(t*th)*b)/np.sin(th)
def blend(a, b, s):
    t = a[0]*(1-s)+b[0]*s
    d = a[1]**(1-s)*b[1]**s                       # distances blend multiplicatively so zooms feel even
    yaw = a[2]*(1-s)+b[2]*s; pit = a[3]*(1-s)+b[3]*s; sx = a[4]*(1-s)+b[4]*s
    pos, q = look(t, d, yaw, pit, sx)
    far = np.linalg.norm(a[0]-b[0])
    if far > 0.12:                                 # swing back a little when travelling across the face
        dirv = (pos-t)/np.linalg.norm(pos-t)
        pos = pos + dirv*CFG['bulge']*np.sin(np.pi*s)*min(far/0.3, 1.0)
    return pos, q

NT = []; NR = []
for f in range(1, M*50+1):
    k = (f-1)//50; t = ((f-1) % 50+1)/50
    if f == M*50: k, t = M-1, 1.0
    s = t*t*(3-2*t)
    p, q = blend(shots[k], shots[k+1], s); NT.append(p); NR.append(q)
last = shots[M]
for i in range(1, 101):                            # Works tail: slow drift back while the head spins
    s = i/100; s = s*s*(3-2*s)
    tail = (last[0], last[1]*(1+(TAIL_PULLBACK-1)*s), last[2]+TAIL_YAW*s, last[3], last[4])
    p, q = look(*tail); NT.append(p); NR.append(q)
NT = np.array(NT); NR = np.array(NR)
for i in range(1, len(NR)):                        # keep quaternions on one side so playback never flips
    if np.dot(NR[i], NR[i-1]) < 0: NR[i] = -NR[i]
N = len(NT); print('frames', N)
times = (np.arange(1, N+1)/24.0).reshape(-1, 1)
ti = addacc(times, 'SCALAR'); ta = addacc(NT, 'VEC3'); ra = addacc(NR, 'VEC4')
ca.samplers[ch['translation'].sampler].input = ti; ca.samplers[ch['translation'].sampler].output = ta
ca.samplers[ch['rotation'].sampler].input = ti; ca.samplers[ch['rotation'].sampler].output = ra
# the 360 spin starts after the last timeline stop
ma = an['manAction']
for s in ma.samplers:
    tt = rd(s.input)+100/24.0; s.input = addacc(tt, 'SCALAR')
# focus anchors (what the depth of field focuses on)
for k in range(1, 8):
    nm = f'focus-{k}'
    if nm in nodes: g.nodes[nodes[nm]].translation = focus[k].tolist()
    else:
        g.nodes.append(Node(name=nm, translation=focus[k].tolist())); g.nodes[nodes['man']].children.append(len(g.nodes)-1)
if 'focus-works' in nodes: g.nodes[nodes['focus-works']].translation = focus[7].tolist()
g.buffers[0].byteLength = len(blob); g.set_binary_blob(bytes(blob)); g.save_binary(MODEL_CAM); print('ok')
