# Race verse self game, written by Sam Langhof Frederiksen, 2024-06-17

# Imports
import pygame
import sys
import math

# Initialization
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("pygame-ce test")

# Variables
clock = pygame.time.Clock()
white=pygame.Color(255, 255, 255)
black=pygame.Color(0, 0, 0)
red=pygame.Color(255, 0, 0)
background = pygame.Color(white)
acceleration = 0
speed = 0 # Initial speed of the player
mpx = 3333 # x position of the track, not implemented in this code snippet
mpy = 3300 # y position of the track, not implemented in this code snippet
checkpoints = [(3333,3333),(3333,5000),(1800,6000),(1000,7500),(2500,8500),(4000,8500),
               (5000,5500),(7500,5000),(6666,6666),(6000,8500),(8000,8800),(8250,6000),
               (7800,4000),(6000,3000),(7200,1800),(6666,900),(3333,700),(600,1500),(2700,2700)] # List of 19 checkpoints for the track for main map, not implemented in this code snippet
mainmapx = checkpoints[0][0] # x position of the start/finish line of the main map
mainmapy = checkpoints[0][1] # y position of the start/finish line of the main map

# Functions
def dPlayer(x,y):
    '''
    @Summary: Draws the player on the screen
    @Parameters: x as integer, centre x coordinate of the player
                 y as integer, centre y coordinate of the player
    @Returns: Three pixels that make up the player
                              .
                            .   .
    '''
    pygame.draw.circle(screen, red, (x,y-14), 5) # Draw the head of the player as a circle, not implemented in this code snippet
    pygame.draw.circle(screen, red, (x-20,y+14), 5) # Draw the left wheel of the player as a circle, not implemented in this code snippet
    pygame.draw.circle(screen, red, (x+20,y+14), 5) # Draw the right wheel of the player as a circle, not implemented in this code snippet
    
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
    pygame.draw.circle(screen, red, (mpx/scale, (fvar-mpy)/scale), 2) # Draw the start/finish line on the minimap, not implemented in this code snippet
       
def main(speed, acceleration):
    '''
    @Summary:    Main game loop that handles events, updates the game state, and renders the graphics
    @Parameters: speed as integer, the initial speed of the player  
                 acceleration as integer, the initial acceleration of the player
    @Returns:    None, but continuously updates the game state and renders the graphics until the game is quit
    '''    
    global mpx, mpy, checkpoints
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
        # Draw the minimap with checkpoints
        dcheckpoint(mpx, mpy, checkpoints)
        # Update the position of the player based on the speed (not implemented in this code snippet)       
        # Draw the player on the screen
        dPlayer(300, 514) 
        # Update the display and control the frame rate
        pygame.display.flip()
        clock.tick(30) 
              
# Run the game
main(speed, acceleration)
