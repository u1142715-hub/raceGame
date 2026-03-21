# Race verse self game, written by Sam Langhof Frederiksen, Started on 2024-06-17

# Imports
import pygame
import sys
import math

# Initialization
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("raceGame1")

# Variables
clock = pygame.time.Clock()
white=pygame.Color(255, 255, 255)
black=pygame.Color(0, 0, 0)
red=pygame.Color(255, 0, 0)
green=pygame.Color(0, 255, 0)
background = pygame.Color(white)
acceleration = 0
speed = 0 # Initial speed of the player
mpx = 3333 # x position of the track, not implemented in this code snippet
mpy = 3300 # y position of the track, not implemented in this code snippet
playerRotation = 360-90 # Rotation of the player, not implemented in this code snippet, y values inverted for easier math with the track coordinates, adjust as needed
# List of checkpoints on the track, represented as tuples of (x, y) coordinates, not implemented in this code snippet
checkpoints = [(3333,3333),(3333,5000),(1800,6000),(1000,7500),(2500,8500),(4000,8500),
               (5000,5500),(7500,5000),(6666,6666),(6000,8500),(8000,8800),(8250,6000),
               (7800,4000),(6000,3000),(7200,1800),(6666,900),(3333,700),(600,1500),(2700,2700)] 
mainmapx = checkpoints[0][0] # x position of the start/finish line of the main map
mainmapy = checkpoints[0][1] # y position of the start/finish line of the main map

# Functions
def dPlayer(x,y,playerRotation):
    '''
    @Summary:   Draws the player on the screen at the specified position and rotation
    @Parameters: x as integer, the x coordinate of the player on the screen
                    y as integer, the y coordinate of the player on the screen
                    playerRotation as integer, the rotation of the player in degrees
    @Returns:   None, but draws the player on the screen at the specified position and rotation 
                              .
                            .   .
    '''
    # draw the default player as equalateral triangle with the front of the player in green and the left and right sides in red, not implemented in this code snippet       
    psize = 15 # Size of the player, adjust as needed   
    tpx=math.cos(math.radians(playerRotation)) * psize + x # Calculate the x coordinate of the front of the player based on the player rotation, not implemented in this code snippet
    tpy=math.sin(math.radians(playerRotation)) * psize + y # Calculate the y coordinate of the front of the player based on the player rotation, not implemented in this code snippet
    lpx=math.cos(math.radians(playerRotation - 90)) * psize + x # Calculate the x coordinate of the left side of the player based on the player rotation, not implemented in this code snippet
    lpy=math.sin(math.radians(playerRotation - 90)) * psize + y # Calculate the y coordinate of the left side of the player based on the player rotation, not implemented in this code snippet
    rpx=math.cos(math.radians(playerRotation + 90)) * psize + x # Calculate the x coordinate of the right side of the player based on the player rotation, not implemented in this code snippet
    rpy=math.sin(math.radians(playerRotation + 90)) * psize + y # Calculate the y coordinate of the right side of the player based on the player rotation, not implemented in this code snippet    
    pygame.draw.circle(screen, green, (tpx,tpy), 5) # Draw the front of the player
    pygame.draw.circle(screen, red, (lpx,lpy), 5) # Draw the left side of the player
    pygame.draw.circle(screen, red, (rpx,rpy), 5) # Draw the right side of the player
    
def sSpeed(speed):    
    '''
    @Summary: Displays the speed of the player on the screen
    @Parameters: speed as integer, the speed of the player  
    @Returns: A text surface that shows the speed of the player
    '''
    font = pygame.font.SysFont(None, 24)
    word = "Speed"
    value = speed
    text_surface = font.render(f"{word}: {value}", True, (black)) 
    position = (500, 20) 
    screen.blit(text_surface, position)
    
def m_acceleration(acceleration, speed):
    '''
    @Summary: Gets the mouse input for acceleration and updates the acceleration variable
    @Parameters: acceleration as integer, the current acceleration of the player
                 speed as integer, the current speed of the player  
    @Returns: Updated acceleration based on mouse input and speed limits
    '''
    mouse = pygame.mouse.get_pressed() 
    if mouse[0] is True and speed > 0:     
        acceleration = -1    
    elif mouse[2] is True and speed < 500: 
        acceleration = 1
    else:
        acceleration = 0 
    return acceleration  

