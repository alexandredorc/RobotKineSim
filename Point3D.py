import numpy as np
import pygame
import copy
class Point3D:
    def __init__(self,xyz):
        self.coord=xyz
        
        self.pixel=[0,0]
        self.depth=-1

    def displayPoint(self,cam,screen,size,color):
        self.get2Dview()
        if self.depth<=0:
            pygame.draw.circle(screen, color, self.pixel, 2)

    def get2Dview(self,cam):
        xyz=copy.copy(self.coord)
        
        xyz.append(1)
        # tranformer le point actuel en point 3d pour la camera
      
        newdot=np.dot(cam.frame,np.array(xyz))
        width, height= pygame.display.get_surface().get_size()
        # on obtient regarde alors si il ce trouve dans l'espace de vision
        # 1 could be replace with minimum dist and depth*2 with maximum dist wich would make more sense
        if  newdot[2]<=cam.dist[1]:
            zoom=(cam.dist[0]-newdot[2]/(cam.dist[1]-cam.dist[0]))
            effec_zoom=1+zoom*(1-cam.zoom)
            px=newdot[0]*(width*cam.res/1000)/effec_zoom
            py=-newdot[1]*(height*cam.res/1000)/effec_zoom
            px+=width/2
            py+=height/2
            self.pixel=[px,py]
            self.depth=newdot[2]
            return 0
        # finalement on map les coordoné réel du point en pixel (px,py) 
        # par apport à ca position en xy et sa profondeur
        print("error")
        self.pixel=[0,0]
        self.depth=-1

def displayLine(p1, p2, screen, color, size,cam):
    p1.get2Dview(cam)
    p2.get2Dview(cam)
    if p1.depth!=-1 and p2.depth!=-1:
        pygame.draw.line(screen,color,p1.pixel,p2.pixel,size)