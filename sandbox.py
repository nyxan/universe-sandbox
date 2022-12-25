# controls:
#  to show the information about the planet - click on that planet
#  to zoom out - q
#  to zoom in - e

import pygame
import math 
from sys import exit

#opening the information file
f = open('planetryinfo.txt','r')

#initializing pygame
pygame.init()

# size of window
SCREENSIZE = 1920,1020
screen = pygame.display.set_mode(SCREENSIZE)

# Name displayed on window
pygame.display.set_caption('simulation')

clock = pygame.time.Clock()

# font used for displaying text
font = pygame.font.Font('Font/Pixeltype.ttf', 25)

# background music used and its volume
music = pygame.mixer.Sound('Music/bg music.mp3')
music.set_volume(1)
music.play(loops = -1)          # looping it forever

# mouse button press (left,middle,right)
MOUSE_B1 = [(1,0,0),(1,1,0),(1,0,1),(1,1,1)]
MOUSE_B2 = [(0,1,0),(1,1,0),(0,1,1),(1,1,1)]
MOUSE_B3 = [(0,0,1),(0,1,1),(1,0,1),(1,1,1)]

# planet's trail colours
MERCURY = (149, 149, 149, 1)
VENUS = (159, 85, 19, 1)
EARTH = (80, 111, 144, 1)
MARS = (232, 144, 83, 1)
JUPITER = (246, 202, 140, 1)
SATURN = (124, 121, 106, 1)
URANUS = (207, 225, 235, 1)
NEPTUNE = (72, 114, 254, 1)

#planet sizes (for display)
size_x,size_y = 10,10
# x-axis, y-axis, angle 
x,y,theta = 50,50,0
# h,k centre of screen
h,k = SCREENSIZE[0]/2, SCREENSIZE[1]/2
# height and width of screen
WIDTH = SCREENSIZE[0]
HEIGHT = SCREENSIZE[1]

# images used
# convert() converts the image to more optimized form for pygame 
# convert() makes bg-less images have bg
# convert_alpha() keeps it bg-less
bg_surf = pygame.image.load('graphics/starbgo.jpg').convert()           # background
bg_surf = pygame.transform.scale(bg_surf,SCREENSIZE)

star_surf = pygame.image.load('graphics/planet0.png').convert_alpha()   # sun
star_rect = star_surf.get_rect(center = (h,k))

close_surf = pygame.image.load('graphics/close-button.png').convert_alpha()   # close button
close_rect = close_surf.get_rect(center = (WIDTH-50,30))


# dictionary containing  surface and rectangles of all the planets in the folder
planets = {}             # small images used for showing in the simulation
planetos = {}            # big images used for showing in the info window

revolving = {}          # the planets which are revolving
pla_no = 0              # no. of planets revolving

# get all the planets in the folder
try:
    n=1
    while True:
        planet_surf = pygame.image.load(f'graphics/planet{n}.png').convert_alpha()         
        planet_rect = planet_surf.get_rect(center = (x,y))
        planets[f'planet{n}'] = [planet_surf, planet_rect]

        planeto_surf = pygame.image.load(f'graphics/planeto{n}.png').convert_alpha()        
        planeto_rect = planeto_surf.get_rect(center = (WIDTH - 175, 230))
        planetos[f'planeto{n}'] = [planeto_surf, planeto_rect]

        revolving[f'planet{n}'] = 0
        n += 1          # at the end, (n-1) is the number of planets in the folder
# if it shows error, i.e. there are no files in the folder anymore, continue
except: None        


# get all the data from file and make a list with each element being another line
alldata = f.read().splitlines()

# get all the parameters with their units from the file in a predefined order - 
# Planet,Mass,Diameter,Density,Gravity,Escape Velocity,Rotation Period,Day Length,Distance from Sun,Orbital Period,Orbital Velocity,Mean Temperature, Surface Pressure, Number of Moons
parameters = alldata[0].split(',')
units =  alldata[1].split(',')

#get all the planet data in a dictionary
planet_info = {}
for i in range(1,n):
    planet_info[i] = alldata[i+1].split(',') 

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

#to make the planets revolve around the sun
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
    
    planet_data[n][2] = theta    # change the value of theta in planet_data dictinary (otherwise the planet will just stay in one position)
    trail(n,planet_obj,color)    # make trails behind them   

    #display the planets
    screen.blit(planet_obj[0],planet_obj[1])

