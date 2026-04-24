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
        self.currentFrame = 0
        self.currentLapPlayer = {}
        self.rotationArray = {}
        self.speed = 0
        self.acceleration = 0
        self.playerRotation = 315  
    
    def update(self):
        self.speed = self.speed + self.acceleration  
        self.mpx = self.mpx + math.cos(math.radians(self.playerRotation)) * self.speed * 0.1 
        self.mpy = self.mpy - math.sin(math.radians(self.playerRotation)) * self.speed * 0.1  
        
    def RecordFrame(self):
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
            "right": (rpx, rpy),}
    
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
        
    def drawPlayer(self, player):
        player.RecordFrame()
        pygame.draw.circle(self.screen, self.green, player.currentLapPlayer[player.currentFrame]["top"], 5)
        pygame.draw.circle(self.screen, self.red, player.currentLapPlayer[player.currentFrame]["left"], 5)
        pygame.draw.circle(self.screen, self.red, player.currentLapPlayer[player.currentFrame]["right"], 5)

    def drawGhost(self, rM, player):
        data = rM.ghostPlayer(player)
        if not data:
            return
        pygame.draw.circle(self.screen, self.green, data["top"], 5)
        pygame.draw.circle(self.screen, self.red, data["left"], 5)
        pygame.draw.circle(self.screen, self.red, data["right"], 5)
            
    def showtrackvsplayer(self, player, checkpoints):
        x = 300 
        y = 300 
        lastx = (checkpoints[18]["x"])
        lasty = (10000-checkpoints[18]["y"]) - (10000-player.mpy) + y 
        for checkpoint in checkpoints:
            xcheck = checkpoint["x"] - player.mpx + x 
            ycheck = (10000-checkpoint["y"]) - (10000-player.mpy) + y
            if 0 <= xcheck <= 600 and 0 <= ycheck <= 600: 
                if checkpoint["active"]==0:
                    color = self.black
                else:
                    color = self.green
                pygame.draw.circle(self.screen, color, (xcheck, ycheck), 75) 
            if checkpoint != checkpoints[0]: 
                pygame.draw.line(self.screen, self.black, (lastx, lasty), (xcheck, ycheck), 5) 
            lastx = xcheck 
            lasty = ycheck 
        sflinex = (checkpoints[0]["x"]) - player.mpx + x 
        sfliney = ((10000-checkpoints[0]["y"]) - (10000-player.mpy) + y) 
        pygame.draw.line(self.screen, self.black, (lastx, lasty), (sflinex, sfliney), 5)
class InputHandler:   
    def __init__(self):
        pass
    
    def checkMouse(self, player):
        mouse = pygame.mouse.get_pressed() 
        if mouse[0] is True and player.speed > 0:     
            player.acceleration = -1    
        elif mouse[2] is True and player.speed < 1000: 
            player.acceleration = 1
        else:
            player.acceleration = 0 
    
    def checkQuit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
    
    def checkKey(self, player):
        if pygame.key.get_pressed()[pygame.K_a]:
            player.playerRotation = (player.playerRotation - 5) % 360
        elif pygame.key.get_pressed()[pygame.K_d]:
            player.playerRotation = (player.playerRotation + 5) % 360 
        player.playerRotation = player.playerRotation % 360
