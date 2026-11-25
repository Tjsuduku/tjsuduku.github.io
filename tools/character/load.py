import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
import numpy as np, io
from pygltflib import GLTF2
from PIL import Image
g=GLTF2().load_binary(SOURCE_GLB)
blob=g.binary_blob()
CT={5126:np.float32,5123:np.uint16,5125:np.uint32}
NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}
def acc(i):
    a=g.accessors[i]; bv=g.bufferViews[a.bufferView]
    n=NC[a.type]; dt=CT[a.componentType]
    off=(bv.byteOffset or 0)+(a.byteOffset or 0)
    arr=np.frombuffer(blob,dtype=dt,count=a.count*n,offset=off).reshape(a.count,n) if not bv.byteStride or bv.byteStride==n*np.dtype(dt).itemsize else None
    return arr
def img(i):
    bv=g.bufferViews[g.images[i].bufferView]
    return Image.open(io.BytesIO(blob[bv.byteOffset:bv.byteOffset+bv.byteLength])).convert('RGB')
