import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
exec(open(os.path.join(HERE,'load.py')).read())
import io
from scipy.spatial import cKDTree
from scipy.interpolate import RBFInterpolator
from scipy.ndimage import gaussian_filter
from PIL import Image
def sstep(a,b,x):
    t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
p=g.meshes[0].primitives[0]
P=acc(p.attributes.POSITION).astype(np.float64).copy()
UV=acc(p.attributes.TEXCOORD_0).astype(np.float64)
I=acc(p.indices).reshape(-1,3).astype(np.int64)
tex0=img(g.textures[g.materials[0].pbrMetallicRoughness.baseColorTexture.index].source); T0=np.asarray(tex0); TH,TW,_=T0.shape
vcol=T0[np.clip(((UV[:,1]%1)*(TH-1)).astype(int),0,TH-1),np.clip(((UV[:,0]%1)*(TW-1)).astype(int),0,TW-1)].astype(np.float64)

# ---------- eye geometry params ----------
EC=[(-0.112,0.486),(0.112,0.486)]   # eye centres (x,y)
AB=0.105;BB=0.075                    # uv box half sizes
A_IN,A_OUT,B_UP,B_LO=0.105,0.090,0.056,0.075
a_open,bu,bl=0.054,0.020,0.019      # almond opening half-width / upper / lower
ZS=0.72
ball_scale=1.12; ball_dz=-0.008-0.0668*(ball_scale-1)+0.002
ball_c=np.array([0.0,0.0,0.2373+ball_dz]); ball_R=0.0668*ball_scale

def outer_r(cx,dx,dy):
    # normalised radius wrt asymmetric ellipse (1 = patch outer boundary)
    inner=(dx*np.sign(cx)<0)
    ax=np.where(inner,A_IN,A_OUT); by=np.where(dy>0,B_UP,B_LO)
    return np.sqrt((dx/ax)**2+(dy/by)**2)
def inzone(xy,cx,cy,sc=ZS,sb=None):
    return outer_r(cx,xy[:,0]-cx,xy[:,1]-cy)<(sc if sb is None else sc)
cent=P[I].mean(1)
dele=np.zeros(len(I),bool)
for cx,cy in EC: dele|=inzone(cent[:,:2],cx,cy)&(cent[:,2]>0.15)
print('triangles removed',dele.sum())
Ikeep=I[~dele]

# ---------- shoulders (wider, sloped; neck untouched) ----------
x,y=P[:,0],P[:,1]
t=sstep(-0.20,-0.45,y); wx=sstep(0.10,0.30,np.abs(x))
P[:,0]=x*(1+0.34*t*wx); P[:,1]=y-0.07*t*sstep(0.25,0.6,np.abs(x))

# ---------- face height field around the eyes ----------
hair=vcol.sum(1)<200
used=np.unique(Ikeep)
sel=np.zeros(len(P),bool); sel[used]=True
sel&=(P[:,2]>0.2)&(np.abs(P[:,0])<0.3)&(P[:,1]>0.36)&(P[:,1]<0.62)&(~hair)
# front shell via cell maxima
cell=0.008; key=np.round(P[sel][:,:2]/cell).astype(int)
best={}
for q,(k0,k1) in zip(P[sel],map(tuple,key)):
    if (k0,k1) not in best or q[2]>best[(k0,k1)][2]: best[(k0,k1)]=q
Q=np.array(list(best.values()))
# drop points inside deleted zones
ok=np.ones(len(Q),bool)
for cx,cy in EC: ok&=~inzone(Q[:,:2],cx,cy,1.0)
Q2=Q.copy(); _q2t=cKDTree(Q2[:,:2])
Q=Q[ok]; print('height pts',len(Q))
rbf=RBFInterpolator(Q[:,:2],Q[:,2],kernel='thin_plate_spline',smoothing=2e-5,neighbors=60)
def face_z(xy): return rbf(xy)

