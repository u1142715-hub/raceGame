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
checkpoints = (
{"x":(3333),"y":(3333),"active":(0)}, # start finish marker 0
{"x":(3333),"y":(5000),"active":(0)}, # marker 1
{"x":(1800),"y":(6000),"active":(0)}, # marker 2
{"x":(1000),"y":(7500),"active":(0)}, # marker 3
{"x":(2500),"y":(8500),"active":(0)}, # marker 4
{"x":(4000),"y":(8500),"active":(0)}, # marker 5
{"x":(5000),"y":(5500),"active":(0)}, # marker 6
{"x":(7500),"y":(5000),"active":(0)}, # marker 7
{"x":(6666),"y":(6666),"active":(0)}, # marker 8
{"x":(6000),"y":(8500),"active":(0)}, # marker 9
{"x":(8000),"y":(8000),"active":(0)}, # marker 10
{"x":(8250),"y":(6000),"active":(0)}, # marker 11
{"x":(7800),"y":(4000),"active":(0)}, # marker 12
{"x":(6000),"y":(3000),"active":(0)}, # marker 13
{"x":(7200),"y":(1800),"active":(0)}, # marker 14
{"x":(6666),"y":(900),"active":(0)}, # marker 15
{"x":(3333),"y":(700),"active":(0)}, # marker 16
{"x":(600),"y":(1500),"active":(0)}, # marker 17
{"x":(2700),"y":(2700),"active":(0)}, # marker 18
)
lcheck = 0 
mainmapx = checkpoints[0]["x"]
mainmapy = checkpoints[0]["y"]

# Player Variables
acceleration = 0
speed = 0 
bestLapSpeed = 0
psize = 15 
mpx = 3135
mpy = 3100
blx=3333
bly=3333
playerRotation = 360-45 
bestLapRotation = 360-90
rotationArray = {}
# Time Variables
clock = pygame.time.Clock()
lapTime = 0.0 

# Ghost Player
currentLapPlayer = (
{"cfx": (mpx),"cfy": (mpy), "current frame":(0), "current speed": (speed), "current rotation": (playerRotation), "active": (1)}    
)
bestLapGhost=(
{"cfx": (blx),"cfy": (bly), "current frame":(0), "current speed": (0), "current rotation": (bestLapRotation), "active": (0)}     
)
# Initialization
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("raceGame1")
background = pygame.Color(white)

# Functions
# Ghost Player Function
def updateGhostPlayer(ghostPlayer,mpx,mpy):
    """
    @Summary:       Gets players inputs, and stores them in a dictionary

    @Parameters:    To be Decided
    
    @Returns:       updated dictionary
    """

# Calculation Functions
# Pre_Game Calculations for speed optimisation during play
def precalculations(rotationArray, psize):
    '''
    @Summary:       Precalculate maths operations before game starts and place them in an array
    @Parameters:    psize as integer, is used to scale the distance between circles
    @Returns:       rotationArray as a dictionary, contains rotation angle, calculated x,y positions for all 3 circles based on angle
    '''
    x = 300
    y = 300
    for angle in range(0, 365, 5):
        tpx = math.cos(math.radians(angle)) * psize + x
        tpy = math.sin(math.radians(angle)) * psize + y
        lpx = math.cos(math.radians(angle - 90)) * psize + x
        lpy = math.sin(math.radians(angle - 90)) * psize + y
        rpx = math.cos(math.radians(angle + 90)) * psize + x
        rpy = math.sin(math.radians(angle + 90)) * psize + y
        rotationArray[angle] = {
            "top":   (tpx, tpy),
            "left":  (lpx, lpy),
            "right": (rpx, rpy)
        }
    return rotationArray
 
# Display Functions
# Draw Player
def drawPlayer(rotationArray,playerRotation):
    tpx, tpy = rotationArray[playerRotation]["top"]
    lpx, lpy = rotationArray[playerRotation]["left"]
    rpx, rpy = rotationArray[playerRotation]["right"]
    pygame.draw.circle(screen, green, (tpx,tpy), 5) 
    pygame.draw.circle(screen, red, (lpx,lpy), 5) 
    pygame.draw.circle(screen, red, (rpx,rpy), 5) 

# Draw On Screen Display      
def showText(name,Value,x,y):
    font = pygame.font.SysFont(None, 20) 
    text_surface = font.render(f"{name}{Value}", True, (black))
    position = (x, y)
    screen.blit(text_surface, position)
    
