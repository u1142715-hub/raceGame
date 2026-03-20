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
background = pygame.Color(white)
acceleration = 0
speed = 0
mp = 450

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
    screen.set_at((x, y-14), (black))  
    screen.set_at((x-20, y+14), (black))  
    screen.set_at((x+20, y+14), (black)) 
    
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

def dmap(speed,mp):
    '''
    @Summary: Draws the track on the screen (not implemented in this code snippet)
    @Parameters: None
    @Returns: None
    '''
    # draw start finish line
    mp = mp + (speed * 0.1)  # Adjust the multiplier as needed
    print(speed, mp)
    if mp > 600:
        mp = mp - 600
    return mp
       
def main(speed, acceleration):
    '''
    @Summary: Main game loop, handles events, updates the game state, and renders the game
    @Parameters: speed as integer, the speed of the player  
                 acceleration as integer, the acceleration of the player
    @Returns: None 
    '''    
    global mp
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
        # Draw the track (not implemented in this code snippet)
        mp = dmap(speed, mp) 
        # Update the position of the player based on the speed (not implemented in this code snippet)       
        # Draw the player on the screen
        dPlayer(300, 514) 
        # Update the display and control the frame rate
        pygame.draw.line(screen, black, (250, mp), (350, mp), 3)
        pygame.draw.line(screen, black, (300, 0), (300, 600), 2) 
        pygame.display.flip()
        clock.tick(30) 
              
# Run the game
main(speed, acceleration)
