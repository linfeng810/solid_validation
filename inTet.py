import numpy as np 

""" test if a point is inside a tetrahedron
from: https://stackoverflow.com/a/61703017
by Philipp B.

Usage: 
bool output=pointInside(v0,v1,v2,v3,p)
input: v0, v1, v2, v3 - np array shape(3) or list(3): nodes of tetrahedron
       p - np array shape(3) or list(3): a point to be tested
       if input is list, will transform to nparray
"""

def det3x3(b,c,d):
    return b[0]*c[1]*d[2] + c[0]*d[1]*b[2] + d[0]*b[1]*c[2] - d[0]*c[1]*b[2] - c[0]*b[1]*d[2] - b[0]*d[1]*c[2]

def pointInside(v0,v1,v2,v3,p):
    v0=np.asarray(v0)
    v1=np.asarray(v1)
    v2=np.asarray(v2)
    v3=np.asarray(v3)
    p =np.asarray(p)
    a = v0 - p
    b = v1 - p
    c = v2 - p
    d = v3 - p
    detA = det3x3(b,c,d)
    detB = det3x3(a,c,d)
    detC = det3x3(a,b,d)
    detD = det3x3(a,b,c)
    ret0 = detA > 0.0 and detB < 0.0 and detC > 0.0 and detD < 0.0
    ret1 = detA < 0.0 and detB > 0.0 and detC < 0.0 and detD > 0.0
    return ret0 or ret1