# ---------- patch mesh ----------
K,R=72,16
ts=np.concatenate([[-0.12,-0.05],np.linspace(0,1,R)**1.35]); R=len(ts)
verts=[];uvs=[];idx=[]
# almond rim traced from the Higgsfield front render (eye spacing scaled to the model)
IN_X,OUT_X,IN_Y,OUT_Y=0.0567,0.171,0.4768,0.4737
HU,HL=0.0255,0.0072
KU,QU=np.log(.5)/np.log(.46),0.72
KL,QL=np.log(.5)/np.log(.537),1.0
def rim_pt(cx,cy,th):
    sg=np.sign(cx)
    xin,xout=sg*IN_X,sg*OUT_X
    if xin>xout: xr,yr,xl,yl,right_is_inner=xin,IN_Y,xout,OUT_Y,True
    else: xr,yr,xl,yl,right_is_inner=xout,OUT_Y,xin,IN_Y,False
    c=np.cos(th); s_=np.sin(th)
    tx=(1-c)/2
    u=tx if right_is_inner else 1-tx
    u=min(max(u,0.0),1.0)
    px=xr+(xl-xr)*tx; base=yr+(yl-yr)*tx
    if s_>=0: py=base+HU*np.sin(np.pi*u**KU)**QU
    else: py=base-HL*np.sin(np.pi*u**KL)**QL
    return px,py
for e,(cx,cy) in enumerate(EC):
    base=len(verts)
    for r,tt in enumerate(ts):
        for k in range(K):
            th=2*np.pi*k/K
            rx,ry=rim_pt(cx,cy,th)
            ca,sa_=np.cos(th),np.sin(th); ox=cx+ca*(A_IN if ca*np.sign(cx)<0 else A_OUT); oy=cy+sa_*(B_UP if sa_>0 else B_LO)
            w=max(tt,0.0)
            px=rx*(1-w)+ox*w; py=ry*(1-w)+oy*w
            if tt<0: px=cx+(rx-cx)*(1+tt); py=cy+(ry-cy)*(1+tt)
            # z
            dx,dy=px-(cx+0.0),py-cy
            inside=max(ball_R**2-(rx-cx)**2-(ry-cy)**2,1e-6)
            zf_rim=float(face_z(np.array([[rx,ry]]))[0])
            z_rim=ball_c[2]+np.sqrt(inside)+0.0028
            if tt<0:
                verts.append((px,py,ball_c[2]+np.sqrt(inside)+0.0028+tt*0.12))
                u=(px-cx)/(2*AB)+0.5; v=1-((py-cy)/(2*BB)+0.5); uvs.append((e*0.5+u*0.5,v)); continue
            zf=float(face_z(np.array([[px,py]]))[0])+0.0012
            _inner=max(0.0,-np.cos(th)*np.sign(cx)) if False else max(0.0,np.cos(th)*(-np.sign(cx)))
            s=sstep(0,0.32+0.45*_inner**1.5,tt)
            z=z_rim*(1-s)+zf*s
            if np.sin(th)>0: z+=0.0025*np.exp(-((tt-0.14)/0.10)**2)
            else: z+=0.0025*np.exp(-((tt-0.12)/0.09)**2)
            if tt>0.55:
                _d,_i=_q2t.query([px,py],k=4); _w=1/(_d+1e-4); zh=float((Q2[_i,2]*_w).sum()/_w.sum())
                bl_=sstep(0.55,0.85,tt); z=z*(1-bl_)+max(z,zh+0.0015)*bl_
            _ins2=ball_R**2-(px-cx)**2-(py-cy)**2
            if _ins2>0: z=max(z,ball_c[2]+np.sqrt(_ins2)+0.003)
            verts.append((px,py,z))
            u=(px-cx)/(2*AB)+0.5; v=1-((py-cy)/(2*BB)+0.5)
            uvs.append((e*0.5+u*0.5,v))
    for r in range(R-1):
        for k in range(K):
            a_=base+r*K+k; b_=base+r*K+(k+1)%K; c_=base+(r+1)*K+k; d_=base+(r+1)*K+(k+1)%K
            idx+=[a_,c_,b_, b_,c_,d_]
