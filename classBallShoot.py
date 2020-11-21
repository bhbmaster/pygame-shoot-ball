import pygame
import sys
import random
import math

version = "0.0.1c"
FPS = 60
Grey = pygame.Color(50,50,50)
Yellow = pygame.Color(200,200,0)
Red = pygame.Color(200, 20, 0)

class Message:
    
    def __init__(self,message,X,Y,color,size=18,font="FiraCode-Bold.ttf"):
        self.font = pygame.font.Font("FiraCode-Bold.ttf", 18) # 32 fits nicely when screen 1000x1000
        self.message = message
        self.color = color
        self.X = X
        self.Y = Y

    def draw(self,surface):
        msg_surface = self.font.render(self.message, True, self.color)
        msg_rect = msg_surface.get_rect()
        msg_rect.topleft = (self.X,self.Y)
        surface.blit(msg_surface,msg_rect)

class Ball:
    pass

class Main:

    def __init__(self, scale = 0.75):
        
        pygame.init()

        self.DisplayInfo=pygame.display.Info()
        self.ratioDisplayX = scale
        self.ratioDisplayY = scale
        self.X = int(self.DisplayInfo.current_w * self.ratioDisplayX)
        self.Y = int(self.DisplayInfo.current_h * self.ratioDisplayY)
        self.DIAGONAL = math.sqrt(self.X**2 + self.Y**2)
        self.surface = pygame.display.set_mode((self.X,self.Y))
        pygame.display.set_caption(f"Shoot Ball v{version} - {self.X}x{self.Y}")
        self.clock = pygame.time.Clock()

    def gameLoop(self):
        while True:
            self.surface.fill(Grey)  # draw background here in case we want to draw debug info in events (before calling draw)
            events = pygame.event.get()
            # events
            for ev in events:
                if ev.type == pygame.QUIT or (ev.type == pygame.KEYUP and ev.key == pygame.K_q):
                    # quit game if press X or hit q key
                    pygame.display.quit()
                    sys.exit()
            # init message
            msg = Message("Shoot the ball by clicking on the screen",self.X/15,self.Y/10,Red)
            # draw
            msg.draw(self.surface)
            pygame.display.update()
            self.clock.tick(FPS)


## main ##

Scale = 0.9
m = Main(Scale)
m.gameLoop()

# EOF