import pygame
import numpy as np

def changeTheta(thetas):
    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
        step=-0.01
    else:
        step=0.01
    if pygame.key.get_pressed()[pygame.K_0]:
        thetas[0]+=step
    if pygame.key.get_pressed()[pygame.K_1]:
        thetas[1]+=step
    if pygame.key.get_pressed()[pygame.K_2]:
        thetas[2]+=step
    if pygame.key.get_pressed()[pygame.K_3]:
        thetas[3]+=step
    if pygame.key.get_pressed()[pygame.K_4]:
        thetas[4]+=step
    if pygame.key.get_pressed()[pygame.K_5]:
        thetas[5]+=step
    
    return thetas
    

class IHM:
    def __init__(self):
        pass
   