V=np.array(verts,np.float32); UVp=np.array(uvs,np.float32); IDX=np.array(idx,np.uint16)
# smooth normals
Nn=np.zeros_like(V)
tri=IDX.reshape(-1,3)
fn=np.cross(V[tri[:,1]]-V[tri[:,0]],V[tri[:,2]]-V[tri[:,0]])
for j in range(3): np.add.at(Nn,tri[:,j],fn)
Nn/=np.linalg.norm(Nn,axis=1,keepdims=True)+1e-9
# make normals point to +z (outward)
Nn[Nn[:,2]<0]*=-1
HN=acc(p.attributes.NORMAL).astype(np.float32)
_ht=cKDTree(P[used]); _d,_ii=_ht.query(V.astype(np.float64),k=6)
hn=HN[used][_ii].mean(1); hn/=np.linalg.norm(hn,axis=1,keepdims=True)+1e-9
tt_v=np.tile(np.repeat(ts,K),2)
wb=sstep(0.35,0.85,tt_v)[:,None]
Nn=Nn*(1-wb)+hn*wb; Nn/=np.linalg.norm(Nn,axis=1,keepdims=True)+1e-9
print('patch verts',len(V))

# ---------- bake patch texture (1024x512) ----------
TW2,TH2=1024,512
tx=np.zeros((TH2,TW2,4),np.float32)
hair2=vcol.sum(1)<380
src=np.where(~hair2&(P[:,2]>0.2)&(np.abs(P[:,0])<0.3)&(P[:,1]>0.35)&(P[:,1]<0.62))[0]
src=np.array([i for i in src if i in set(used.tolist())])
_med=np.median(vcol[src].sum(1)); src=src[vcol[src].sum(1)>0.88*_med]
srcxy=P[src,:2]; sc=vcol[src]
for e,(cx,cy) in enumerate(EC):
    msk=~inzone(srcxy,cx,cy,0.97)
    tree=cKDTree(srcxy[msk]); sc_e=sc[msk]
    w_=512;h_=512
    cols=np.arange(w_);rows=np.arange(h_)
    X=cx+((cols+0.5)/w_-0.5)*2*AB; Y=cy+(0.5-(rows+0.5)/h_)*2*BB
    XX,YY=np.meshgrid(X,Y)
    d,ii=tree.query(np.c_[XX.ravel(),YY.ravel()],k=10)
    wgt=1/(d+1e-4); col=(sc_e[ii]*wgt[...,None]).sum(1)/wgt.sum(1)[:,None]
    col=col.reshape(h_,w_,3)
    for c in range(3): col[...,c]=gaussian_filter(col[...,c],6)
    # rim distance shading
    th=np.linspace(0,2*np.pi,400,endpoint=False)
    rp=np.array([rim_pt(cx,cy,tt_) for tt_ in th])
    rt=cKDTree(rp); dd,_=rt.query(np.c_[XX.ravel(),YY.ravel()]); dd=dd.reshape(h_,w_)
    from matplotlib.path import Path as _Path
    _ins=_Path(rp).contains_points(np.c_[XX.ravel(),YY.ravel()]).reshape(XX.shape)
    upw=sstep(-0.004,0.006,YY-0.4755); up=upw>0.5
    lash=np.exp(-(dd/0.0045)**2)*(0.18+0.78*upw)
    crease=np.exp(-((dd-0.012)/0.0022)**2)*0.22*upw*np.exp(-((XX-cx)/0.05)**2)
    shade=np.clip(lash+crease,0,1)[...,None]
    dark=np.array([40,24,20.0])
    col=col*(1-shade)+dark*shade
    # soft pink waterline lower
    wl=(np.exp(-((dd-0.0045)/0.0025)**2)*(1-upw))[...,None]*0.3
    col=col*(1-wl)+np.array([205,120,105.0])*wl
    _sock=(_ins*sstep(0.0,0.004,dd))[...,None]
    col=col*(1-_sock)+np.array([92,52,46.0])*_sock
    # alpha: fade near outer ellipse
    rr=outer_r(cx,(XX-cx).ravel(),(YY-cy).ravel()).reshape(XX.shape)
    alpha=1-sstep(0.86,1.0,rr)
    tx[:,e*512:(e+1)*512,:3]=col; tx[:,e*512:(e+1)*512,3]=alpha*255
