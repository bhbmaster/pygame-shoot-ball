import pygame
import sys
import random
import math

version = "0.0.3c"
FPS = 60
Scale = 0.75
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

    def __init__(self,x0,y0,dir_degrees,speed,radius):
        self.cX = x0
        self.cY = y0
        self.dir_degrees = dir_degrees
        self.radius = radius
        self.speed = speed
        # change in x and y (normalized):
        self.cDx = math.cos(self.dir_degrees*math.pi/180)
        self.cDy = -math.sin(self.dir_degrees*math.pi/180)
        self.circle_shades = 20

    def update(self):  # update aka move

        # window borders:
        window_width,window_height = pygame.display.get_window_size()

        if (self.cY + self.radius > window_height) or (self.cY - self.radius < 0):
            self.cDy = -self.cDy
        if (self.cX + self.radius > window_width) or (self.cX - self.radius < 0):
            self.cDx = -self.cDx
        # debug info 2 here
        # next circle position updated with change in X and change Y
        self.cX += self.cDx*self.speed # (new - add change_in_x_normalized_ratio * circle_speed)
        self.cY += self.cDy*self.speed # (new - add 

    def draw(self,surface):

        # draw circles shades which draws the circle
        circle_shades_prime = self.circle_shades + 1
        for i in range(circle_shades_prime):
            ratioR = (circle_shades_prime - i) / circle_shades_prime # moves from 1 to 0 smoothly (aka Ratio Reverse)
            ratio = 1-ratioR                                         # moves from 0 to 1 smoothly
            cRed = 200
            cGreenVar = 200
            cGreen = int(cGreenVar*ratio) + (255-cGreenVar)
            cBlue = 0
            cColor = pygame.Color(cRed,cGreen, cBlue)
            cR = self.radius*ratio # moves from radius 0 to 1*circle_radius (small to big)
            cW = int(self.radius/circle_shades_prime)+1
            pygame.draw.circle(surface, cColor, (self.cX, self.cY), cR, cW)

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

        # preloop inits
        circle_mouse_pos = []
        balls = []
        # for now put here:
        circle_min_speed = 0.5
        circle_max_speed = int(self.DIAGONAL/45) # gets us speed of around ~30 in 1000 by 1000 (1414 diag)
        circle_radius = int(self.DIAGONAL/28) # gets us ball of size 50 in 1000 by 1000 (1414 diag)
        
        # print to console
        print(f"* Shoot Ball v{version} - Window Size {self.X}x{self.Y} - MaxSpeed: {circle_max_speed} - Radius: {circle_radius}")

        # loop
        while True:
            self.surface.fill(Grey)  # draw background here in case we want to draw debug info in events (before calling draw)
            events = pygame.event.get()
            # events
            for ev in events:
                if ev.type == pygame.QUIT or (ev.type == pygame.KEYUP and ev.key == pygame.K_q):
                    # quit game if press X or hit q key
                    pygame.display.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    x_mouse, y_mouse = ev.pos
                    circle_mouse_pos.append((x_mouse, y_mouse))
                if ev.type == pygame.MOUSEBUTTONUP:
                    # get mouse start and end position & delta
                    x_mouse , y_mouse = ev.pos
                    mX0=circle_mouse_pos[0][0]
                    mY0=circle_mouse_pos[0][1]
                    mX1=x_mouse
                    mY1=y_mouse
                    mDx=(mX1-mX0)
                    mDy=(mY1-mY0)
                    # direction
                    theta_radians = math.atan2(mDy,mDx)
                    theta_degrees = theta_radians * 180 / math.pi
                    adjusted_degreses = theta_degrees * -1
                    # adjusted_degress = adjusted_degress+180  # uncomment to shoot like pool
                    # speed
                    arrow_length = math.sqrt(mDx**2 + mDy**2)
                    max_speed_arrow_length = self.DIAGONAL/2
                    circle_speed = arrow_length / (max_speed_arrow_length/circle_max_speed)  
                    # dividing by 40 makes it so max speed is 30
                    if circle_speed > circle_max_speed: circle_speed=circle_max_speed
                    if circle_speed < circle_min_speed: circle_speed=circle_min_speed
                    # setting circle
                    circle_mouse_pos = []
                    balls.append(Ball(mX0,mY0,adjusted_degreses,circle_speed,circle_radius))
                    # HERE
            # init message
            msg = Message("Shoot balls by clicking on screen",self.X/15,self.Y/10,Red)
            # draw
            msg.draw(self.surface)
            for ball in balls:
                ball.update()
                ball.draw(self.surface)
            pygame.display.update()
            self.clock.tick(FPS)


## main ##

m = Main(Scale)
m.gameLoop()

# EOF