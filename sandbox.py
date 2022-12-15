#to do
'''add planets by clicking'''
'''make revolution more realistic'''
'''add planet info'''


import pygame
import math 
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1620,960))
pygame.display.set_caption('simulation')
clock = pygame.time.Clock()

# variables for revolution of the planet
# x-axis, y-axis, angle(to rotate it)
x=200
y=200
theta=0

# images used
# convert() converts the image to more optimized form for pygame 
# convert() makes bg-less images have bg
# convert_alpha() keeps it bg-less
bg_surf = pygame.image.load('graphics/starbg1.jpg').convert()
star_surf = pygame.image.load('graphics/sun.png').convert_alpha()
planet_surf = pygame.image.load('graphics/planet3.png').convert_alpha()

planet_rect = planet_surf.get_rect(topleft = (x,y))

while True:
    
    # to close the window when user clicks on close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    # display the image 
    # blit (block image transfer)
    # blit(imagehandle,position)
    screen.blit(bg_surf,(0,0))
    screen.blit(star_surf,(760,440))
    
    # the math:
    #     +800 and +490 are the cenre of the circle (let it be origin)
    #     theta starts from 0 i.e. at:
    #         0  : cos is max and sin is 0
    #         90 : cos is 0 and sin is max
    #         180: cos is min and sin is 0
    #         270: cos is 0 and sin is min
    #         after 360 : repeat
    #     value at x-axis is determined by cos and value at y-axis is determined by sin
    screen.blit(planet_surf,planet_rect)
    planet_rect.x = x*math.cos(theta)+800
    planet_rect.y = y*math.sin(theta)+490
    theta += 0.01

    pygame.display.update()

    mouse_press = pygame.mouse.get_pressed()
    # to slow down time by getting less fps when mouse1 is clicked
    if mouse_press == (1,0,0): 
            clock.tick(24)
    else: clock.tick(90)
