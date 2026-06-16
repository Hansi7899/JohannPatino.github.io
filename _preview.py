"""CPU-only orthographic preview of the voxel character (mirrors scene.html).
Flags: --office (office outfit), --walk (mid-stride leg swing)."""
import math, sys
from PIL import Image, ImageDraw

OFFICE = "--office" in sys.argv
PHI    = 0.34 if "--walk" in sys.argv else 0.0

def hx(v): return ((v>>16)&255,(v>>8)&255,v&255)
HAIR=hx(0x18100a); SKIN=hx(0xc88e63); EYE=hx(0x18100a)
MOUTH=hx(0x7c4038); EYEWHITE=hx(0xf0eee8)
SHIRT=hx(0xb0ada8); LOGO=hx(0xd4bc3a); SHORTS=hx(0x887740)
SHOE=hx(0x0e0e0e); STRAP=hx(0x2a2a32); GLASS=hx(0x0c0c10)
OFFICE_BLUE=hx(0x4a7fc0); PANTS=hx(0x151720); COLLAR=hx(0xedf1f6)
BUTTON=hx(0xd8e2f0); POCKET=hx(0x3a65a8); BELT=hx(0x121212); BUCKLE=hx(0xb0b0b0)

def gar(c): return OFFICE_BLUE if (OFFICE and c==SHIRT) else c
HIP_Y = -0.30

B=[]
def box(w,h,d,c,x,y,z,phi=0.0): B.append((w,h,d,c,x,y,z,phi))
def legbox(w,h,d,c,x,y,z): box(w,h,d,c,x,y,z, PHI if x<0 else -PHI)

SLEEVE = OFFICE_BLUE if OFFICE else SKIN

# HEAD — single face block + simple hair
box(0.72,0.80,0.44,SKIN,0,1.10,0)          # face
box(0.78,0.22,0.48,HAIR,0,1.46,0)          # hair crown
box(0.70,0.13,0.08,HAIR,0,1.34,0.24)       # front fringe
box(0.10,0.58,0.46,HAIR,-0.41,1.17,0)      # L side
box(0.10,0.58,0.46,HAIR, 0.41,1.17,0)      # R side
box(0.20,0.06,0.05,HAIR,-0.17,1.24,0.23)   # brow L
box(0.20,0.06,0.05,HAIR, 0.17,1.24,0.23)   # brow R
box(0.18,0.05,0.05,MOUTH,0,0.85,0.23)      # mouth
if OFFICE:
    box(0.20,0.14,0.06,EYEWHITE,-0.18,1.10,0.23)
    box(0.20,0.14,0.06,EYEWHITE, 0.18,1.10,0.23)
    box(0.09,0.12,0.05,EYE,     -0.18,1.10,0.245)
    box(0.09,0.12,0.05,EYE,      0.18,1.10,0.245)
else:
    box(0.22,0.16,0.06,GLASS,-0.18,1.10,0.24)
    box(0.22,0.16,0.06,GLASS, 0.18,1.10,0.24)
    box(0.09,0.05,0.06,GLASS, 0,   1.13,0.24)

# NECK / TORSO
box(0.22,0.16,0.24,SKIN,0,0.66,0)
box(0.86,0.74,0.44,gar(SHIRT),0,0.22,0)
if OFFICE:
    box(0.44,0.10,0.45,COLLAR,0,0.52,0)
    box(0.06,0.68,0.05,POCKET,0,0.20,0.235)
    box(0.14,0.12,0.04,POCKET,-0.20,0.34,0.235)
    box(0.82,0.08,0.44,BELT,0,-0.12,0)
    box(0.10,0.08,0.04,BUCKLE,0,-0.12,0.235)
    for by in (0.44,0.28,0.12,-0.04): box(0.05,0.05,0.04,BUTTON,0,by,0.245)
else:
    box(0.82,0.22,0.42,SHIRT,0,-0.26,0)
    box(0.22,0.26,0.04,LOGO,0,0.24,0.235)
    box(0.08,0.60,0.04,STRAP,-0.25,0.26,0.235)
    box(0.08,0.60,0.04,STRAP, 0.25,0.26,0.235)

