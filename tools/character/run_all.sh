#!/usr/bin/env bash
# Rebuild the 3D character from source files. Run from anywhere:  bash tools/character/run_all.sh
# Needs: python3 with numpy scipy pillow pygltflib (pip install -r tools/character/requirements.txt), and node.
set -e
cd "$(dirname "$0")"
echo "1/5 stickers";  python3 make_stickers.py
echo "2/5 model";     python3 build_model.py
echo "3/5 camera";    python3 camera_path.py
echo "4/5 shrink";    mkdir -p work
npx -y @gltf-transform/cli@4 prune work/me_cam.glb work/me_pr.glb
npx -y @gltf-transform/cli@4 quantize work/me_pr.glb work/me_q.glb
echo "5/5 install";   mkdir -p ../../web/public/models && cp work/me_q.glb ../../web/public/models/me.glb
ls -l ../../web/public/models/me.glb
echo "Done. Now: cd web && npm run dev  (or npm run build)"
