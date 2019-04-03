#! python3
# Created by Sny on 2019-03-31
# The GameStats class

import json

class GameStats():
    """ Trace the status of game """
    def __init__(self, ai_setting):
        self.ai_setting = ai_setting
        self.reset_stats()
        self.game_active = False

        # Initialize highest score
        self.load_data(ai_setting.filename)
    
    def reset_stats(self):
        self.ships_left = self.ai_setting.ship_limit
        self.score = 0
        self.level = 1
    
    def load_data(self, filename):
        try:
            with open(filename) as file_obj:
                self.high_score = json.load(file_obj)
        except FileNotFoundError:
            self.high_score = 0

    def save_data(self, filename):
        with open(filename, 'w') as file_obj:
            json.dump(self.high_score, file_obj)