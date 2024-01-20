import numpy as np
import pygame
import copy
class Point3D:
    def __init__(self,xyz):
        if isinstance(xyz, list):
            xyz=np.array(xyz)
        if len(xyz)==3:
            xyz=np.append(xyz, 1)
        self.coord=xyz
        
        self.pixel=[0,0]
        self.depth=-1

    def displayPoint(self,cam,screen,size,color):
        self.get2Dview()
        if self.depth<=0:
            pygame.draw.circle(screen, color, self.pixel, 2)

    def get2Dview(self,cam):
        xyz=copy.copy(self.coord)
        if isinstance(xyz, list):
            xyz=np.array(xyz)
        if len(xyz)==3:
            xyz=np.append(xyz, 1)
        
        # tranformer le point actuel en point 3d pour la camera
        newdot=np.dot(cam.frame,np.array(xyz))
        width, height= pygame.display.get_surface().get_size()
        # on obtient regarde alors si il ce trouve dans l'espace de vision
        # 1 could be replace with minimum dist and depth*2 with maximum dist wich would make more sense
        
        if cam.iso:
            #print(newdot,width,cam.res)
            px=newdot[0]*width/cam.res
            px=-px+width/2
            py=-newdot[1]*height/cam.res
            py+=height/2

            self.pixel=[px,py]
            self.depth=newdot[2]
            return 0
        
        else:
            d=cam.focal-cam.depth
            px=(newdot[0]*cam.focal/(newdot[2]+d))*width/cam.res
            px=-px+width/2
            
            py=-(newdot[1]*cam.focal/(newdot[2]+d))*height/cam.res
            py+=height/2

            self.pixel=[px,py]
            self.depth=newdot[2]
            if (newdot[2]+d)<0:
                self.pixel=[px,py]
                self.depth=-1
                return -1
            return 0
        # finalement on map les coordoné réel du point en pixel (px,py) 
        # par apport à ca position en xy et sa profondeur
        print("error")
        self.pixel=[0,0]
        self.depth=-1

def get_closestP(p1,p2,cam):

    newdot1=np.dot(cam.frame,p1.coord)

    newdot2=np.dot(cam.frame,p2.coord)
    alpha=(0.1-cam.focal+cam.depth-newdot1[2])/(newdot2[2]-newdot1[2])
    return Point3D(p1.coord+alpha*(p2.coord-p1.coord))

def displayLine(p1, p2, screen, color, size,cam):
    
    p1.get2Dview(cam)
    p2.get2Dview(cam)
    if p1.depth!=-1 and p2.depth!=-1:
        pygame.draw.line(screen,color,p1.pixel,p2.pixel,size)
    elif p1.depth==-1 and p2.depth==-1:
        return 0
    elif p1.depth!=-1:
        p2=get_closestP(p1,p2,cam)
        p2.get2Dview(cam)
        pygame.draw.line(screen,color,p1.pixel,p2.pixel,size)
    elif p2.depth!=-1:
        p1=get_closestP(p2,p1,cam)
        p1.get2Dview(cam)
        pygame.draw.line(screen,color,p1.pixel,p2.pixel,size)