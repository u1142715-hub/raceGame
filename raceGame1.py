# raceGame1.py
# This is a simple racing game implemented in Python using the Pygame library. 
# The player controls a car that can accelerate, decelerate, and turn left or right. 
# The game includes a track with checkpoints that the player must pass through to complete laps. 
# The player's speed and lap time are displayed on the screen. 
# The game loop handles user input, updates the game state, and renders the game on the screen.
# Note: This code is a basic implementation and can be expanded with additional features 
# such as sound effects, more complex track designs, and improved graphics. 
# Adjust the code as needed to fit your specific requirements and preferences.
# Author: Sam Frederiksen 
# Date Started: 14/03/2026

# Import necessary libraries
import pygame 
import sys
import math
import time

# Variables
# Colors
white=pygame.Color(255, 255, 255)
black=pygame.Color(0, 0, 0)
red=pygame.Color(255, 0, 0)
green=pygame.Color(0, 255, 0)

# Checkpoints
checkpoints = [(3333,3333,0),(3333,5000,0),(1800,6000,0),(1000,7500,0),(2500,8500,0),(4000,8500,0),
               (5000,5500,0),(7500,5000,0),(6666,6666,0),(6000,8500,0),(8000,8800,0),(8250,6000,0),
               (7800,4000,0),(6000,3000,0),(7200,1800,0),(6666,900,0),(3333,700,0),(600,1500,0),(2700,2700,0)]
lcheck = 0 
mainmapx = checkpoints[0][0]
mainmapy = checkpoints[0][1]

# Player Variables
acceleration = 0
speed = 0 
psize = 15 
mpx = 3135
mpy = 3100
playerRotation = 360-45 

# Time Variables
clock = pygame.time.Clock()
lapTime = 0.0 

# Initialization
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("raceGame1")
background = pygame.Color(white)

# Functions
# Input Functions

# Calculation Functions

# Display Functions
# Draw Player
def drawPlayer(tpx,tpy,lpx,lpy,rpx,rpy):
    pygame.draw.circle(screen, green, (tpx,tpy), 5) 
    pygame.draw.circle(screen, red, (lpx,lpy), 5) 
    pygame.draw.circle(screen, red, (rpx,rpy), 5) 

# Draw On Screen Display      
def showText(Value,x,y):
    font = pygame.font.SysFont(None, 20) 
    text_surface = font.render(f"Local Time: {Value}", True, (black))
    position = (x, y)
    screen.blit(text_surface, position)
    
# Draw Minimap
def dcheckpoint(mpx, mpy, checkpoints):
    scale = 100 
    fvar = 10000 
    sflinex = (checkpoints[0][0]/scale) 
    sfliney = ((fvar-checkpoints[0][1])/scale) 
    lastx = sflinex 
    lasty = sfliney 
    for dcircle in checkpoints:
        xcircle = int(dcircle[0]/scale) 
        ycircle = int((fvar-dcircle[1])/scale)
        gcircle = int(dcircle[2])
        if gcircle == 0:
            color=black
        else:
            color=green
        
        pygame.draw.circle(screen, color, (xcircle, ycircle), 2) 
        pygame.draw.line(screen, black, (lastx, lasty), (xcircle, ycircle), 1) 
        lastx = xcircle 
        lasty = ycircle
               
    pygame.draw.line(screen, black, (lastx, lasty), (sflinex, sfliney), 1)
    pygame.draw.circle(screen, red, (mpx/scale, (fvar-mpy)/scale), 2) 

