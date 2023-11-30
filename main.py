import pygame
import sys
from math import pi
from Camera import Camera
from Point3D import Point3D,displayLine


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

    for i in range(-size,size+1):
        p11=Point3D([size,i,0])
        p12=Point3D([-size,i,0])
        p21=Point3D([i,size,0])
        p22=Point3D([i,-size,0])
        displayLine(p11,p12,screen,[100,100,100],1,cam)
        displayLine(p21,p22,screen,[100,100,100],1,cam)

pc=Point3D([0,0,0])
px=Point3D([1,0,0])
py=Point3D([0,1,0])
pz=Point3D([0,0,1])

add=0.001
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black color
    screen.fill((0, 0, 0))
    
    cam.mouseClick()
    cam.get_frame()
    displayGrid(5,screen,cam)
    displayLine(pc,px,screen,red,2,cam)
    displayLine(pc,py,screen,green,2,cam)
    displayLine(pc,pz,screen,blue,2,cam)
   
    # Update the display
    pygame.display.flip()

# Quit Pygame properly
pygame.quit()
sys.exit()

