import pygame
import sys
import random
import math

version = "0.0.5c"
FPS = 60
SHADES_PER_CIRCLE = 20
MAX_SECOND_HOLD = 1000            # how many milliseconds hold generate max gold
Scale = 0.75                      # percent size of full screen . 1 = full screen
Red = pygame.Color(200, 20, 0)    # text color
Grey = pygame.Color(50,50,50)     # background color
# Yellow = pygame.Color(200,200,0)

class Message:
    
    def __init__(self,message,X,Y,color,size=18,font="FiraCode-Bold.ttf"):

        # init message size string and location
        self.font = pygame.font.Font("FiraCode-Bold.ttf", 18) # 32 fits nicely when screen 1000x1000
        self.message = message
        self.color = color
        self.X = X
        self.Y = Y

    def draw(self,surface):

        # draw message on surface/screen
        msg_surface = self.font.render(self.message, True, self.color)
        msg_rect = msg_surface.get_rect()
        msg_rect.topleft = (self.X,self.Y)
        surface.blit(msg_surface,msg_rect)

class Ball:

    def __init__(self,x0,y0,dir_degrees,speed,radius):

        # init
        self.cX = x0
        self.cY = y0
        self.dir_degrees = dir_degrees
        self.radius = radius
        self.speed = speed

        # change in x and y (normalized):
        self.cDx = math.cos(self.dir_degrees*math.pi/180)
        self.cDy = -math.sin(self.dir_degrees*math.pi/180)
        self.circle_shades = SHADES_PER_CIRCLE

        # color init
        self.choice = random.randint(1,6)  # we 6 color set choices (in draw function we take care of this)
        self.cVar = random.randint(100,200) # additionally we vary randomly the shade variance

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
        self.cY += self.cDy*self.speed # (new - add change_in_y_normalized_ratio * circle_speed)

    def draw(self,surface):

        # draw circles shades which draws the circle
        circle_shades_prime = self.circle_shades + 1

        # shades of the circle which make the circle
        for i in range(circle_shades_prime):

            ratioR = (circle_shades_prime - i) / circle_shades_prime # moves from 1 to 0 smoothly (aka Ratio Reverse)
            ratio = 1-ratioR                                         # moves from 0 to 1 smoothly

            # pick R,G,B for shades depending on the color choice we picked when ball was initiated
            if self.choice == 1: cRed = 200; cGreen = int(self.cVar*ratio) + (255-self.cVar); cBlue = 0
            elif self.choice == 2: cRed = 0; cGreen =  200; cBlue = int(self.cVar*ratio) + (255-self.cVar)
            elif self.choice == 3: cRed = int(self.cVar*ratio) + (255-self.cVar); cGreen = 100; cBlue =  100
            elif self.choice == 4: cRed = int(self.cVar*ratio) + (255-self.cVar); cGreen = int(self.cVar*ratio) + (255-self.cVar);  cBlue =  200
            elif self.choice == 5: cRed = 0; cGreen = int(self.cVar*ratio) + (255-self.cVar);  cBlue =  int(self.cVar*ratio) + (255-self.cVar)
            elif self.choice == 6: cRed = int(self.cVar*ratio) + (255-self.cVar); cGreen = int(self.cVar*ratio) + (255-self.cVar); cBlue = int(self.cVar*ratio) + (255-self.cVar)

            cColor = pygame.Color(cRed,cGreen, cBlue)

            cR = self.radius*ratio # moves from radius 0 to 1*circle_radius (small to big)
            cW = int(self.radius/circle_shades_prime)+1

            # draw the shade arc/circle
            pygame.draw.circle(surface, cColor, (self.cX, self.cY), cR, cW)

class Main:

    def __init__(self, scale = 0.75):

        # init pygame and set size and caption and clock (for fps management)        
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

        # mouse click constants - left mouse button is 1, right mouse button is 3
        LEFT = 1
        RIGHT = 3

        # preloop inits
        circle_mouse_pos = []
        balls = []

        # circle mins and maxes for speed
        circle_min_speed = 0.5
        circle_max_speed = int(self.DIAGONAL/45) # gets us speed of around ~30 in 1000 by 1000 (1414 diag)

        # circle mins and maxes for radius
        circle_min_radius = 1
        circle_max_radius = int(self.DIAGONAL/15)
        circle_delta_radius = circle_max_radius - circle_min_radius
        max_second_hold = MAX_SECOND_HOLD # 3000 ms | 3s for max radius ball (less hold smaller ball)
        
        # print to console (we flush it otherwise it only shows up when the game closes)
        main_title_string=f"* Shoot Ball v{version} - Window Size {self.X}x{self.Y} - vMin {circle_min_speed}, vMax {circle_max_speed} - rMin {circle_min_radius}, rMax {circle_max_radius}"
        # print(main_title_string); sys.stdout.flush()

        # main game loop where we draw background, get events, draw message, update balls, draw balls, update screen
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
                    time = pygame.time.get_ticks()
            
                if ev.type == pygame.MOUSEBUTTONUP:

                    # reset balls if right click
                    if ev.button == RIGHT:
                        balls = []
                        continue

                    # get mouse start and end position & delta
                    x_mouse , y_mouse = ev.pos
                    mX0=circle_mouse_pos[0][0]
                    mY0=circle_mouse_pos[0][1]
                    mX1=x_mouse
                    mY1=y_mouse
                    mDx=(mX1-mX0)
                    mDy=(mY1-mY0)

                    # mouse direction = ball direction
                    theta_radians = math.atan2(mDy,mDx)
                    theta_degrees = theta_radians * 180 / math.pi
                    adjusted_degreses = theta_degrees * -1
                    # adjusted_degress = adjusted_degress+180  # uncomment to shoot like pool
                    
                    # set speed of ball
                    arrow_length = math.sqrt(mDx**2 + mDy**2)
                    max_speed_arrow_length = self.DIAGONAL/2
                    circle_speed = arrow_length / (max_speed_arrow_length/circle_max_speed)  
                    if circle_speed > circle_max_speed: circle_speed=circle_max_speed
                    if circle_speed < circle_min_speed: circle_speed=circle_min_speed

                    # set radius of ball (set by time it takes to draw arrow - more time bigger ball)
                    delta_time = pygame.time.get_ticks() - time
                    if delta_time > max_second_hold: delta_time = max_second_hold
                    circle_radius = circle_min_radius + int(circle_delta_radius*delta_time/max_second_hold)
                    # print(f"{delta_time=} {circle_radius=}"); sys.stdout.flush()
                    
                    # setting circle
                    circle_mouse_pos = []
                    balls.append(Ball(mX0,mY0,adjusted_degreses,circle_speed,circle_radius))
                    # HERE
            
            # init message + title bar
            msg = Message(f"Shoot balls by click dragging on the screen. Longer strokes = more speed. Quicker strokes = smaller ball.",self.X/15,self.Y/10,Red)
            # extra_title_string = f" -  FPS: {int(self.clock.get_fps())} - BALLS: {len(balls)} - CIRCLE_DRAWS: {SHADES_PER_CIRCLE*len(balls)}"
            extra_title_string = f" - {int(self.clock.get_fps())} fps - {len(balls)} balls"
            pygame.display.set_caption(main_title_string+extra_title_string)
            
            # draw
            msg.draw(self.surface)
            for ball in balls:
                ball.update()
                ball.draw(self.surface)
     
            # update screen and make sure we sleep correct amount of time to achieve good FPS (hence tick)
            pygame.display.update()
            self.clock.tick(FPS)


## main ##
m = Main(Scale)
m.gameLoop()

# EOF