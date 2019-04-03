#! python3
# Created by Sny on 2019-03-31
# Settings of the game

class Settings():
    """ The class stores the all settings of this game """

    def __init__(self):
        """ Parameters for settings of the game """
        # Settings for screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Settings for ship
        self.ship_limit = 3

        # Settings for bullet
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # Settings for alien
        self.fleet_drop_speed = 10

        # Dynamic settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        # Data filename
        self.filename = "game_data.json"
    
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # -1 means left, 1 means right
        self.fleet_direction = 1

        # Score
        self.alien_points = 50
    
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)