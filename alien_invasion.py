#! python3
# Created by Sny on 2019-03-31
# Create a window of the game

import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
    # Initialization of the game
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create Play button
    play_button = Button(ai_settings, screen, "Play")

    # Create a ship
    ship = Ship(ai_settings, screen)
    # Create a group of bullets
    bullets = Group()
    # Create a group of aliens
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Record the stats of the game
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, stats, screen)

    # Main loop
    while True:
        gf.check_events(ai_settings, stats, screen, ship, bullets, aliens,
            play_button, sb)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, stats, screen, ship, bullets,
                aliens, sb)
            gf.update_aliens(ai_settings, stats, screen, ship, bullets, aliens,
                sb)
        
        gf.update_screen(ai_settings, stats, screen, ship, bullets, aliens,
            play_button, sb)

if __name__ == '__main__':
    run_game()