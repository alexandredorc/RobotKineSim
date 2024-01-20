import pygame
import sys
from math import pi
from Camera import Camera
from DH import generateDH
from Elements import *
from IHM import changeTheta
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

font = pygame.font.Font(None, 36)
small = pygame.font.Font(None, 20)
cam=Camera([pi/2,0],[0,0,0],res_mile=2.5,iso=True)

thetas_init=[0,0,0,0,0,0]
DH_mat_init=np.array([[  0   ,  0 ,  0.1695    ,0]
                    ,[ 0        ,pi/2 , 0     ,pi/2]
                    ,[ 0.221325 , 0   , 0       ,0]
                    ,[ 0.035406 ,-pi/2, 0.235    ,0]
                    ,[ 0        , pi/2, 0 ,0]
                    ,[ 0.00925  ,-pi/2 , 0.0416   ,0]])
thetas=[0,0,0,0,0,0]
frames=generateDH(DH_mat_init)
#print(np.array(frames))

display_DH = False
selected_cell = None
selected_input = None
current_input = ""


# Main loop
running = True
while running:
    
    # create the rectangle of the display
    width, height= pygame.display.get_surface().get_size()
    plus_btn=pygame.Rect(width/4, height*3/4 , width / 15, 50)
    DH_btn=pygame.Rect(width*14/15, height/8 , width / 15, 50)

    nb_joints=len(DH_mat_init)
    DH_rects=[[0] * (np.shape(DH_mat_init)[1] + 1) for _ in range(np.shape(DH_mat_init)[0])]
    theta_rects=[0]*len(thetas)

    for i in range(len(thetas)):
        rect = pygame.Rect(width * (i / len(thetas)), height - 50, width / len(thetas), 50)
        theta_rects[i]=rect
    for i in range(nb_joints):
        for j in range(5):
            rect = pygame.Rect(width * ((1/4)+(j/10)) , height*((1/4)+(i / (nb_joints*2))), width / 10, height/ (nb_joints*2))
           
            DH_rects[i][j]=rect
    
    screen.fill((0, 0, 0))

    cam.keysCLick()
    cam.mouseClick()

    cam.get_frame()
    displayGrid(10,screen,cam)
    if selected_input is None and selected_cell is None:
        thetas=changeTheta(thetas)
    DH_mat=copy.copy(DH_mat_init) 
    
    DH_mat[:,-1]+=np.array(thetas)
    frames=generateDH(DH_mat)

    for i in range(len(frames)-1):
        p1=Point3D(frames[i][:,3])
        p2=Point3D(frames[i+1][:,3])
        displayLine(p1,p2,screen,[255,255,255],1,cam)
    for f in frames:
        displayFrame(f,screen,cam) 

    # Render the input boxes
    for i in range(len(thetas)):
        pygame.draw.rect(screen, gray, theta_rects[i])
        if selected_input == i:
            pygame.draw.rect(screen, (0,0,255), theta_rects[i], width=3)
            out=current_input
        else:
            
            out=str(round(thetas[i]%(pi*2),2))
        
        
        text_surface = font.render(out, True, white if i != selected_input else black)
        text_rect = text_surface.get_rect(center=theta_rects[i].center)
        screen.blit(text_surface, text_rect)
    
    if display_DH:
        for i in range(nb_joints):
            for j in range(5):
                pygame.draw.rect(screen, (100,100,100), DH_rects[i][j])
                if selected_cell is not None and selected_cell[0]==i and selected_cell[1]==j:
                    pygame.draw.rect(screen, (0,0,255), DH_rects[i][j], width=3)
                    out=current_input
                else:
                    if j!=4:
                        out=str(round(DH_mat_init[i][j],5))
                    else:
                        out="-"
                text_surface = small.render(out, True, white if (selected_cell is not None and (selected_cell[0]!=i or selected_cell[1]!=j)) else black)
                text_rect = text_surface.get_rect(center=DH_rects[i][j].center)
                screen.blit(text_surface, text_rect)
        
        pygame.draw.rect(screen, gray, plus_btn,border_bottom_left_radius=20,border_bottom_right_radius=20)
        text_surface = font.render("+", True, white)
        text_rect = text_surface.get_rect(center=plus_btn.center)
        screen.blit(text_surface, text_rect)

    pygame.draw.rect(screen, gray, DH_btn,border_top_left_radius=20,border_bottom_left_radius=20)
    text_surface = font.render("DH", True, white)
    text_rect = text_surface.get_rect(center=DH_btn.center)
    screen.blit(text_surface, text_rect)


    # Update the display
    pygame.display.flip()


     
    # event management
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RETURN:
                if selected_input is not None and current_input !="":
                    thetas[selected_input]=float(current_input)
                elif selected_cell is not None and current_input !="":
                    DH_mat_init[selected_cell[0],selected_cell[1]]=float(current_input)
                current_input=""
                print("Angle Inputs:", thetas)
                print("DH Inputs:", DH_mat_init)

            elif event.key == pygame.K_BACKSPACE:
                if current_input != "" and selected_input is not None:
                    current_input = current_input[:-1]
                if current_input != "" and selected_cell is not None:
                    current_input = current_input[:-1]

            elif event.unicode.isdigit() or event.unicode == '.':
                if selected_input is not None:
                    current_input += event.unicode
                if selected_cell is not None:
                    current_input += event.unicode
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            res=True
            if DH_btn.collidepoint(event.pos):
                display_DH = not display_DH
                print(display_DH)
            
            for i in range(len(thetas)):
                if theta_rects[i].collidepoint(event.pos):
                    selected_input = i
                    current_input=str(thetas[i])
                    selected_cell=None
                    res=False
            if display_DH:
                for i in range(nb_joints):
                    for j in range(5):
                        if DH_rects[i][j].collidepoint(event.pos) and j !=4:
                            selected_cell = [i,j]
                            current_input=str(DH_mat_init[i,j])
                            selected_input=None
                            res=False
                        elif DH_rects[i][j].collidepoint(event.pos) and j ==4:
                            DH_mat_init=np.delete(DH_mat_init,i,axis=0)
                            thetas.pop(i)
                            res=False
                if plus_btn.collidepoint(event.pos):
                    DH_mat_init=np.append(DH_mat_init,[[0,0,0,0]],axis=0)
                    thetas.append(0)
                    
            if res:
                selected_input=None
                selected_cell=None
                

# Quit Pygame properly
pygame.quit()
sys.exit()

