import pygame
import sys
from math import pi
from Camera import Camera
from DH import generateDH
from Elements import *
from IHM import IHM
import numpy as np
import copy
from decimal import Decimal


# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption('DH advance cheat mode')

black=(0,0,0)
gray = (200, 200, 200)
white=(255,255,255)


cam=Camera([pi/2,0],[0,0,0],res_mile=2.5,iso=True)

thetas_init=[0,0,0,0,0,0]
DH_mat_init=np.array([[  0   ,  0 ,  0.1695    ,0]
                    ,[ 0        ,pi/2 , 0     ,pi/2]
                    ,[ 0.221325 , 0   , 0       ,0]
                    ,[ 0.035406 ,-pi/2, 0.235    ,0]
                    ,[ 0        , pi/2, 0 ,0]
                    ,[ 0.00925  ,-pi/2 , 0.0416   ,0]])

ihm=IHM(thetas_init,DH_mat_init,screen)



# Main loop
running = True
while running:
    
    ihm.setup_btns()
    
    screen.fill((0, 0, 0))

    cam.keysCLick()

    cam.mouseClick()

    cam.get_frame()

    displayGrid(10,screen,cam)

    if ihm.selected_input is None and ihm.selected_cell is None:
        ihm.changeTheta()

    DH_mat=copy.copy(ihm.DH_mat) 
    
    DH_mat[:,-1]+=np.array(ihm.thetas)
    frames=generateDH(DH_mat)

    for i in range(len(frames)-1):
        p1=Point3D(frames[i][:,3])
        p2=Point3D(frames[i+1][:,3])
        displayLine(p1,p2,screen,[255,255,255],1,cam)

    for f in frames:
        displayFrame(f,screen,cam)

    

    ihm.display_theta()

    ihm.display_DH_grid()

    ihm.display_DH_btn()
    # Update the display
    pygame.display.flip()

    running=ihm.main_event_loop()
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        print(np.array(frames))
# Quit Pygame properly
pygame.quit()
sys.exit()