# dictionary containing the position of trails of the orbits of the planets
trail_d = {}
def trail(n,planet_obj,color):
    # so trails aren't made when zooming in or out
    if keys[pygame.K_q] == True or keys[pygame.K_e] == True:
        trail_d[n].clear()
    
    # getting the position of planet
    planet_pos = (planet_obj[1].x,planet_obj[1].y)

    #checking if point is integer to not have to many points in the list
    if str(planet_obj[1].x).isdigit():
        try:
            if planet_pos not in trail_d[n]:
                # getting the points where the planet passed so a trail can be made on that point in a list
                trail_d[n].append(planet_pos)
        except:
            # if the dictionary doesn't contain the planet
            # make key with planet's number that contains empty list
            trail_d[n] = []
        
        try:
            # make the trail
            # draw.lines make lines from the points given the list
            pygame.draw.lines(screen,color,False,trail_d[n])
        except: 
            None
    
    # erase too long trails
    # trail_d[n] is the list containing the positions from where the planet passed
    # planet_data[n][0] relative distance to the planet
    if len(trail_d[n]) > 2*planet_data[n][0]:
        trail_d[n].pop(0)

# for zooming out and displaying outer planets
def zoom_out(size_x, size_y):
    for i in range(1,n):
        # the distance of planet from x = 0
        x_distance = planet_data[i][0]
        
        # changing the position of planets
        # /100 so planets closer to the sun zoom out slower and vice versa
        # y is always 10 less than x
        planet_data[i][0] -= (1*x_distance)/100         # x
        planet_data[i][1] = x_distance-10               # y

        # so size doesn't become negative
        if size_x > 9 :
            size_x -= 0.01
            size_y -= 0.01
            if i < 5:
                # change the size of the inner planets
                planets[f'planet{i}'][0] = pygame.transform.scale(planets[f'planet{i}'][0],(size_x,size_y))

    return size_x,size_y

# for zooming in into inner planets
def zoom_in(size_x, size_y):
    global planet_rect
    for i in range(1,n):
        # the distance of planet from x = 0
        x_distance = planet_data[i][0]

        # changing the position of planets
        # /100 so planets closer to the sun zoom in slower and vice versa
        # y is always 10 less than x
        planet_data[i][0] += (1*x_distance)/100         # x
        planet_data[i][1] = x_distance-10               # y

    return size_x,size_y

# for showing the information window on the right side of the screen
def show_info(n):
    # displaying the information window
    pygame.draw.rect(screen,'Black',((WIDTH-350,0),(WIDTH,HEIGHT)))
    screen.blit(close_surf,close_rect)

    # displaying planet information
    for i in range(len(parameters)):
        # getting planet information in a string 
        info = str(parameters[i]) + '  =  ' + str(planet_info[n][i]) + ' ' + str(units[i])
        # displaying planet information
        info_surf = font.render(info,False,'White')
        info_rect = info_surf.get_rect(topleft = (WIDTH - 320, i*35 + (k-100)))
        
        # displaying images of planets
        planet_surf = planetos[f'planeto{n}'][0]
        planet_rect = planetos[f'planeto{n}'][1]

        screen.blit(planet_surf,planet_rect)
        screen.blit(info_surf,info_rect)


showing_info = 0            # if the info window is open
running = 1                 # if program is running
while running:
    # to close the window when user clicks on close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # set running to false so while loop ends
            running = 0

    # to display the image 
    # blit - block image transfer
    # blit(imagehandle,position)
    screen.blit(bg_surf,(0,0))
    screen.blit(star_surf,star_rect)
    
    # to know which mouse,keyboard button the user has pressed and to get the position of the mouse
    mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    # set the revolving value of all planets to true (n-1 is the total number of planets)
    while pla_no < n:
        revolving[f'planet{pla_no}'] = 1
        pla_no += 1
   
    for i in range(1,n):
        # loops run for 8 times, checking for each planet
        # to make all the planets revolve
        if revolving[f'planet{i}'] >= 1:
            revolve(i)

    # if both are done in same loop, some planets will be diplayed over the info window    
    for i in range(1,n):
        # loops run for 8 times, checking for each planet

        # showing info window
        if planets[f'planet{i}'][1].collidepoint(mouse_pos) and mouse in MOUSE_B1:
            showing_info = i

        # showing planet information if info window is active
        if showing_info == i:
            show_info(i)

    # clicking on close, closes the window    
    if close_rect.collidepoint(mouse_pos) and mouse in MOUSE_B1:
        showing_info = 0 

    # check if q is pressed from keyboard
    # zooming out and storing the sizes of the planets
    if keys[pygame.K_q]: 
        size_x,size_y = zoom_out(size_x,size_y)

    # check if q is pressed from keyboard
    # zooming in and storing the sizes of the planets    
    if keys[pygame.K_e]: 
        size_x,size_y = zoom_in(size_x,size_y)
    
    #updating what is done in this iteration of the loop to display on the screen
    pygame.display.update()

    #fps
    clock.tick(60)

# if running is false then exit the program
if running == 0:
    pygame.quit()
    exit()