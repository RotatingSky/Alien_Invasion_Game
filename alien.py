#! python3
# Created by Sny on 2019-03-31
# The Alien class

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ A class for an alien """
    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load image of alien
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Set the position of the alien
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Store the float position of the alien
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor *
            self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """ Draw the alien in the given position """
        self.screen.blit(self.image, self.rect)