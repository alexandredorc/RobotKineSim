import numpy as np
from Point3D import Point3D,displayLine


def displayGrid(size,screen,cam):
    cell=0.25
    for i in range(-size,size+1):
        p11=Point3D([size*cell,i*cell,0])
        p12=Point3D([-size*cell,i*cell,0])
        p21=Point3D([i*cell,size*cell,0])
        p22=Point3D([i*cell,-size*cell,0])
        displayLine(p11,p12,screen,[100,100,100],1,cam)
        displayLine(p21,p22,screen,[100,100,100],1,cam)

def displayFrame(T,screen,cam):
    size=0.05
    U=np.array([[0,size,0,0],
                [0,0,size,0],
                [0,0,0,size],
                [1,1,1,1]])

    V=np.transpose(np.dot(T,U))
    pc=Point3D(V[0])
    px=Point3D(V[1])
    py=Point3D(V[2])
    pz=Point3D(V[3])
    displayLine(pc,px,screen,[255,0,0],3,cam)
    displayLine(pc,py,screen,[0,255,0],3,cam)
    displayLine(pc,pz,screen,[0,0,255],3,cam)
