import pygame
import sys
import random
import math

version = "0.0.2"
FPS = 30

pygame.init()
DisplayInfo=pygame.display.Info()
ratioDisplayX = 0.75
ratioDisplayY = 0.75
X = int(DisplayInfo.current_w * ratioDisplayX)
Y = int(DisplayInfo.current_h * ratioDisplayY)
DIAGONAL = math.sqrt(X**2 + Y**2)
surface = pygame.display.set_mode((X,Y))
pygame.display.set_caption(f"Shoot Ball v{version} - {X}x{Y}")
clock = pygame.time.Clock()

grey = pygame.Color(50,50,50)
yellow = pygame.Color(200,200,0)
red = pygame.Color(200, 20, 0)

font = pygame.font.Font("FiraCode-Bold.ttf", 18) # 32 fits nicely when screen 1000x1000
msg = "Shoot the ball by clicking on the screen"

circle_exists = False
circle_time_mover = 0
circle_min_speed = 0.5
circle_max_speed = int(DIAGONAL/47) # gets us speed of around ~30 in 1000 by 1000 (1414 diag)
circle_speed = 0
circle_fire_degrees = 0
circle_radius = int(DIAGONAL/28) # gets us ball of size 50 in 1000 by 1000 (1414 diag)
circle_shades = 20
circle_mouse_pos = []

print(f"* Shoot Ball v{version} - Window Size {X}x{Y} - MaxSpeed: {circle_max_speed} - Radius: {circle_radius}")

while True:
    surface.fill(grey)
    if circle_exists:
        circle_time_mover += circle_speed
    # events
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT or (ev.type == pygame.KEYUP and ev.key == pygame.K_q):
            # quit game if press X or hit q key
            pygame.display.quit()
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            x_mouse , y_mouse = ev.pos
            circle_mouse_pos.append((x_mouse , y_mouse)) # note: doesn't have to be list (only 1 item saved with each mousedown and mouseup set)
            # circle_exists = True
            # circle_time_mover = 0
            # mx = random.choice([-1,0,1])
            # my = random.choice([-1,0,1])
            # mx = math.cos(circle_fire_degrees*math.pi/180)
            # my = -math.sin(circle_fire_degrees*math.pi/180)
        if ev.type == pygame.MOUSEBUTTONUP:
            x_mouse , y_mouse = ev.pos
            x0=circle_mouse_pos[0][0]
            y0=circle_mouse_pos[0][1]
            x1=x_mouse
            y1=y_mouse
            dx=(x1-x0)
            dy=(y1-y0)
            # direction
            theta_radians = math.atan2(dy,dx)
            theta_degrees = theta_radians * 180 / math.pi
            adjusted_degress = theta_degrees*-1
            # adjusted_degress = adjusted_degress+180  # uncomment to shoot like pool
            cDx = math.cos(adjusted_degress*math.pi/180)
            cDy = -math.sin(adjusted_degress*math.pi/180)
            # speed
            arrow_length = math.sqrt(dx**2 + dy**2)
            max_speed_arrow_length = DIAGONAL/2
            circle_speed = arrow_length / (max_speed_arrow_length/circle_max_speed)  # dividing by 40 makes it so max speed is 30
            if circle_speed > circle_max_speed: circle_speed=circle_max_speed
            if circle_speed < circle_min_speed: circle_speed=circle_min_speed
            # setting circle
            circle_exists = True
            msg = f"DEBUG: ({x0},{y0}) @ {int(adjusted_degress)}deg | speed={int(circle_speed)}"
            pygame.draw.circle(surface, pygame.Color(0,0,255), (x0, y0), 5, 0) # red start
            pygame.draw.circle(surface, pygame.Color(255,0,0), (x1, y1), 5, 0) # green end
            circle_mouse_pos = [] # reset mouse events
            circle_time_mover = 0 # reset mover


    # drawings
    if circle_exists:
        circle_shades_prime = circle_shades + 1
        for i in range(circle_shades_prime):
            ratioR = (circle_shades_prime - i) / circle_shades_prime # moves from 1 to 0 smoothly (aka Ratio Reverse)
            ratio = 1-ratioR                                         # moves from 0 to 1 smoothly
            cRed = 200
            cGreenVar = 200
            cGreen = int(cGreenVar*ratio) + (255-cGreenVar)
            cBlue = 0
            cColor = pygame.Color(cRed,cGreen, cBlue)
            cX = x0+cDx*circle_time_mover
            cY = y0+cDy*circle_time_mover
            cR = circle_radius*ratio # moves from radius 0 to 1*circle_radius (small to big)
            cW = int(circle_radius/circle_shades_prime)+1
            pygame.draw.circle(surface, cColor, (cX, cY), cR, cW)
            
    # msg - make into class
    msg_surface = font.render(msg, True, red)
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = (X/15,Y/10) # (90,100) works good for 1000x1000
    surface.blit(msg_surface,msg_rect)
    # screen update
    pygame.display.update()
    clock.tick(FPS)

# EOF