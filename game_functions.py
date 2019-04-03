#! python3
# Created by Sny on 2019-03-31
# Refactoring module for the game

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def start_game(ai_settings, stats, screen, ship, bullets, aliens, sb):
    # Reset the settings of the game
    ai_settings.initialize_dynamic_settings()
    
    # Hidden the cursor
    pygame.mouse.set_visible(False)

    # Reset the stats of the game
    stats.reset_stats()
    stats.game_active = True
    
    # Reset the scoreboard
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Clear the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    # Create a new fleet of aliens
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def exit_game(ai_settings, stats):
    stats.save_data(ai_settings.filename)
    sys.exit()

def check_keydown_events(event, ai_settings, stats, screen, ship, bullets,
    aliens, sb):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        exit_game(ai_settings, stats)
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(ai_settings, stats, screen, ship, bullets, aliens, sb)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(ai_settings, stats, screen, ship, bullets, aliens,
    play_button, sb, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, stats, screen, ship, bullets, aliens, sb)

def check_events(ai_settings, stats, screen, ship, bullets, aliens,
    play_button, sb):
    """ Response to the keyboard and mouce """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game(ai_settings, stats)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, screen, ship,
                bullets, aliens, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, stats, screen, ship, bullets, aliens,
                play_button, sb, mouse_x, mouse_y)

def update_screen(ai_settings, stats, screen, ship, bullets, aliens,
    play_button, sb):
    """ Update image of screen """
    # Draw the screen
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Show score
    sb.show_score()

    # Draw button
    if not stats.game_active:
        play_button.draw_button()

    # Show the window
    pygame.display.flip()

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, stats, screen, ship, bullets,
    aliens, sb):
    # Remove the collised aliens and bullets
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for tempAliens in collisions.values():
            stats.score += ai_settings.alien_points * len(tempAliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        # Increase the level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)
    
    return collisions

def update_bullets(ai_settings, stats, screen, ship, bullets, aliens, sb):
    """ Update position of bullets """
    bullets.update()
    
    # Remove some bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, stats, screen, ship, bullets,
        aliens, sb)

def change_fleet_direction(ai_settings, aliens):
    """ Drop the fleet and change the direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def ship_hit(ai_settings, stats, screen, ship, bullets, aliens, sb):
    if stats.ships_left > 0:
        # ship_left minus 1
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Clear the list of aliens and list of bullets
        aliens.empty()
        bullets.empty()

        # Create new groups of aliens and bullets
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, bullets, aliens, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, bullets, aliens, sb)
            break

def update_aliens(ai_settings, stats, screen, ship, bullets, aliens, sb):
    """ Update position of aliens """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, bullets, aliens, sb)
    
    check_aliens_bottom(ai_settings, stats, screen, ship, bullets, aliens, sb)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_aliens_y(ai_settings, alien_height, ship_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height)
        - ship_height)
    number_alien_y = int(available_space_y / (2 * alien_height))
    return number_alien_y

def create_alien(ai_settings, screen, aliens, alien_number_x, alien_number_y):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number_x
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * alien_number_y
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """ Create a group of aliens """
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_alien_y = get_number_aliens_y(ai_settings, alien.rect.height,
        ship.rect.height)

    for alien_number_y in range(number_alien_y):
        for alien_number_x in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number_x,
                alien_number_y)