# Author: Sam Frederiksen 
# Date Started: 14/03/2026
# Import necessary libraries, so far personal best is 41 seconds, approx average speed 340
import pygame # Depending on python environment this may need to be set up using pygame-ce, but you still import pygame
import sys
import math
import time
import copy
# Game Colors
white=pygame.Color(255, 255, 255)
black=pygame.Color(0, 0, 0)
red=pygame.Color(255, 0, 0)
green=pygame.Color(0, 255, 0)
# Classes
class Player:
    def __init__(self):
        self.mpx = 3135   
        self.mpy = 3100
        self.psize = 15 
        self.playerRotation = 315
        self.speed = 0
class Checkpoints:
    def __init__(self):
        pass
class DrawScreen:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))
        
# Functions
def precalculations(player, rotationArray):
    '''
    @Summary:       Precalculate maths operations before game starts and place them in an array
    @Parameters:    psize as integer, is used to scale the distance between circles
    @Returns:       rotationArray as a dictionary, contains rotation angle, calculated x,y positions for all 3 circles based on angle
    '''
    x = 300
    y = 300
    for angle in range(0, 365, 5):
        tpx = math.cos(math.radians(angle)) * player.psize + x
        tpy = math.sin(math.radians(angle)) * player.psize + y
        lpx = math.cos(math.radians(angle - 90)) * player.psize + x
        lpy = math.sin(math.radians(angle - 90)) * player.psize + y
        rpx = math.cos(math.radians(angle + 90)) * player.psize + x
        rpy = math.sin(math.radians(angle + 90)) * player.psize + y
        rotationArray[angle] = {
            "top":   (tpx, tpy),
            "left":  (lpx, lpy),
            "right": (rpx, rpy)
        }
    return rotationArray
 
def drawPlayer(player, currentLapPlayer, currentFrame, rotationArray, screen,bestLapGhost):
    """
    Records the player's state for this frame and draws the player circles.
    Stores:
        - speed
        - rotation
        - top/left/right circle positions
    """
    tpx, tpy = rotationArray[player.playerRotation]["top"]
    lpx, lpy = rotationArray[player.playerRotation]["left"]
    rpx, rpy = rotationArray[player.playerRotation]["right"]
    currentLapPlayer[currentFrame] = {
        "speed": player.speed,
        "pRotation": player.playerRotation,
        "mpx": player.mpx,
        "mpy": player.mpy,
        "top": (tpx, tpy),
        "left": (lpx, lpy),
        "right": (rpx, rpy),
}
    pygame.draw.circle(screen, green, currentLapPlayer[currentFrame]["top"], 5)
    pygame.draw.circle(screen, red, currentLapPlayer[currentFrame]["left"], 5)
    pygame.draw.circle(screen, red, currentLapPlayer[currentFrame]["right"], 5)
    if bestLapGhost and currentFrame in bestLapGhost:
        gmpx = bestLapGhost[currentFrame]["mpx"]
        gmpy = bestLapGhost[currentFrame]["mpy"]
        gx = gmpx - player.mpx + 300
        gy = (10000 - gmpy) - (10000 - player.mpy) + 300
        grot = bestLapGhost[currentFrame]["pRotation"]
        gt, gl, gr = rotationArray[grot]["top"], rotationArray[grot]["left"], rotationArray[grot]["right"]
        pygame.draw.circle(screen, green, (gx + (gt[0] - 300), gy + (gt[1] - 300)), 5)
        pygame.draw.circle(screen, red,   (gx + (gl[0] - 300), gy + (gl[1] - 300)), 5)
        pygame.draw.circle(screen, red,   (gx + (gr[0] - 300), gy + (gr[1] - 300)), 5)

def showText(name,Value,x,y, screen):
    font = pygame.font.SysFont(None, 20) 
    text_surface = font.render(f"{name}{Value}", True, (black))
    position = (x, y)
    screen.blit(text_surface, position)
    
def dcheckpoint(player, checkpoints, screen):
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
    pygame.draw.circle(screen, red, (player.mpx/scale, (fvar-player.mpy)/scale), 2) 

def showtrackvsplayer(player, checkpoints, screen):
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
    lasty = (10000-checkpoints[18]["y"]) - (10000-player.mpy) + y 
    for checkpoint in checkpoints:
        xcheck = checkpoint["x"] - player.mpx + x 
        ycheck = (10000-checkpoint["y"]) - (10000-player.mpy) + y
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
    sflinex = (checkpoints[0]["x"]) - player.mpx + x 
    sfliney = ((10000-checkpoints[0]["y"]) - (10000-player.mpy) + y) 
    pygame.draw.line(screen, black, (lastx, lasty), (sflinex, sfliney), 5)
 
def main():
    player = Player()
    dscreen = DrawScreen()
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
    acceleration = 0
    rotationArray = {}
    clock = pygame.time.Clock()
    lapTime = 0.0 
    currentLapPlayer = {}  
    bestLapGhost= {}     
    pygame.init()
    screen = dscreen.screen
    pygame.display.set_caption("raceGame1")
    background = pygame.Color(white)
    currentFrame = 0
    cx = checkpoints[0]["x"]
    cy = checkpoints[0]["y"]
    markercounter = 0
    bestLap = 300
    hrs = int(bestLap // 3600)
    mins = int((bestLap % 3600) // 60)
    secs = int(bestLap % 60)
    bestLap =f"{hrs:02}:{mins:02}:{secs:02}"
    elapsed = 0
    rotationArray = precalculations(player, rotationArray)
    while True:
        screen.fill(background)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        if pygame.key.get_pressed()[pygame.K_a]:
            player.playerRotation = (player.playerRotation - 5) % 360
        elif pygame.key.get_pressed()[pygame.K_d]:
            player.playerRotation = (player.playerRotation + 5) % 360 
        player.playerRotation=player.playerRotation % 360
        mouse = pygame.mouse.get_pressed() 
        if mouse[0] is True and player.speed > 0:     
            acceleration = -1    
        elif mouse[2] is True and player.speed < 1000: 
            acceleration = 1
        else:
            acceleration = 0 
        player.speed = player.speed + acceleration  
        player.mpx = player.mpx + math.cos(math.radians(player.playerRotation)) * player.speed * 0.1 
        player.mpy = player.mpy - math.sin(math.radians(player.playerRotation)) * player.speed * 0.1               
        if checkpoints[0]["active"] == 0 and (player.mpx - checkpoints[0]["x"])**2 + (player.mpy - checkpoints[0]["y"])**2 < 75**2:         
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
                cx = checkpoints[markercounter]["x"]
                cy = checkpoints[markercounter]["y"]
                if abs(cx-player.mpx) <75 and abs((cy)-(player.mpy))<75:
                    checkpoints[markercounter]["active"] = 1
                    markercounter += 1
                    if markercounter >18:
                        markercounter = 0
                        currentFrame = 0
                        if lapTime < bestLap:
                            bestLap = lapTime
                            bestLapGhost = copy.deepcopy(currentLapPlayer)
                        currentLapPlayer = {}
                        for init in checkpoints[:-1]:
                            init["active"]=0
                            lcheck =0
        dcheckpoint(player, checkpoints, screen)   
        showtrackvsplayer(player, checkpoints, screen)  
        drawPlayer(player, currentLapPlayer, currentFrame, rotationArray, screen, bestLapGhost)
        showText("Speed ",player.speed, 450, 20, screen)
        showText("Lap Time ", lapTime, 450, 40, screen)
        showText("Best Lap", bestLap, 450, 60, screen)
        showText("Current Frame", currentFrame, 450, 80, screen)
        pygame.display.flip()
        clock.tick(30) 
              
main()