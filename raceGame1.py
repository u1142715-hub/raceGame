# Author: Sam Frederiksen 
# Date Started: 14/03/2026
# Import necessary libraries, so far personal best is 41 seconds, approx average speed 340
import pygame # Depending on python environment this may need to be set up using pygame-ce, but you still import pygame
import sys
import math
import time
import copy
# Classes
class Player:
    def __init__(self):
        self.mpx = 3135   
        self.mpy = 3100
        self.psize = 15 
        self.playerRotation = 315
        self.speed = 0
        self.currentFrame = 0
        self.acceleration = 0
        self.currentLapPlayer = {}
        self.rotationArray = {}
    
    def update(self):
        self.speed = self.speed + self.acceleration  
        self.mpx = self.mpx + math.cos(math.radians(self.playerRotation)) * self.speed * 0.1 
        self.mpy = self.mpy - math.sin(math.radians(self.playerRotation)) * self.speed * 0.1  
        
    def checkMouse(self):
        mouse = pygame.mouse.get_pressed() 
        if mouse[0] is True and self.speed > 0:     
            self.acceleration = -1    
        elif mouse[2] is True and self.speed < 1000: 
            self.acceleration = 1
        else:
            self.acceleration = 0 
    
    def checkQuit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
    
    def checkKey(self):
        if pygame.key.get_pressed()[pygame.K_a]:
            self.playerRotation = (self.playerRotation - 5) % 360
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.playerRotation = (self.playerRotation + 5) % 360 
        self.playerRotation=self.playerRotation % 360
        
    def drawPlayer1(self, dscreen, bestLapGhost):
        tpx, tpy = self.rotationArray[self.playerRotation]["top"]
        lpx, lpy = self.rotationArray[self.playerRotation]["left"]
        rpx, rpy = self.rotationArray[self.playerRotation]["right"]
        self.currentLapPlayer[self.currentFrame] = {
            "speed": self.speed,
            "pRotation": self.playerRotation,
            "mpx": self.mpx,
            "mpy": self.mpy,
            "top": (tpx, tpy),
            "left": (lpx, lpy),
            "right": (rpx, rpy),
    }
        pygame.draw.circle(dscreen.screen, dscreen.green, self.currentLapPlayer[self.currentFrame]["top"], 5)
        pygame.draw.circle(dscreen.screen, dscreen.red, self.currentLapPlayer[self.currentFrame]["left"], 5)
        pygame.draw.circle(dscreen.screen, dscreen.red, self.currentLapPlayer[self.currentFrame]["right"], 5)
        if bestLapGhost and self.currentFrame in bestLapGhost:
            gmpx = bestLapGhost[self.currentFrame]["mpx"]
            gmpy = bestLapGhost[self.currentFrame]["mpy"]
            gx = gmpx - self.mpx + 300
            gy = (10000 - gmpy) - (10000 - self.mpy) + 300
            grot = bestLapGhost[self.currentFrame]["pRotation"]
            gt, gl, gr = self.rotationArray[grot]["top"], self.rotationArray[grot]["left"], self.rotationArray[grot]["right"]
            pygame.draw.circle(dscreen.screen, dscreen.green, (gx + (gt[0] - 300), gy + (gt[1] - 300)), 5)
            pygame.draw.circle(dscreen.screen, dscreen.red,   (gx + (gl[0] - 300), gy + (gl[1] - 300)), 5)
            pygame.draw.circle(dscreen.screen, dscreen.red,   (gx + (gr[0] - 300), gy + (gr[1] - 300)), 5)
    
    def precalculations(self):
        x = 300
        y = 300
        for angle in range(0, 365, 5):
            tpx = math.cos(math.radians(angle)) * self.psize + x
            tpy = math.sin(math.radians(angle)) * self.psize + y
            lpx = math.cos(math.radians(angle - 90)) * self.psize + x
            lpy = math.sin(math.radians(angle - 90)) * self.psize + y
            rpx = math.cos(math.radians(angle + 90)) * self.psize + x
            rpy = math.sin(math.radians(angle + 90)) * self.psize + y
            self.rotationArray[angle] = {
                "top":   (tpx, tpy),
                "left":  (lpx, lpy),
                "right": (rpx, rpy)
            }
        return self.rotationArray