# ARMS
for side in (-1,1):
    px,py=side*0.57,0.54
    box(0.28,0.28,0.42,gar(SHIRT),px,py-0.10,0)
    box(0.24,0.40,0.38,SLEEVE,    px,py-0.42,0)
    box(0.24,0.14,0.36,SKIN,      px,py-0.66,0)

# LOWER
legbox(0.34,0.14,0.50,SHOE,-0.22,-1.28,0.07)
legbox(0.34,0.14,0.50,SHOE, 0.22,-1.28,0.07)
if OFFICE:
    box(0.82,0.30,0.42,PANTS,0,-0.21,0)
    legbox(0.38,0.94,0.40,PANTS,-0.21,-0.77,0)
    legbox(0.38,0.94,0.40,PANTS, 0.21,-0.77,0)
else:
    legbox(0.26,0.60,0.30,SKIN,-0.22,-0.92,0)
    legbox(0.26,0.60,0.30,SKIN, 0.22,-0.92,0)
    box(0.84,0.18,0.42,SHORTS,0,-0.27,0)
    legbox(0.40,0.52,0.42,SHORTS,-0.21,-0.58,0)
    legbox(0.40,0.52,0.42,SHORTS, 0.21,-0.58,0)

# ── render ──
CORNERS=[(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]
FACES=[((4,5,6,7),(0,0,1)),((0,1,2,3),(0,0,-1)),((1,5,6,2),(1,0,0)),
       ((0,4,7,3),(-1,0,0)),((3,2,6,7),(0,1,0)),((0,1,5,4),(0,-1,0))]
def rotY(p,a): c,s=math.cos(a),math.sin(a); x,y,z=p; return (c*x+s*z,y,-s*x+c*z)
def rotX(p,a): c,s=math.cos(a),math.sin(a); x,y,z=p; return (x,c*y-s*z,s*y+c*z)
def swingX(p,phi):
    if not phi: return p
    x,y,z=p; c,s=math.cos(phi),math.sin(phi); yy=y-HIP_Y
    return (x, c*yy-s*z+HIP_Y, s*yy+c*z)
def swingXvec(v,phi):
    if not phi: return v
    x,y,z=v; c,s=math.cos(phi),math.sin(phi); return (x, c*y-s*z, s*y+c*z)

def render(yaw,pitch,fname):
    W,H=460,640; SCALE=150; CX,CY=W/2,H*0.46
    img=Image.new("RGB",(W,H),(238,240,247)); dr=ImageDraw.Draw(img)
    cen=(0,0.15,0); light=(0.4,0.7,0.6)
    ln=math.sqrt(sum(v*v for v in light)); light=tuple(v/ln for v in light)
    polys=[]
    for (w,h,d,col,bx,by,bz,phi) in B:
        verts=[]
        for cx_,cy_,cz_ in CORNERS:
            p=swingX((bx+cx_*w/2,by+cy_*h/2,bz+cz_*d/2),phi)
            p=(p[0]-cen[0],p[1]-cen[1],p[2]-cen[2]); verts.append(rotX(rotY(p,yaw),pitch))
        for idx,nrm in FACES:
            n=rotX(rotY(swingXvec(nrm,phi),yaw),pitch)
            if n[2]<=0.01: continue
            depth=sum(verts[i][2] for i in idx)/4
            sh=max(0.30,n[0]*light[0]+n[1]*light[1]+n[2]*light[2]); sh=0.55+0.45*sh
            c=tuple(min(255,int(v*sh)) for v in col)
            pts=[(CX+verts[i][0]*SCALE,CY-verts[i][1]*SCALE) for i in idx]
            polys.append((depth,pts,c))
    polys.sort(key=lambda t:t[0])
    for _,pts,c in polys: dr.polygon(pts,fill=c,outline=tuple(int(v*0.7) for v in c))
    img.save(fname); print("saved",fname)

tag=("office" if OFFICE else "casual")+("_walk" if PHI else "")
render(0.0,0.05,f"media/_pv_{tag}_front.png")
render(-0.55,0.12,f"media/_pv_{tag}_34.png")
