#! python3
# Created by Sny on 2019-03-31
# The Ship class

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """ The class for ship """
    def __init__(self, ai_settings, screen):
        """ Initialize the ship and settings """
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load ship image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Put the ship in the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store float position
        self.center = float(self.rect.centerx)

        # Flags for moving
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def update(self):
        """ Adjust position of ship by flags """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        
        # Update rect object
        self.rect.centerx = self.center

    def blitme(self):
        """ Draw ship in the given position """
        self.screen.blit(self.image, self.rect)