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
       
def main(speed, acceleration):
    '''
    @Summary: Main game loop, handles events, updates the game state, and renders the game
    @Parameters: speed as integer, the speed of the player  
                 acceleration as integer, the acceleration of the player
    @Returns: None 
    '''    
    while True:
        screen.fill(background)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        
        # Get mouse input for acceleration
        mouse = pygame.mouse.get_pressed() 
        if mouse[0] is True and speed>.9:           
            acceleration = -1    
        elif mouse[2] is True: 
            acceleration = 1
        else:
            acceleration = 0 
            
        # Calculate the new speed based on acceleration
        speed = speed + acceleration
        # Dispaly the Speed of the player
        sSpeed(speed) 
        # Draw the player on the screen
        dPlayer(300, 514) 
        # Update the display and control the frame rate
        pygame.display.flip()
        clock.tick(30) 
              
# Run the game
main(speed, acceleration)