class DrawScreen:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))
        self.white = pygame.Color(255, 255, 255)
        self.black = pygame.Color(0, 0, 0)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
    
    def hud(self,player, lapTime, bestLap):
        self.showText("Speed ",player.speed, 450, 20)
        self.showText("Lap Time ", lapTime, 450, 40)
        self.showText("Best Lap", bestLap, 450, 60)
        self.showText("Current Frame", player.currentFrame, 450, 80)
    
    def showText(self, name,Value,x,y):  
        font = pygame.font.SysFont(None, 20) 
        text_surface = font.render(f"{name}{Value}", True, (self.black))
        position = (x, y)
        self.screen.blit(text_surface, position) 
class Checkpoints:
    def __init__(self):
        pass
        
# Functions
    
def dcheckpoint(player, checkpoints, dscreen):
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
            color=dscreen.black
        else:
            color=dscreen.green
        pygame.draw.circle(dscreen.screen, color, (xcircle, ycircle), 2) 
        pygame.draw.line(dscreen.screen, dscreen.black, (lastx, lasty), (xcircle, ycircle), 1) 
        lastx = xcircle 
        lasty = ycircle    
    pygame.draw.line(dscreen.screen, dscreen.black, (lastx, lasty), (sflinex, sfliney), 1)
    pygame.draw.circle(dscreen.screen, dscreen.red, (player.mpx/scale, (fvar-player.mpy)/scale), 2) 

def showtrackvsplayer(player, checkpoints, dscreen):
    x = 300 
    y = 300 
    lastx = (checkpoints[18]["x"])
    lasty = (10000-checkpoints[18]["y"]) - (10000-player.mpy) + y 
    for checkpoint in checkpoints:
        xcheck = checkpoint["x"] - player.mpx + x 
        ycheck = (10000-checkpoint["y"]) - (10000-player.mpy) + y
        if 0 <= xcheck <= 600 and 0 <= ycheck <= 600: 
            if checkpoint["active"]==0:
                color = dscreen.black
            else:
                color = dscreen.green
            pygame.draw.circle(dscreen.screen, color, (xcheck, ycheck), 75) 
        if checkpoint != checkpoints[0]: 
            pygame.draw.line(dscreen.screen, dscreen.black, (lastx, lasty), (xcheck, ycheck), 5) 
        lastx = xcheck 
        lasty = ycheck 
    sflinex = (checkpoints[0]["x"]) - player.mpx + x 
    sfliney = ((10000-checkpoints[0]["y"]) - (10000-player.mpy) + y) 
    pygame.draw.line(dscreen.screen, dscreen.black, (lastx, lasty), (sflinex, sfliney), 5)
 
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
    clock = pygame.time.Clock()
    lapTime = 0.0  
    bestLapGhost= {}     
    pygame.init()
    pygame.display.set_caption("raceGame1")
    cx = checkpoints[0]["x"]
    cy = checkpoints[0]["y"]
    markercounter = 0
    bestLap = 300
    hrs = int(bestLap // 3600)
    mins = int((bestLap % 3600) // 60)
    secs = int(bestLap % 60)
    bestLap =f"{hrs:02}:{mins:02}:{secs:02}"
    elapsed = 0
    player.precalculations()
    while True:
        dscreen.screen.fill(dscreen.white)
        player.checkQuit()
        player.checkKey()
        player.checkMouse()
        player.update()             
        if checkpoints[0]["active"] == 0 and (player.mpx - checkpoints[0]["x"])**2 + (player.mpy - checkpoints[0]["y"])**2 < 75**2:         
            checkpoints[0]["active"] = 1
            checkpoints[18]["active"] = 0 
            lcheck = 1
            lap_start = time.time()
            markercounter = markercounter + 1
        if lcheck ==1:
            player.currentFrame += 1
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
                        player.currentFrame = 0
                        if lapTime < bestLap:
                            bestLap = lapTime
                            bestLapGhost = copy.deepcopy(player.currentLapPlayer)
                        player.currentLapPlayer = {}
                        for init in checkpoints[:-1]:
                            init["active"]=0
                            lcheck =0
        dcheckpoint(player, checkpoints, dscreen)   
        showtrackvsplayer(player, checkpoints, dscreen)  
        player.drawPlayer1(dscreen, bestLapGhost)
        dscreen.hud(player, lapTime, bestLap)
        pygame.display.flip()
        clock.tick(30) 
              
main()