# Draw Minimap
def dcheckpoint(mpx, mpy, checkpoints):
    '''
    @Summary:       Draws a minimap for player to easily see where they are in relation to track
    @Parameters:    mpx as integer
                    mpy as integer
                    checkpoints as tuple
    @Returns:       minimap top left of screen of track and player position
    '''
    scale = 100 
    fvar = 10000 
    sflinex = ((checkpoints[0]["x"])/scale) 
    sfliney = ((fvar-checkpoints[0]["y"])/scale) 
    lastx = sflinex 
    lasty = sfliney 
    for dcircle in checkpoints:
        xcircle = int((dcircle["x"])/scale) 
        ycircle = int((fvar-dcircle["y"])/scale)
        gcircle = int(dcircle["active"])
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
    y = 300 
    lastx = (checkpoints[18]["x"])
    lasty = (10000-checkpoints[18]["y"]) - (10000-mpy) + y 
    for checkpoint in checkpoints:
        xcheck = checkpoint["x"] - mpx + x 
        ycheck = (10000-checkpoint["y"]) - (10000-mpy) + y
        if 0 <= xcheck <= 600 and 0 <= ycheck <= 600: 
            if checkpoint["active"]==0:
                color = black
            else:
                color = green
            
            pygame.draw.circle(screen, color, (xcheck, ycheck), 75) 
        
        if checkpoint != checkpoints[0]: 
            pygame.draw.line(screen, black, (lastx, lasty), (xcheck, ycheck), 5) 
        lastx = xcheck 
        lasty = ycheck 
    sflinex = (checkpoints[0]["x"]) - mpx + x 
    sfliney = ((10000-checkpoints[0]["y"]) - (10000-mpy) + y) 
    pygame.draw.line(screen, black, (lastx, lasty), (sflinex, sfliney), 5)
 
# Main game engine function                   
def main(speed, acceleration,mpx, mpy, playerRotation, checkpoints, lapTime, lcheck):
    currentFrame = 0
    cx = checkpoints[0]["x"]
    cy = checkpoints[0]["y"]
    markercounter = 0
    bestLap = 55
    hrs = int(bestLap // 3600)
    mins = int((bestLap % 3600) // 60)
    secs = int(bestLap % 60)
    bestLap =f"{hrs:02}:{mins:02}:{secs:02}"
    elapsed = 0
    
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
                    
        # Check to see if first marker has been passed               
        if checkpoints[0]["active"] == 0 and (mpx - checkpoints[0]["x"])**2 + (mpy - checkpoints[0]["y"])**2 < 75**2:         
            checkpoints[0]["active"] = 1
            checkpoints[18]["active"] = 0 
            lcheck = 1
            lap_start = time.time()
            markercounter = markercounter + 1

        if lcheck ==1:
            currentFrame += 1
            elapsed = time.time() - lap_start
            hrs = int(elapsed // 3600)
            mins = int((elapsed % 3600) // 60)
            secs = int(elapsed % 60)
            lapTime =f"{hrs:02}:{mins:02}:{secs:02}"
            if (checkpoints[markercounter]["active"]) == 0:
                #check to see if player is on marker now
                cx = checkpoints[markercounter]["x"]
                cy = checkpoints[markercounter]["y"]
                if abs(cx-mpx) <75 and abs((cy)-(mpy))<75:
                    checkpoints[markercounter]["active"] = 1
                    markercounter += 1
                    if markercounter >18:
                        markercounter = 0
                        currentFrame = 0
                        for init in checkpoints[:-1]:
                            init["active"]=0
                            lcheck =0
                            if lapTime < bestLap:
                                bestLap = lapTime
                                #update ghost
                            

        # mpx, mpy = movePlayer(speed, playerRotation, mpx, mpy)
        dcheckpoint(mpx, mpy, checkpoints)   
        showtrackvsplayer(mpx, mpy, checkpoints)  
                
        # Draw Screen
        drawPlayer(rotationArray, playerRotation)
        showText("Speed ",speed,450,20)
        showText("Lap Time ",lapTime,450,40)
        showText("Best Lap",bestLap,450,60)
        showText("Current Frame",currentFrame,450,80)
        pygame.display.flip()
        clock.tick(30) 
              
# Run the game
#This function will loop 0 to 360, step 5, calculate maths values * psize(player size) 
# and put in an array. optimise for speed, so calculations only done once
rotationArray = precalculations(rotationArray, psize)
# Start Game
main(speed, acceleration, mpx, mpy, playerRotation, checkpoints, lapTime, lcheck)