# note atlas is 1024 wide x 512 high; uv v maps top->bottom
patch_png=io.BytesIO(); Image.fromarray(np.clip(tx,0,255).astype(np.uint8),'RGBA').save(patch_png,'PNG'); patch_png=patch_png.getvalue()
Image.fromarray(np.clip(tx,0,255).astype(np.uint8),'RGBA').save(os.path.join(WORK,'patch_tex.png'))

# ---------- eyeball texture: warm sclera, original iris ----------
tex=Image.open(EYETEX).convert('RGB'); a=np.asarray(tex).astype(np.float32)
H,W,_=a.shape; yy,xx=np.mgrid[0:H,0:W]; dd2=np.hypot(xx-256,yy-256)
sclera=np.array([232,224,214],np.float32)
shade=np.clip(1-0.38*np.clip((dd2-95)/200,0,1),0.62,1)[...,None]
SC=0.75/ball_scale
sx_=np.clip(256+(xx-256)/SC,0,W-1).astype(int); sy_=np.clip(256+(yy-256)/SC,0,H-1).astype(int)
a_sc=a[sy_,sx_]
irism=np.clip((92*SC-dd2)/3,0,1)[...,None]
out=sclera*shade*(1-irism)+a_sc*irism*np.where(a_sc.sum(2,keepdims=True)>600,1.0,0.78)
buf=io.BytesIO(); Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(buf,'JPEG',quality=92); eyejpg=buf.getvalue()

# ---------- base cap ----------
low=P[:,1]<-0.70
ax_=np.abs(P[low,0]).max()*0.97; zc=(P[low,2].max()+P[low,2].min())/2; az=(P[low,2].max()-P[low,2].min())/2*0.97
yc=float(P[:,1].min())+0.012; KK=48
ring=np.array([[ax_*np.cos(q),yc,zc+az*np.sin(q)] for q in np.linspace(0,2*np.pi,KK,endpoint=False)],np.float32)
CP=np.vstack([[0,yc,zc],ring]).astype(np.float32); CI=[]
for i in range(KK): CI+=[0,1+i,1+(i+1)%KK]
CI=np.array(CI,np.uint16); CN=np.tile(np.array([0,-1,0],np.float32),(len(CP),1))

# ---------- Sen-style skin material: full base colour, roughness map, normal map, no emissive hack ----------
BF=[0.83,0.75,0.73]
from scipy.ndimage import sobel
Lm=T0.astype(np.float32).mean(2)/255
r_,g_,b_=[T0[...,i].astype(np.float32) for i in range(3)]
rough=np.full(Lm.shape,0.52,np.float32)
rough[Lm<0.18]=0.42                       # hair / brows a touch glossier
lips=(r_>g_*1.45)&(r_>120)
rough[lips]=0.36
rough=gaussian_filter(rough,2)+ (np.random.default_rng(1).random(Lm.shape).astype(np.float32)-0.5)*0.04
mr=np.zeros(T0.shape,np.uint8); mr[...,0]=255; mr[...,1]=np.clip(rough*255,0,255); mr[...,2]=0
hgt=Lm-gaussian_filter(Lm,6); hgt=gaussian_filter(hgt,0.8)
gx=np.clip(sobel(hgt,1),-0.25,0.25); gy=np.clip(sobel(hgt,0),-0.25,0.25)
st=0.0
nx=-gx*st; ny=gy*st; nz=np.ones_like(nx); nl=np.sqrt(nx**2+ny**2+nz**2)
nm=np.stack([(nx/nl*0.5+0.5),(ny/nl*0.5+0.5),(nz/nl*0.5+0.5)],-1)
def jpg(a):
    b=io.BytesIO(); Image.fromarray(a).save(b,'JPEG',quality=90); return b.getvalue()
