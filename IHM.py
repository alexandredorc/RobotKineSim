import pygame
import numpy as np

black=(0,0,0)
gray = (200, 200, 200)
white=(255,255,255)



class IHM:
    def __init__(self,thetas,DH_mat,screen):
        self.display_DH = False
        self.thetas=thetas
        self.DH_mat=DH_mat
        self.selected_input = None
        self.selected_cell = None
        self.current_input = ""
        self.setup_btns()
        self.screen=screen

        self.font = pygame.font.Font(None, 36)
        self.small = pygame.font.Font(None, 20)
        
    def setup_btns(self):
        # create the rectangle of the display
        self.width, self.height= pygame.display.get_surface().get_size()
        self.plus_btn=pygame.Rect(self.width/4, self.height*3/4 , self.width / 15, 50)
        self.DH_btn=pygame.Rect(self.width*14/15, self.height/8 , self.width / 15, 50)

        self.nb_joints=len(self.DH_mat)
        self.DH_rects=[[0] * (np.shape(self.DH_mat)[1] + 1) for _ in range(np.shape(self.DH_mat)[0])]
        self.theta_rects=[0]*len(self.thetas)
        for i in range(len(self.thetas)):
            rect = pygame.Rect(self.width * (i / len(self.thetas)), 
                               self.height - 50, 
                               self.width / len(self.thetas), 
                               50)
            self.theta_rects[i]=rect

        for i in range(self.nb_joints):
            for j in range(5):
                rect = pygame.Rect(self.width * ((1/4)+(j/10)) , 
                                   self.height*((1/4)+(i / (self.nb_joints*2))), 
                                   self.width / 10, 
                                   self.height/ (self.nb_joints*2))
            
                self.DH_rects[i][j]=rect

    def key_down(self,event):
        
        if event.key == pygame.K_RETURN:
            if self.selected_input is not None and self.current_input !="":
                self.thetas[self.selected_input]=float(self.current_input)
            elif self.selected_cell is not None and self.current_input !="":
                self.DH_mat[self.selected_cell[0],self.selected_cell[1]]=float(self.current_input)
            self.current_input=""
            print("Angle Inputs:", self.thetas)
            print("DH Inputs:", self.DH_mat)

        elif event.key == pygame.K_BACKSPACE:
            if self.current_input != "" and self.selected_input is not None:
                self.current_input = self.current_input[:-1]
            if self.current_input != "" and self.selected_cell is not None:
                self.current_input = self.current_input[:-1]

        elif event.unicode.isdigit() or event.unicode == '.':
            if self.selected_input is not None:
                self.current_input += event.unicode
            if self.selected_cell is not None:
                self.current_input += event.unicode

    def mouse_click(self,event):
        res=True
        if self.DH_btn.collidepoint(event.pos):
            self.display_DH = not self.display_DH
        
        for i in range(len(self.thetas)):
            if self.theta_rects[i].collidepoint(event.pos):
                self.selected_input = i
                self.current_input=str(self.thetas[i])
                self.selected_cell=None
                res=False
        if self.display_DH:
            for i in range(self.nb_joints):
                for j in range(5):
                    if self.DH_rects[i][j].collidepoint(event.pos) and j !=4:
                        self.selected_cell = [i,j]
                        self.current_input=str(self.DH_mat[i,j])
                        self.selected_input=None
                        res=False
                    elif self.DH_rects[i][j].collidepoint(event.pos) and j ==4:
                        self.DH_mat=np.delete(self.DH_mat,i,axis=0)
                        self.thetas.pop(i)
                        res=False
            if self.plus_btn.collidepoint(event.pos):
                self.DH_mat=np.append(self.DH_mat,[[0,0,0,0]],axis=0)
                self.thetas.append(0)
                
        if res:
            self.selected_input=None
            self.selected_cell=None

    def main_event_loop(self):
        # event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.key_down(event)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_click(event)
        return True

    def display_theta(self):
        
        for i in range(len(self.thetas)):
            pygame.draw.rect(self.screen, gray, self.theta_rects[i])
            if self.selected_input == i:
                pygame.draw.rect(self.screen, (0,0,255), self.theta_rects[i], width=3)
                out=self.current_input
            else:
                
                out=str(round(self.thetas[i]%(np.pi*2),2))
            
            
            text_surface = self.font.render(out, True, white if i != self.selected_input else black)
            text_rect = text_surface.get_rect(center=self.theta_rects[i].center)
            self.screen.blit(text_surface, text_rect)

    def display_DH_btn(self):
        pygame.draw.rect(self.screen, gray, self.DH_btn,border_top_left_radius=20,border_bottom_left_radius=20)
        text_surface = self.font.render("DH", True, white)
        text_rect = text_surface.get_rect(center=self.DH_btn.center)
        self.screen.blit(text_surface, text_rect)

    def display_DH_grid(self):
        if self.display_DH:
            for i in range(self.nb_joints):
                for j in range(5):
                    pygame.draw.rect(self.screen, (100,100,100), self.DH_rects[i][j])
                    if self.selected_cell is not None and self.selected_cell[0]==i and self.selected_cell[1]==j:
                        pygame.draw.rect(self.screen, (0,0,255), self.DH_rects[i][j], width=3)
                        out=self.current_input
                    else:
                        if j!=4:
                            out=str(round(self.DH_mat[i][j],5))
                        else:
                            out="-"
                    text_surface = self.small.render(out, True, white if (self.selected_cell is not None and (self.selected_cell[0]!=i or self.selected_cell[1]!=j)) else black)
                    text_rect = text_surface.get_rect(center=self.DH_rects[i][j].center)
                    self.screen.blit(text_surface, text_rect)
            
            pygame.draw.rect(self.screen, gray, self.plus_btn,border_bottom_left_radius=20,border_bottom_right_radius=20)
            text_surface = self.font.render("+", True, white)
            text_rect = text_surface.get_rect(center=self.plus_btn.center)
            self.screen.blit(text_surface, text_rect)

    
    def changeTheta(self):
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            step=-0.01
        else:
            step=0.01
        if pygame.key.get_pressed()[pygame.K_0]:
            self.thetas[0]+=step
        if pygame.key.get_pressed()[pygame.K_1]:
            self.thetas[1]+=step
        if pygame.key.get_pressed()[pygame.K_2]:
            self.thetas[2]+=step
        if pygame.key.get_pressed()[pygame.K_3]:
            self.thetas[3]+=step
        if pygame.key.get_pressed()[pygame.K_4]:
            self.thetas[4]+=step
        if pygame.key.get_pressed()[pygame.K_5]:
            self.thetas[5]+=step
        
 

