#to do
'''add planets by clicking'''
'''make revolution more realistic'''
'''add planet info'''


import pygame
import math 
from sys import exit

pygame.init()
screensize = 1280,720
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption('simulation')
clock = pygame.time.Clock()

# variables for revolution of the planet
# x-axis, y-axis, angle(to rotate it)
# h,k centre of screen
x,y,theta = 50,50,0
h,k = screensize[0]/2, screensize[1]/2

# images used
# convert() converts the image to more optimized form for pygame 
# convert() makes bg-less images have bg
# convert_alpha() keeps it bg-less
bg_surf = pygame.image.load('graphics/starbg1.jpg').convert()
star_surf = pygame.image.load('graphics/sun.png').convert_alpha()
star_rect = star_surf.get_rect(center = (h,k))

planets = {}            # all the planets in the folder
revolving = {}          # the planets which are revolving
try:
    n=1
    while True:
        planet_surf = pygame.image.load(f'graphics/planet{n}.png').convert_alpha()
        planet_rect = planet_surf.get_rect(center = (x,y))
        planets[f'pla{n}'] = [planet_surf, planet_rect]
        revolving[f'pla{n}'] = 0
        n += 1
except: None

def revolve(n):   
    # the math:
    #     (h-15) and (k-15) are the cenre of the circle (let it be origin)
    #     x and y decide the radius
    #     theta starts from 0 i.e. at:
    #         0  : cos is max and sin is 0
    #         90 : cos is 0 and sin is max
    #         180: cos is min and sin is 0
    #         270: cos is 0 and sin is min
    #         after 360 : repeat
    #     value at x-axis is determined by cos and value at y-axis is determined by sin 
    global x,y,theta
    plaobj = planets[f'pla{n}']
    screen.blit(plaobj[0],plaobj[1])
    plaobj[1].x = x*math.cos(theta)+(h-15)
    plaobj[1].y = y*math.sin(theta)+(k-15)
    theta += 0.01


running = ' '
while running:
    # to close the window when user clicks on close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        
    # to display the image 
    # blit - block image transfer
    # blit(imagehandle,position)
    screen.blit(bg_surf,(0,0))
    screen.blit(star_surf,star_rect)
    
    # to know if the user has pressed any mouse button and to get the position of the mouse
    mouse_press = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    # mouse_press (left button,middle button,right button)
    if mouse_press == (1,0,0) or mouse_press == (1,1,0) or mouse_press == (1,0,1):
        x,y = mouse_pos
        x,y = x-h,y-k
        revolving[f'pla{3}'] = 1
        
    for i in range(1,n):
        if revolving[f'pla{i}'] == 1:
            revolve(i)
    
    pygame.display.update()

    # fps
    clock.tick(90)

if running == 0:
    pygame.quit()
    exit()