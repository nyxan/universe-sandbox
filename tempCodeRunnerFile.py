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