import numpy as np 
import pygame
from math import sin, cos, sqrt,pi
import copy
class Camera:
    def __init__(self,view=[0,0],center=[0,0,0],depth=10,res_mile=100,dist=[1,30],zoom=1):
        
        self.frame=np.eye(4)
        self.view=view
        self.center=center
        self.depth=depth
        self.res=res_mile
        self.zoom=zoom
        self.dist=dist
        self.width=800
        self.height=600
        self.sensitive=1
        self.mousepoint=[-1,-1]
        self.mousestate=False
        self.saveview=copy.copy(self.view)

    def get_frame(self):
       
        vec=np.array([self.depth*sin(self.view[0])*cos(self.view[1]),self.depth*sin(self.view[0])*sin(self.view[1]),self.depth*cos(self.view[0])])
       
        axisz=normalize(-vec)
        axisy=normalize(np.array([-cos(self.view[0])*cos(self.view[1]),-cos(self.view[0])*sin(self.view[1]),sin(self.view[0])]))
        axisx=normalize(np.array([-sin(self.view[1]),cos(self.view[1]),0]))
        
        R=np.linalg.inv(np.column_stack((axisx,axisy,axisz)))
        
        trans=np.eye(4)
        trans[:3,:3]=R
        
        trans[2][3]=self.depth
        self.frame=trans
    
    def mouseClick(self):
        pos=pygame.mouse.get_pos()
        state=pygame.mouse.get_pressed()[0]
        if not state:
            self.mousestate=False
        elif state and not self.mousestate:
            self.mousestate=True
            self.mousepoint=pos
            self.saveview=copy.copy(self.view)
        if self.mousestate:
            self.changeView()

    def changeView(self):
        pos=pygame.mouse.get_pos()
        x=pos[0]-self.mousepoint[0]
        y=pos[1]-self.mousepoint[1]
        move=self.sensitive*pi
        width, height= pygame.display.get_surface().get_size()
        self.view[1]=self.saveview[1]+(x*2*move/width)
        self.view[1]%=2*pi
        if self.saveview[0]+(y*move/height)<=0:
            self.view[0]=0.01
        elif self.saveview[0]+(y*move/height)>=pi:
            self.view[0]=pi-0.01
        else:
            self.view[0]=self.saveview[0]+(y*move/height)
        

def normalize(vector):
    norm= sqrt(np.sum(np.square(vector)))
    if norm<0:
        print(norm, vector)
    else:
        return vector/norm

