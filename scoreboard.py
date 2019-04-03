#! python3
# Created by Sny on 2019-03-31
# The Score class

import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """ A class for display score """
    def __init__(self, ai_settings, stats, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.ai_settings = ai_settings

        # Setting for font of score
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Initialize the score
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    
    def prep_score(self):
        # Render a score image
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
            self.ai_settings.bg_color)
        
        # Put the image in the right up corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_high_score(self):
        # Render the highest score
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color, self.ai_settings.bg_color)
        
        # Set this in the center top of screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    
    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True,
            self.text_color, self.ai_settings.bg_color)
        
        # Set the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        # Show the remain ships
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)