def dcheckpoint(mpx, mpy, checkpoints):
    '''
    @Summary:    Draws a checkpoint on the screen
    @Parameters: mpx as integer, the current x position of the track     
                 mpy as integer, the current y position of the track 
                 checkpoints as list of tuples, the x and y coordinates of the checkpoints to be drawn
    @Returns:    None, but draws a checkpoint on the screen at the specified position
    '''
    # This function is not implemented in the main game loop, but can be used to draw checkpoints
    # on the track based on their position relative to the current position of the track
    # Draw minimap of the track with checkpoints, not implemented in this code snippet
    # function variable to determine how many checkpoints to draw on the minimap, adjust as needed
    scale = 100 # Scale factor for the minimap, adjust as needed
    fvar = 10000 # Variable to determine how many checkpoints to draw on the minimap, adjust as needed
    sflinex = (checkpoints[0][0]/scale) # x coordinate of the start/finish line of the track, not implemented in this code snippet
    sfliney = ((fvar-checkpoints[0][1])/scale) # y coordinate of the start/finish line of the track, not implemented in this code snippet
    lastx = sflinex # x coordinate of the last checkpoint drawn on the minimap, not implemented in this code snippet
    lasty = sfliney # y coordinate of the last checkpoint drawn on the minimap, not implemented in this code snippet
    for dcircle in checkpoints:
        # Pause the program to allow for step-by-step drawing of checkpoints on the minimap, not implemented in this code snippet
        xcircle = int(dcircle[0]/scale) # Scale down the x coordinate of the checkpoint for the minimap
        ycircle = int((fvar-dcircle[1])/scale) # Scale down the y coordinate of the checkpoint for the minimap
        pygame.draw.circle(screen, black, (xcircle, ycircle), 2) # Draw the checkpoint on the minimap, not implemented in this code snippet
        pygame.draw.line(screen, black, (lastx, lasty), (xcircle, ycircle), 1) # Draw a line from the current position of the track to the checkpoint on the minimap, not implemented in this code snippet
        lastx = xcircle # Update the last x coordinate for the next checkpoint, not implemented in this code snippet
        lasty = ycircle # Update the last y coordinate for the next checkpoint, not implemented in this code snippet
               
    pygame.draw.line(screen, black, (lastx, lasty), (sflinex, sfliney), 1)
    pygame.draw.circle(screen, red, (mpx/scale, (fvar-mpy)/scale), 2) # Draw the players position on the minimap, not implemented in this code snippet

def dcheckturn(playerRotation):
    '''
    @Summary:    Checks for mouse movement to determine if the player is turning and updates the player rotation variable accordingly
    @Parameters: playerRotation as integer, the current rotation of the player  
    @Returns:    Updated player rotation based on mouse movement
    '''
    # check for player direction 360 degrees using a to turn left d to turn right, not implemented in this code snippet
    if pygame.key.get_pressed()[pygame.K_a]:
        playerRotation = (playerRotation - 5) % 360 # Rotate left by 5 degrees, not implemented in this code snippet
    elif pygame.key.get_pressed()[pygame.K_d]:
        playerRotation = (playerRotation + 5) % 360 # Rotate right by 5 degrees, not implemented in this code snippet
        
    playerRotation=playerRotation % 360 # Ensure the player rotation stays within 0-359 degrees, not implemented in this code snippet
    return playerRotation

def movePlayer(speed, playerRotation, mpx, mpy):
    '''
    @Summary:    Updates the player's position based on speed and rotation
    @Parameters: speed as integer, the current speed of the player  
                 playerRotation as integer, the current rotation of the player in degrees
                 mpx as integer, the current x coordinate of the player
                 mpy as integer, the current y coordinate of the player, not implemented in this code snippet
    @Returns:    Updated player position based on speed and rotation, not implemented in this code snippet
    '''
    mpx = mpx + math.cos(math.radians(playerRotation)) * speed * 0.1 # Update the x coordinate of the player based on speed and rotation, not implemented in this code snippet
    mpy = mpy - math.sin(math.radians(playerRotation)) * speed * 0.1 # Update the y coordinate of the player, remember y inverted for easier math with the track coordinates, adjust as needed, not implemented in this code snippet
    return mpx, mpy
    
