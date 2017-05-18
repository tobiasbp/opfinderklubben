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
PLAYER_MAX_SPEED = 40
PLAYER_MIN_SPEED = -1 * PLAYER_MAX_SPEED

#the next line is only needed for python2.x and not necessary for python3.x
#from __future__ import print_function, division
import pygame
import random
#from math import cos, sin, radians, sqrt
import math

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
        """ Constructor. Pass in the size of the star """
        
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.size = size
        
        # Set layer
        self._layer = self.size
        
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
        self.pos_x = random.randrange(screen_width)
        self.pos_y = random.randrange(screen_height)
        
        # Speed based on size. Smaller star is slower
        self.speed = size/100
        
    def update(self):
        """ Move star """
        
        # Update position (float)
        # Subtract as stars move opposite to player
        self.pos_x -= player['dx'] * self.speed
        self.pos_y -= player['dy'] * self.speed
        
        # Move to the updated position (integer)
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y
        
        # Wrap around screen edges as new random star (with same size)
        if self.rect.right < 0:
            self.pos_x =+ screen_width
            self.pos_y = random.randrange(screen_height)
        if self.rect.left > screen_width:
            self.pos_x = 0
            self.pos_y = random.randrange(screen_height)
        if self.rect.centery < 0:
            self.pos_y =+ screen_height
            self.pos_x = random.randrange(screen_width)
        if self.rect.centery > screen_height:
            #self.pos_y =- screen_height
            self.pos_y = 0
            self.pos_x = random.randrange(screen_width)
 

class Player(pygame.sprite.Sprite):
    """
    This class represents a player
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, size=40):
        """ Constructor. Optionally pass in the 
        size of the player. """
        
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
        """ Move player """
        # Get pressed/held status of all keys        
        pressed = pygame.key.get_pressed()
    
        # Check for keys
        if pressed[pygame.K_LEFT]:
            player['dir'] -= PLAYER_ROT_SPEED
        if pressed[pygame.K_RIGHT]:
            player['dir'] += PLAYER_ROT_SPEED
        if pressed[pygame.K_UP] :
            player['speed'] += PLAYER_ACCELERATION
        if pressed[pygame.K_DOWN]:
            player['speed'] -= PLAYER_ACCELERATION
        if pressed[pygame.K_SPACE]:
            bullet_group.add(Bullet(self.rect.center))
        
        # Enforce speeds
        if player['speed'] > PLAYER_MAX_SPEED:
            player['speed'] = PLAYER_MAX_SPEED
        if player['speed'] < PLAYER_MIN_SPEED:
            player['speed'] = PLAYER_MIN_SPEED
            
        # Rotated copies of image and rect
        self.rot_image = pygame.transform.rotate(self.image_orig, -player['dir'])
        self.rot_rect = self.rot_image.get_rect(center=self.rect.center)
        # Update sprite to new rotated image & rect
        self.image = self.rot_image
        self.rect = self.rot_rect
        
class Bullet(pygame.sprite.Sprite):
    """
    This class represents a bullet
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, center, speed=2.0, bullet_range=screen_height/2, size=5, layer=100):
        """ Constructor. Optionally pass in the size
        of the bullet and the layer """
        
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Set layer. Nice to be on the same layer as the one shooting
        self._layer = layer

        # My center as floats
        self.centerx = center[0]
        self.centery = center[1]
        
        # Time To Live (Bullet will die when travveled this far)
        self.bullet_range = bullet_range
        
        # How far have I traveled
        self.dist = 0.0
        
        # Speed of bullet 
        self.speedx = math.cos(math.radians(player['dir'])) * speed
        self.speedy = math.sin(math.radians(player['dir'])) * speed
        
        # This is the speed the bullet inherits from the player
        self.start_speedx = player['dx'] 
        self.start_speedy = player['dy'] 
        
        # Create an empty image (surface). Needed by PyGame.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([size, size])
        
        # Unlikely color is transparent background
        self.image.fill([1,2,3])
        self.image.set_colorkey([1,2,3])
        
        # Draw space ship
        pygame.draw.ellipse(self.image, RED, [0,0,size,size]) 
                
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        
        # Set initial position on screen
        self.rect.center = (self.centerx, self.centery)
               
    def update(self):
        """ Move bullet """
        # Move bullet in relation to the player (The "camera")
        # That is, this is ignoring the bullets own speed
        self.centerx -= player['dx']
        self.centery -= player['dy']

        # Move bullet based on own speeds
        self.centerx += self.speedx + self.start_speedx
        self.centery += self.speedy + self.start_speedy

        # Update position of bullet graphic
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        # Calculate how far bullet has traveled (Self propelled)
        self.dist += math.sqrt(self.speedx**2 + self.speedy**2)

        # Remeove bullet when traveled max distance
        if self.dist > self.bullet_range:
            self.kill()

# This is a list of 'sprites.' Each star in the program is
# added to this list. The list is managed by a class called 'Group.'
#star_group = pygame.sprite.Group()
star_group = pygame.sprite.LayeredUpdates()

# Add stars to group
for i in range(50):
    # This represents a star
    star = Star(random.randrange(5,40))
 
    # Set a random location for the star
    #star.pos_x = random.randrange(screen_width)
    #star.pos_y = random.randrange(screen_height)
 
    # Add the star to the list of stars
    star_group.add(star)
    
player_group = pygame.sprite.LayeredUpdates()
player_group.add(Player())

# Bullets will add themselves to this group when fired
bullet_group = pygame.sprite.LayeredUpdates()

# Create Pygame clock object.  
clock = pygame.time.Clock()

mainloop = True

# How many seconds the "game" is played.
playtime = 0.0

# FIXME: This needs to be in the object!
player = {'dir': 0, 'speed': 0.0, 'dx': 0.0, 'dy': 0.0}
 
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
                            
        
    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)
    
    # How far did player move
    player['dx'] = math.cos(math.radians(player['dir'])) * player['speed']
    player['dy'] = math.sin(math.radians(player['dir'])) * player['speed']
    
    # Clear screen (paint)
    screen.fill(BLACK)
    
    # Update sprites
    player_group.update()
    star_group.update()
    bullet_group.update()
    
    # Draw all sprites on the surface screen 
    star_group.draw(screen)
    player_group.draw(screen)
    bullet_group.draw(screen)
    
   
    
    #Update Pygame display.
    pygame.display.flip()

# Finish Pygame.  
pygame.quit()

# At the very last:
print("This game was played for {0:.2f} seconds".format(playtime))