MR_BYTES=jpg(mr); NM_BYTES=jpg((nm*255).astype(np.uint8))
Image.fromarray(mr).resize((512,512)).save(os.path.join(WORK,'dbg_mr.png')); Image.fromarray((nm*255).astype(np.uint8)).resize((512,512)).save(os.path.join(WORK,'dbg_nm.png'))
# ---------- logo stickers (decals) ----------
STK=[('sfu',0.0,0.418,0.078,0),
     ('jaalik',0.19,0.4,0.075,8),('reframes',0.215,0.338,0.09,-6),
     ('telus',0.205,0.262,0.1,-8),
     ('skechers',-0.205,0.392,0.095,6),
     ('cloverdale',-0.178,0.3,0.068,-5),('instagram',-0.24,0.345,0.05,8),('facebook',-0.122,0.338,0.048,-10),('tiktok',-0.245,0.268,0.05,6),('linkedin',-0.16,0.238,0.048,-8),
     ('boopdog',0.155,0.168,0.095,-8),
     ('chatgpt',-0.15,0.2,0.1,8),('claude',-0.14,0.145,0.095,4)]
import os

HNf=acc(p.attributes.NORMAL).astype(np.float64)
centK=P[Ikeep].mean(1); fnK=np.cross(P[Ikeep[:,1]]-P[Ikeep[:,0]],P[Ikeep[:,2]]-P[Ikeep[:,0]]); fnK/=np.linalg.norm(fnK,axis=1,keepdims=True)+1e-12
usedv=np.unique(Ikeep)
decals=[]
CENT={}
for name,sx,sy,sw,rot in STK:
    im=Image.open(STK_DIR+name+'.png'); sh=sw*im.height/im.width
    A_=P[Ikeep[:,0]];B_=P[Ikeep[:,1]];C_=P[Ikeep[:,2]]
    v0=C_[:,:2]-A_[:,:2]; v1=B_[:,:2]-A_[:,:2]; v2=np.array([sx,sy])-A_[:,:2]
    d00=(v0*v0).sum(1);d01=(v0*v1).sum(1);d11=(v1*v1).sum(1);d20=(v2*v0).sum(1);d21=(v2*v1).sum(1)
    den=d00*d11-d01*d01+1e-18; uu_=(d11*d20-d01*d21)/den; vv_=(d00*d21-d01*d20)/den
    hit=(uu_>=0)&(vv_>=0)&(uu_+vv_<=1)&(fnK[:,2]>0.1)
    zz=(A_[:,2]+uu_*(C_[:,2]-A_[:,2])+vv_*(B_[:,2]-A_[:,2]))[hit]
    cz=zz.max(); c=np.array([sx,sy,cz]); CENT[name]=c.tolist()
    nb=usedv[(np.linalg.norm(P[usedv]-c,axis=1)<0.025)]
    n=HNf[nb].mean(0); n/=np.linalg.norm(n)
    t=np.array([1.0,0,0]); t-=n*np.dot(t,n); t/=np.linalg.norm(t)
    b=np.cross(n,t)
    ang=np.radians(rot); t,b=t*np.cos(ang)+b*np.sin(ang), -t*np.sin(ang)+b*np.cos(ang)
    d=centK-c
    pt=(P[Ikeep]-c)@t; pb=(P[Ikeep]-c)@b
    selt=(pt.min(1)<sw*0.55)&(pt.max(1)>-sw*0.55)&(pb.min(1)<sh*0.55)&(pb.max(1)>-sh*0.55)&(np.abs(d@n)<(0.07 if name in ('sfu','skechers') else 0.05))&(fnK@n>-0.2)
    tri=Ikeep[selt]
    pos=P[tri].reshape(-1,3)+n*0.0025
    nor=HNf[tri].reshape(-1,3)
    dd=pos-c
    uu=(dd@t)/sw+0.5; vv=(dd@b)/sh+0.5
    uv=np.stack([uu,1-vv],1)
    ii=np.arange(len(pos),dtype=np.uint32)
    decals.append((name,pos.astype(np.float32),nor.astype(np.float32),uv.astype(np.float32),ii,open(STK_DIR+name+'.png','rb').read()))
    print('sticker',name,len(tri),'tris')