class RaceManager:
    def __init__(self):
        self.checkpoints = (
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
        {"x":(2700),"y":(2700),"active":(0)},) # marker 18
        self.lcheck = 0
        self.lapTime = 0.0
        self.bestLapGhost = {}
        self.markercounter = 0
        self.bestLap = 300
        self.elapsed = 0
        self.lap_start = None
        self.cx = self.checkpoints[0]["x"]
        self.cy = self.checkpoints[0]["y"]
        self.scale = 100
        self.fvar = 10000
        self.sflinex = 0
        self.sfliney = 0
        self.lastx = 0
        self.lasyy = 0
        
    def cPoint(self, player, dscreen):
        self.sflinex = (self.checkpoints[0]["x"])/self.scale
        self.sfliney = ((self.fvar-self.checkpoints[0]["y"])/self.scale) 
        self.lastx = self.sflinex 
        self.lasty = self.sfliney
        for dcircle in self.checkpoints:
            xcircle = int((dcircle["x"])/self.scale) 
            ycircle = int((self.fvar-dcircle["y"])/self.scale)
            gcircle = int(dcircle["active"])
            if gcircle == 0:
                color=dscreen.black
            else:
                color=dscreen.green
            pygame.draw.circle(dscreen.screen, color, (xcircle, ycircle), 2) 
            pygame.draw.line(dscreen.screen, dscreen.black, (self.lastx, self.lasty), (xcircle, ycircle), 1) 
            self.lastx = xcircle 
            self.lasty = ycircle    
        pygame.draw.line(dscreen.screen, dscreen.black, (self.lastx, self.lasty), (self.sflinex, self.sfliney), 1)
        pygame.draw.circle(dscreen.screen, dscreen.red, (player.mpx/self.scale, (self.fvar-player.mpy)/self.scale), 2) 
        
    def checkRaceStart(self,player):
        if self.checkpoints[0]["active"] == 0 and (player.mpx - self.checkpoints[0]["x"])**2 + (player.mpy - self.checkpoints[0]["y"])**2 < 75**2:         
            self.checkpoints[0]["active"] = 1
            self.checkpoints[18]["active"] = 0 
            self.lcheck = 1
            self.lap_start = time.time()
            self.markercounter = self.markercounter + 1    

    def raceMode(self, player):
        if self.lcheck ==1:
            player.currentFrame += 1
            self.elapsed = time.time() - self.lap_start
            hrs = int(self.elapsed // 3600)
            mins = int((self.elapsed % 3600) // 60)
            secs = int(self.elapsed % 60)
            self.lapTime =f"{hrs:02}:{mins:02}:{secs:02}"
            if (self.checkpoints[self.markercounter]["active"]) == 0:
                self.cx = self.checkpoints[self.markercounter]["x"]
                self.cy = self.checkpoints[self.markercounter]["y"]
            if abs(self.cx-player.mpx) <75 and abs((self.cy)-(player.mpy))<75:
                self.checkpoints[self.markercounter]["active"] = 1
                self.markercounter += 1
            if self.markercounter >18:
                self.markercounter = 0
                player.currentFrame = 0
                if self.lapTime < self.bestLap:
                    self.bestLap = self.lapTime
                    self.bestLapGhost = copy.deepcopy(player.currentLapPlayer)
                player.currentLapPlayer = {}
                for init in self.checkpoints[:-1]:
                    init["active"]=0
                    self.lcheck =0
                     
    def ghostPlayer(self, player):
        frame = player.currentFrame
        if frame not in self.bestLapGhost:
            return None
        ghost = self.bestLapGhost[frame]
        gmpx = ghost["mpx"]
        gmpy = ghost["mpy"]
        gx = gmpx - player.mpx + 300
        gy = (10000 - gmpy) - (10000 - player.mpy) + 300
        grot = ghost["pRotation"]
        gt = player.rotationArray[grot]["top"]
        gl = player.rotationArray[grot]["left"]
        gr = player.rotationArray[grot]["right"]
        return { "top": (gx + (gt[0] - 300), gy + (gt[1] - 300)),
            "left": (gx + (gl[0] - 300), gy + (gl[1] - 300)),
            "right": (gx + (gr[0] - 300), gy + (gr[1] - 300)),}

# Functions
def main():
    player = Player()
    dscreen = DrawScreen()
    iHandler = InputHandler()
    rM = RaceManager()
    clock = pygame.time.Clock()    
    pygame.init()
    pygame.display.set_caption("raceGame1")
    hrs = int(rM.bestLap // 3600)
    mins = int((rM.bestLap % 3600) // 60)
    secs = int(rM.bestLap % 60)
    rM.bestLap =f"{hrs:02}:{mins:02}:{secs:02}"
    player.precalculations()
    while True:
        dscreen.screen.fill(dscreen.white)
        iHandler.checkQuit()
        iHandler.checkKey(player)
        iHandler.checkMouse(player) 
        player.update() 
        rM.checkRaceStart(player) 
        rM.raceMode(player)          
        rM.cPoint(player, dscreen)   
        dscreen.showtrackvsplayer(player, rM.checkpoints)  
        dscreen.drawPlayer(player)
        dscreen.drawGhost(rM, player)
        dscreen.hud(player, rM.lapTime, rM.bestLap)
        pygame.display.flip()
        clock.tick(30) 
              
main()