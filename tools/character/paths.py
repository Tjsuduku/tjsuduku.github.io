# All file locations for the character pipeline. Change them here only.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(ROOT, 'source')
LOGOS = os.path.join(SRC, 'logos') + os.sep           # real logos (inputs)
SOURCE_GLB = os.path.join(SRC, 'model', 'source_me.glb')  # base character (input)
EYETEX = os.path.join(SRC, 'face', 'eyetex.png')       # face texture crop used for the lid patch (input)
WORK = os.path.join(HERE, 'work')                       # scratch output, safe to delete, not in git
STK_DIR = os.path.join(WORK, 'stk') + os.sep               # generated stickers
os.makedirs(STK_DIR, exist_ok=True)
MODEL_V4 = os.path.join(WORK, 'me_v4.glb')              # after build_model.py
CENTERS = os.path.join(WORK, 'centers.json')            # sticker centres, used by camera_path.py
MODEL_CAM = os.path.join(WORK, 'me_cam.glb')            # after camera_path.py
FINAL_GLB = os.path.join(ROOT, 'web', 'public', 'models', 'me.glb')  # what the website loads