# ---------- write glb ----------
from pygltflib import BufferView, Accessor, Mesh, Primitive, Node, Material, Attributes, Image as GImage, Texture
blob=bytearray(g.binary_blob())
def add(data,target=None):
    while len(blob)%4: blob.append(0)
    off=len(blob); blob.extend(data)
    g.bufferViews.append(BufferView(buffer=0,byteOffset=off,byteLength=len(data),target=target)); return len(g.bufferViews)-1
def addacc(bv,ct,n,typ,mn=None,mx=None):
    g.accessors.append(Accessor(bufferView=bv,componentType=ct,count=n,type=typ,min=mn,max=mx)); return len(g.accessors)-1
pa=g.accessors[p.attributes.POSITION]
bv=add(P.astype(np.float32).tobytes(),34962); pa.bufferView=bv; pa.byteOffset=0; pa.min=P.min(0).tolist(); pa.max=P.max(0).tolist()
ia=g.accessors[p.indices]
Ik=Ikeep.astype(np.uint32)
bv=add(Ik.tobytes(),34963); ia.bufferView=bv; ia.byteOffset=0; ia.count=int(Ik.size); ia.componentType=5125; ia.min=[int(Ik.min())]; ia.max=[int(Ik.max())]
# head material -> Sen style
hm=g.materials[0]
hm.emissiveFactor=[0,0,0]; hm.emissiveTexture=None
hm.pbrMetallicRoughness.baseColorFactor=BF+[1]; hm.pbrMetallicRoughness.roughnessFactor=1.0; hm.pbrMetallicRoughness.metallicFactor=0.0
g.images.append(GImage(mimeType='image/jpeg',bufferView=add(MR_BYTES))); g.textures.append(Texture(source=len(g.images)-1,sampler=g.textures[0].sampler))
hm.pbrMetallicRoughness.metallicRoughnessTexture={'index':len(g.textures)-1}
g.images.append(GImage(mimeType='image/jpeg',bufferView=add(NM_BYTES))); g.textures.append(Texture(source=len(g.images)-1,sampler=g.textures[0].sampler))
hm.normalTexture={'index':len(g.textures)-1,'scale':1.0}
# eyeball texture
g.images[g.textures[g.materials[1].pbrMetallicRoughness.baseColorTexture.index].source].bufferView=add(eyejpg)
# eyeballs forward + scale
for n in g.nodes:
    if n.name in ('eye_L','eye_R'):
        n.translation=[n.translation[0],n.translation[1],n.translation[2]+ball_dz]; n.scale=[ball_scale]*3