def showtrackvsplayer(mpx, mpy, checkpoints):
    '''
    @Summary:    Shows the track and player on the screen, not implemented in this code snippet
    @Parameters: mpx as integer, the current x coordinate of the player  
                 mpy as integer, the current y coordinate of the player 
                 checkpoints as list of tuples, the x and y coordinates of the checkpoints to be drawn
    @Returns:    None, but shows the track and player on the screen, not implemented in this code snippet
    '''
    # player position on main map does not change, screen size is 600 x 600only the track and checkpoints move based on the player's position
    x = 300 # x coordinate of the player on the screen, not implemented in this code snippet
    y = 550 # y coordinate of the player on the screen, not implemented in this code snippet, y in realitiy is 600-50 for easier math with the track coordinates, adjust as needed
    lastx = (checkpoints[18][0])
    lasty = (10000-checkpoints[18][1]) - (10000-mpy) + y # Calculate the y coordinate of the last checkpoint drawn on the screen based on the player's position, not implemented in this code snippet
    for checkpoint in checkpoints:
        # check if track or checkpoint is within the screen bounds before drawing
        xcheck = checkpoint[0] - mpx + x # Calculate the x coordinate of the checkpoint on the screen based on the player's position, not implemented in this code snippet
        ycheck = (10000-checkpoint[1]) - (10000-mpy) + y # Calculate the y coordinate of the checkpoint on the screen based on the player's position, not implemented in this code snippet
        if 0 <= xcheck <= 600 and 0 <= ycheck <= 600: # Check if the checkpoint is within the screen bounds, not implemented in this code snippet
            pygame.draw.circle(screen, black, (xcheck, ycheck), 75) # Draw the checkpoint on the screen, not implemented in this code snippet
        
        # don't draw a line from the last checkpoint to the first checkpoint, as it will be drawn at the end of the loop, but still draw line to first checkpoint
        if checkpoint != checkpoints[0]: # Check if the checkpoint is not the first checkpoint, not implemented in this code snippet    
            pygame.draw.line(screen, black, (lastx, lasty), (xcheck, ycheck), 5) # Draw a line from the current position of the track to the checkpoint on the screen, not implemented in this code snippet
        lastx = xcheck # Update the last x coordinate for the next checkpoint, not implemented in this code snippet
        lasty = ycheck # Update the last y coordinate for the next checkpoint, not implemented in this code snippet
    # Draw a line from the last checkpoint to the start/finish line on the screen, not implemented in this code snippet
    sflinex = (checkpoints[0][0]) - mpx + x # Calculate the x coordinate of the start/finish line on the screen based on the player's position, not implemented in this code snippet
    sfliney = ((10000-checkpoints[0][1]) - (10000-mpy) + y) # Calculate the y coordinate of the start/finish line on the screen based on the player's position, not implemented in this code snippet
    pygame.draw.line(screen, black, (lastx, lasty), (sflinex, sfliney), 5) # Draw a line from the last checkpoint to the start/finish line on the screen, not implemented in this code snippet
                                                 
def main(speed, acceleration):
    '''
    @Summary:    Main game loop that handles events, updates the game state, and renders the graphics
    @Parameters: speed as integer, the initial speed of the player  
                 acceleration as integer, the initial acceleration of the player
    @Returns:    None, but continuously updates the game state and renders the graphics until the game is quit
    '''    
    global mpx, mpy, checkpoints, playerRotation
    while True:
        screen.fill(background)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
          
        # Get mouse input for acceleration
        acceleration = m_acceleration(acceleration, speed)
        # Calculate the new speed based on acceleration
        speed = speed + acceleration
        # Dispaly the Speed of the player
        sSpeed(speed) 
        # Update the player rotation based on keyboard input
        playerRotation = dcheckturn(playerRotation) 
        mpx, mpy = movePlayer(speed, playerRotation, mpx, mpy) # Update the player's position based on speed and rotation, not implemented in this code snippet
        # Draw the minimap with checkpoints
        dcheckpoint(mpx, mpy, checkpoints)   
        showtrackvsplayer(mpx, mpy, checkpoints) # Show the track and player on the screen, not implemented in this code snippet 
        # Draw the player on the screen in dafault rotation
        dPlayer(300, 514,playerRotation) # Draw the player on the screen at the specified position and rotation, not implemented in this code snippet
        # Update the display and control the frame rate
        pygame.display.flip()
        clock.tick(30) 
              
# Run the game
main(speed, acceleration)
