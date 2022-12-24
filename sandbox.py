#to do
'''add trails BEHIND the planets'''
'''zoom out'''
'''add planet info'''
'''music'''


import pygame
import math 
from sys import exit

pygame.init()
SCREENSIZE = 1920,1020
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('simulation')
clock = pygame.time.Clock()

MOUSE_B1 = [(1,0,0),(1,1,0),(1,0,1),(1,1,1)]
MOUSE_B2 = [(0,1,0),(1,1,0),(0,1,1),(1,1,1)]
MOUSE_B3 = [(0,0,1),(0,1,1),(1,0,1),(1,1,1)]

# planet trail colours
MERCURY = (149, 149, 149, 1)
VENUS = (159, 85, 19, 1)
EARTH = (80, 111, 144, 1)
MARS = (232, 144, 83, 1)
JUPITER = (246, 202, 140, 1)
SATURN = (124, 121, 106, 1)
URANUS = (207, 225, 235, 1)
NEPTUNE = (72, 114, 254, 1)

size_x,size_y = 10,10
# x-axis, y-axis, angle 
x,y,theta = 50,50,0
# h,k centre of screen
h,k = SCREENSIZE[0]/2, SCREENSIZE[1]/2

# images used
# convert() converts the image to more optimized form for pygame 
# convert() makes bg-less images have bg
# convert_alpha() keeps it bg-less
bg_surf = pygame.image.load('graphics/starbgo.jpg').convert()
bg_surf = pygame.transform.scale(bg_surf,SCREENSIZE)
star_surf = pygame.image.load('graphics/sun.png').convert_alpha()
star_rect = star_surf.get_rect(center = (h,k))

pause_surf = pygame.image.load('graphics/pause.png').convert_alpha()
pause_rect = pause_surf.get_rect(center = (2*h-100,100))
pause_rect1 = star_surf.get_rect(center = (2*h-150,100))

planets = {}            # all the planets in the folder
revolving = {}          # the planets which are revolving
pla_no = 0              # no. of planets revolving

try:
    n=1
    while True:
        planet_surf = pygame.image.load(f'graphics/planet{n}.png').convert_alpha()
        planet_rect = planet_surf.get_rect(center = (x,y))
        planets[f'planet{n}'] = [planet_surf, planet_rect]
        revolving[f'planet{n}'] = 0
        n += 1          # at the end, (n-1) is the number of planets in the folder
except: None        

# planet's approx data for revolution
# planet_number : [x,y,theta,increment_in_theta,colour_of_the_trail]
# x and y are the distances from the sun
# increment in theta is the rate at which it revolve
planet_data = {}
planet_data[1] = [110,100,0,0.04,MERCURY]
planet_data[2] = [160,150,0,0.016,VENUS]
planet_data[3] = [200,190,0,0.01,EARTH]
planet_data[4] = [270,260,0,0.0056,MARS]
planet_data[5] = [800,780,0,0.00083,JUPITER]
planet_data[6] = [1460,1440,0,0.00037,SATURN]
planet_data[7] = [2800,2760,0,0.00011,URANUS]
planet_data[8] = [3640,3600,0,0.00006,NEPTUNE]

def revolve(n): 
    x,y,theta,inc,color = planet_data[n] 
    planet_obj = planets[f'planet{n}']
    # the math:
        # (h-10) and (k-10) are the cenre of the circle (let it be origin), -10 for the deviation caused by the size of the image
        # x and y decide the radius
        # value at x-axis is determined by cos and value at y-axis is determined by sin 
        # theta -= <rate> determines the speed of the revoltion (minus sign because planets revolve anticlockwise)
        # theta starts from 0 i.e. at:
            #  0  : cos is max and sin is 0
            # -90 : cos is 0 and sin is min
            # -180: cos is min and sin is 0
            # -270: cos is 0 and sin is max
            # after -360 : repeat
    planet_obj[1].x = x*math.cos(theta)+(h)
    planet_obj[1].y = y*math.sin(theta)+(k)
    theta -= inc
    
    planet_data[n][2] = theta    #change the value of theta in planet_data dictinary (otherwise the planet will just stay in one position)
    trail(n,planet_obj,color)

    screen.blit(planet_obj[0],planet_obj[1])

trail_d = {}
def trail(n,planet_obj,color):
    try:
        trail_d[n].append((planet_obj[1].x,planet_obj[1].y))
    except:
        trail_d[n] = []

    try:
        pygame.draw.aalines(screen,color,False,trail_d[n])
    except: 
        None

    if len(trail_d[n]) > planet_data[n][0]:
        trail_d[n].pop(0)

running = 1
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
    mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    while pla_no < n:
        ##x,y = planet_data[pla_no]
        revolving[f'planet{pla_no}'] = 1
        pla_no += 1
        
    for i in range(1,n):
        if revolving[f'planet{i}'] >= 1:
            revolve(i)
    
    pygame.display.update()

    clock.tick(60)
    
    if keys[pygame.K_q]: 
        for i in range(1,n):
            x_distance = planet_data[i][0]
            
            planet_data[i][0] -= (1*x_distance)/100
            planet_data[i][1] = x_distance-10
            # try:
            #     planet_surf = pygame.transform.scale(planet_surf,(size_x,size_y))
            # except: None
            if i < 5:
                planets[f'planet{i}'][0] = pygame.transform.scale(planets[f'planet{i}'][0],(size_x,size_y))
            if size_x > 0 :
                size_x -= 0.01
                size_y -= 0.01
    if keys[pygame.K_e]: 
        for i in range(1,n):
            x_distance = planet_data[i][0]
            
            planet_data[i][0] += (1*x_distance)/100
            planet_data[i][1] = x_distance+10
            # try:
            #     planet_surf = pygame.transform.scale(planet_surf,(size_x,size_y))
            # except: None
            if i < 5:
                planets[f'planet{i}'][0] = pygame.transform.scale(planets[f'planet{i}'][0],(size_x,size_y))
            if size_x <11 :
                size_x += 0.01
                size_y += 0.01

if running == 0:
    pygame.quit()
    exit()