# patch
bvp=add(patch_png); g.images.append(GImage(mimeType='image/png',bufferView=bvp)); img_i=len(g.images)-1
g.textures.append(Texture(source=img_i,sampler=g.textures[0].sampler)); tex_i=len(g.textures)-1
g.materials.append(Material(pbrMetallicRoughness={'baseColorFactor':BF+[1],'metallicFactor':0,'roughnessFactor':0.5,'baseColorTexture':{'index':tex_i}},alphaMode='BLEND',doubleSided=True,name='lid_patch_mat'))
mat_patch=len(g.materials)-1
aP=addacc(add(V.tobytes(),34962),5126,len(V),'VEC3',V.min(0).tolist(),V.max(0).tolist())
aN=addacc(add(Nn.astype(np.float32).tobytes(),34962),5126,len(V),'VEC3',Nn.min(0).tolist(),Nn.max(0).tolist())
aU=addacc(add(UVp.tobytes(),34962),5126,len(V),'VEC2',UVp.min(0).tolist(),UVp.max(0).tolist())
aI=addacc(add(IDX.tobytes(),34963),5123,len(IDX),'SCALAR',[0],[int(IDX.max())])
g.meshes.append(Mesh(name='lid_patch',primitives=[Primitive(attributes=Attributes(POSITION=aP,NORMAL=aN,TEXCOORD_0=aU),indices=aI,material=mat_patch)]))
g.nodes.append(Node(name='lid_patch',mesh=len(g.meshes)-1)); g.nodes[24].children.append(len(g.nodes)-1)
# cap
g.materials.append(Material(pbrMetallicRoughness={'baseColorFactor':[0.06,0.065,0.075,1],'metallicFactor':0,'roughnessFactor':0.8},doubleSided=True,name='cap_jacket'))
aCP=addacc(add(CP.tobytes(),34962),5126,len(CP),'VEC3',CP.min(0).tolist(),CP.max(0).tolist())
aCN=addacc(add(CN.tobytes(),34962),5126,len(CN),'VEC3',[0,-1,0],[0,-1,0])
aCI=addacc(add(CI.tobytes(),34963),5123,len(CI),'SCALAR',[0],[int(CI.max())])
g.meshes.append(Mesh(name='base_cap',primitives=[Primitive(attributes=Attributes(POSITION=aCP,NORMAL=aCN),indices=aCI,material=len(g.materials)-1)]))
g.nodes.append(Node(name='base_cap',mesh=len(g.meshes)-1)); g.nodes[24].children.append(len(g.nodes)-1)
from pygltflib import Sampler
g.samplers.append(Sampler(magFilter=9729,minFilter=9987,wrapS=33071,wrapT=33071)); smp=len(g.samplers)-1
man=g.nodes[24]
man.children=[cidx for cidx in man.children if not (g.nodes[cidx].name or '').startswith('sticker')]
for name,pos,nor,uv,ii,png in decals:
    g.images.append(GImage(mimeType='image/png',bufferView=add(png))); g.textures.append(Texture(source=len(g.images)-1,sampler=smp))
    g.materials.append(Material(pbrMetallicRoughness={'baseColorFactor':[0.66,0.66,0.66,1],'metallicFactor':0,'roughnessFactor':1.0,'baseColorTexture':{'index':len(g.textures)-1}},emissiveTexture={'index':len(g.textures)-1},emissiveFactor=[0.22,0.22,0.22],alphaMode='BLEND',doubleSided=True,name='logo_'+name))
    aP_=addacc(add(pos.tobytes(),34962),5126,len(pos),'VEC3',pos.min(0).tolist(),pos.max(0).tolist())
    aN_=addacc(add(nor.tobytes(),34962),5126,len(nor),'VEC3',nor.min(0).tolist(),nor.max(0).tolist())
    aU_=addacc(add(uv.tobytes(),34962),5126,len(uv),'VEC2',uv.min(0).tolist(),uv.max(0).tolist())
    aI_=addacc(add(ii.tobytes(),34963),5125,len(ii),'SCALAR',[0],[int(ii.max())])
    g.meshes.append(Mesh(name='logo_'+name,primitives=[Primitive(attributes=Attributes(POSITION=aP_,NORMAL=aN_,TEXCOORD_0=aU_),indices=aI_,material=len(g.materials)-1)]))
    g.nodes.append(Node(name='logo_'+name,mesh=len(g.meshes)-1)); man.children.append(len(g.nodes)-1)
g.buffers[0].byteLength=len(blob); g.set_binary_blob(bytes(blob)); g.save_binary(MODEL_V4); print('saved',len(blob))

import json; json.dump(CENT,open(CENTERS,'w'))
