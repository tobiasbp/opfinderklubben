#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Starfield demo

Based on:
http://programarcadegames.com/python_examples/show_file.php?file=moving_sprites.py
"""
# Desired framerate in frames per second. Try out other values.              
FPS = 30

PLAYER_ROT_SPEED = 6
PLAYER_ACCELERATION = 1

#the next line is only needed for python2.x and not necessary for python3.x
#from __future__ import print_function, division
import pygame
import random
from math import cos, sin, radians

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Size of the screen/window
screen_width = 600
screen_height = 600

# Initialize Pygame.
pygame.init()

# Create window/display/screen.
screen = pygame.display.set_mode((screen_width,screen_height))

# A class (from Sprite) representing the background stars in the starfield
class Star(pygame.sprite.Sprite):
    """
    This class represents a star
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, size):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Set layer
        self._layer = size
        
        # Create an empty image (surface). Needed by PyGame.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([size, size])
        
        # Unlikely color is transparent background
        self.image.fill([1,2,3])
        self.image.set_colorkey([1,2,3])
        
        # The intensity of the color of the star is based on it's size
        i = min(255, (255/size*10))
        
        # Draw an ellipse (The star)
        pygame.draw.ellipse(self.image, [i, i, i], [0, 0, size, size]) 
                
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        # Needed by PyGame
        self.rect = self.image.get_rect()
        
        # Store stars position as a float
        self.pos_x = 0.0
        self.pos_y = 0.0
        
        # Speed based on size. Smaller star is slower
        self.speed = size/100
        
        
    def update(self):
        """ Move star """
        
        # Update position (float)
        # Subtract as stars move opposite to player
        self.pos_x -= player['dx'] * self.speed
        self.pos_y -= player['dy'] * self.speed
        
        # Move to the updated position (integer)
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        
        # Wrap around screen edges
        if self.pos_x < 0:
            self.pos_x =+ screen_width
        if self.pos_x > screen_width:
            self.pos_x = 0
        if self.rect.y < 0:
            self.pos_y =+ screen_height
        if self.rect.y > screen_height:
            #self.pos_y =- screen_height
            self.pos_y = 0
 

class Player(pygame.sprite.Sprite):
    """
    This class represents a player
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, size=40):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Set layer
        self._layer = 100
        
        # Create an empty image (surface). Needed by PyGame.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([size, size])
        
        # Unlikely color is transparent background
        self.image.fill([1,2,3])
        self.image.set_colorkey([1,2,3])
        
        # Draw space ship
        pygame.draw.polygon(self.image, WHITE, ((size,size/2),(0,3*size/4),(0,size/4))) 

        # Save original image as rotation is destructive
        self.image_orig = self.image
                
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        # Needed by PyGame
        self.rect = self.image.get_rect()
        
        self.rect.center = (screen_width/2, screen_height/2)
        
    def update(self):
        """ Move star """
        # Rotated copies of image and rect
        self.rot_image = pygame.transform.rotate(self.image_orig, -player['dir'])
        self.rot_rect = self.rot_image.get_rect(center=self.rect.center)
        # Update sprite to new rotated image & rect
        self.image = self.rot_image
        self.rect = self.rot_rect
        
        

 
# This is a list of 'sprites.' Each star in the program is
# added to this list. The list is managed by a class called 'Group.'
#star_group = pygame.sprite.Group()
star_group = pygame.sprite.LayeredUpdates()

# Add stars to list
for i in range(50):
    # This represents a star
    star = Star(random.randrange(5,40))
 
    # Set a random location for the star
    star.pos_x = random.randrange(screen_width)
    star.pos_y = random.randrange(screen_height)
 
    # Add the star to the list of stars
    star_group.add(star)
    
player_group = pygame.sprite.LayeredUpdates()
player_group.add(Player())

# Create Pygame clock object.  
clock = pygame.time.Clock()

mainloop = True

# How many seconds the "game" is played.
playtime = 0.0


player = {'dir': 0, 'speed': 8.0, 'dx': 0.0, 'dy': 0.0}
 
while mainloop:
    # Do not go faster than this framerate.
    milliseconds = clock.tick(FPS)  
    playtime += milliseconds / 1000.0 
    
    # Process events
    for event in pygame.event.get():
    
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False 
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                mainloop = False
                            
    # Get pressed/held status of all keys        
    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_LEFT]:
        player['dir'] -= PLAYER_ROT_SPEED
    if pressed[pygame.K_RIGHT]:
        player['dir'] += PLAYER_ROT_SPEED
    if pressed[pygame.K_UP]:
        player['speed'] += PLAYER_ACCELERATION
    if pressed[pygame.K_DOWN]:
        player['speed'] -= PLAYER_ACCELERATION
        
    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)
    
    # How far did player move
    player['dx'] = cos(radians(player['dir'])) * player['speed']
    player['dy'] = sin(radians(player['dir'])) * player['speed']
    
    # Clear screen (paint)
    screen.fill(BLACK)
    
    # Update sprites
    star_group.update()
    player_group.update()
    
    # Draw all sprites on the surface screen 
    star_group.draw(screen)
    player_group.draw(screen)
    
   
    
    #Update Pygame display.
    pygame.display.flip()

# Finish Pygame.  
pygame.quit()

# At the very last:
print("This game was played for {0:.2f} seconds".format(playtime))

