import pygame
import sys
from math import pi
from Camera import Camera
from Point3D import Point3D,displayLine
from DH import generateDH
import numpy as np

cam=Camera([pi/2,0],[0,0,0])

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption('DH advance cheat mode')

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

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

def changeTheta(thetas):
    
    if pygame.key.get_pressed()[pygame.K_0]:
        thetas[0]+=0.01
    if pygame.key.get_pressed()[pygame.K_1]:
        thetas[1]+=0.01
    if pygame.key.get_pressed()[pygame.K_2]:
        thetas[2]+=0.01
    if pygame.key.get_pressed()[pygame.K_3]:
        thetas[3]+=0.01
    if pygame.key.get_pressed()[pygame.K_4]:
        thetas[4]+=0.01
    if pygame.key.get_pressed()[pygame.K_5]:
        thetas[5]+=0.01
    if pygame.key.get_pressed()[pygame.K_6]:
        thetas[6]+=0.01
    return thetas
    
thetas=[0,0,0,0,0,0]
DH_mat=np.array([[ 0     ,   0 , 0   ,thetas[0]]
                    ,[ 0.050 ,-pi/2, 0   ,thetas[1]]
                    ,[ 0.425 , 0   ,0.050,thetas[2]]
                    ,[ 0     ,-pi/2,0.425,thetas[3]]
                    ,[ 0     , pi/2, 0   ,thetas[4]]
                    ,[ 0     , -pi/2, 0.1 ,thetas[5]]])

frames=generateDH(DH_mat)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black color
    screen.fill((0, 0, 0))
    cam.keysCLick()
    cam.mouseClick()
    cam.get_frame()
    displayGrid(5,screen,cam)
    thetas=changeTheta(thetas)
    DH_mat=np.array([[ 0     ,   0 , 0   ,thetas[0]]
                    ,[ 0.050 ,-pi/2, 0   ,thetas[1]]
                    ,[ 0.425 , 0   ,0.050,thetas[2]]
                    ,[ 0     ,-pi/2,0.425,thetas[3]]
                    ,[ 0     , pi/2, 0   ,thetas[4]]
                    ,[ 0     , -pi/2, 0.1 ,thetas[5]]])

    frames=generateDH(DH_mat)

    for i in range(len(frames)-1):
        p1=Point3D(frames[i][:,3])
        p2=Point3D(frames[i+1][:,3])
        displayLine(p1,p2,screen,white,1,cam)
    for f in frames:
        displayFrame(f,screen,cam) 
    
    # Update the display
    pygame.display.flip()

# Quit Pygame properly
pygame.quit()
sys.exit()

