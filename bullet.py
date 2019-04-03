#! python3
# Created by Sny on 2019-03-31
# The Bullet class

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ A class for bullet management """
    def __init__(self, ai_settings, screen, ship):
        """ Create a bullet object in the position of the ship """
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a rectangle of bullet
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the float position of bullet
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
    
    def update(self):
        """ Move uptowards """
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw bullet on the screen """
        pygame.draw.rect(self.screen, self.color, self.rect)