# Draw Track   
def showtrackvsplayer(mpx, mpy, checkpoints):
    '''
    @Summary:       Draws track on screen, based on player center point x,y (player only rotates does not move, track moves instead)
    @Parameters:    mpx as integer, first value, players x coordinate on main scale
                    mpy as integer, 2nd value, players y coordinate on main scale
                    checkpoints as tuple, holds x,y position for checkpoints, and third value is to check if player passed through correctly
    @Returns:       None, however draws 75px diameter circles, color based on test, and only if close enough to player, 
                    draws line between checkpoints, only if in range of player.
    '''
    
    x = 300 
    y = 550 
    lastx = (checkpoints[18][0])
    lasty = (10000-checkpoints[18][1]) - (10000-mpy) + y 
    for checkpoint in checkpoints:
        xcheck = checkpoint[0] - mpx + x 
        ycheck = (10000-checkpoint[1]) - (10000-mpy) + y
        if 0 <= xcheck <= 600 and 0 <= ycheck <= 600: 
            if checkpoint[2]==0:
                color = black
            else:
                color = green
            
            pygame.draw.circle(screen, color, (xcheck, ycheck), 75) 
        
        if checkpoint != checkpoints[0]: 
            pygame.draw.line(screen, black, (lastx, lasty), (xcheck, ycheck), 5) 
        lastx = xcheck 
        lasty = ycheck 
    sflinex = (checkpoints[0][0]) - mpx + x 
    sfliney = ((10000-checkpoints[0][1]) - (10000-mpy) + y) 
    pygame.draw.line(screen, black, (lastx, lasty), (sflinex, sfliney), 5)
    
# Race Functions
def dPlayer(x,y,playerRotation,psize):
    # PreCalculate this throw all answers in array to speed game up - Optimisation 1        
    tpx=math.cos(math.radians(playerRotation)) * psize + x 
    tpy=math.sin(math.radians(playerRotation)) * psize + y 
    lpx=math.cos(math.radians(playerRotation - 90)) * psize + x 
    lpy=math.sin(math.radians(playerRotation - 90)) * psize + y 
    rpx=math.cos(math.radians(playerRotation + 90)) * psize + x 
    rpy=math.sin(math.radians(playerRotation + 90)) * psize + y 
    return tpx,tpy,lpx,lpy,rpx,rpy 
                
def main(speed, acceleration,mpx, mpy, playerRotation, checkpoints, lapTime, lcheck):
    # Main Loop
    
    while True:
        screen.fill(background)
        # Escape Loop if window closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # Check for Key Press
        if pygame.key.get_pressed()[pygame.K_a]:
            playerRotation = (playerRotation - 5) % 360
        elif pygame.key.get_pressed()[pygame.K_d]:
            playerRotation = (playerRotation + 5) % 360 
        
        playerRotation=playerRotation % 360
        
        # Check mouse state
        mouse = pygame.mouse.get_pressed() 
        if mouse[0] is True and speed > 0:     
            acceleration = -1    
        elif mouse[2] is True and speed < 1000: 
            acceleration = 1
        else:
            acceleration = 0 
        
        # Calculations
        # Update Speed 
        speed = speed + acceleration  
        
        # Move Player
        mpx = mpx + math.cos(math.radians(playerRotation)) * speed * 0.1 
        mpy = mpy - math.sin(math.radians(playerRotation)) * speed * 0.1 
        tpx,tpy,lpx,lpy,rpx,rpy = dPlayer(300, 514,playerRotation,psize)
            
        # lapTime = sTime(lapTime)
        if checkpoints[0][2] == 0 and (mpx - checkpoints[0][0])**2 + (mpy - checkpoints[0][1])**2 < 75**2:         
            checkpoints[0] = (checkpoints[0][0], checkpoints[0][1], 1) 
            lapTime = float(0.0) 
            lcheck ="Lap started"
        
        # mpx, mpy = movePlayer(speed, playerRotation, mpx, mpy)
        dcheckpoint(mpx, mpy, checkpoints)   
        showtrackvsplayer(mpx, mpy, checkpoints)  
                
        # Draw Screen
        drawPlayer(tpx,tpy,lpx,lpy,rpx,rpy)
        showText(speed,450,20)
        showText((time.strftime("%H:%M:%S", time.localtime())),450,40)
        showText(lapTime,450,60)
        pygame.display.flip()
        clock.tick(30) 
              
# Run the game
# precalculations() #This function will loop 0 to 360, step 5, calculate maths values * psize(player size) 
# and put in an array. optimise for speed, so calculations only done once
main(speed, acceleration, mpx, mpy, playerRotation, checkpoints, lapTime, lcheck)
