import sys
import pygame
import random

from time import sleep
from bullet import Bullet
from alien import Alien
from alien_bullet import Alien_Bullet


def update_screen(ai_settings, screen, ship, bullets, alien_bullets, aliens, stats, menu, play_button, sb):
    """Update images on the screen and flip to the new screen"""
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for bullet in alien_bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        menu.draw_menu()
        play_button.draw_button()

    pygame.display.flip()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Responds to key presses"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_f:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_s:
        # Move the ship to the right
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        # Create a new bullet and add it to the bullets group
        fire_bullet(ai_settings=ai_settings, screen=screen, ship=ship, bullets=bullets)

    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Responds to key releases"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_f:
        ship.moving_right = False
    if event.key == pygame.K_LEFT or event.key == pygame.K_s:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb):
    """Respond to key presses and mouse events"""
    # Get keyboard and mouse movements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats=stats, play_button=play_button, mouse_x=mouse_x, mouse_y=mouse_y,
                              ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens, bullets=bullets, sb=sb)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event=event, ai_settings=ai_settings, screen=screen, ship=ship, bullets=bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event=event, ship=ship)


def update_bullets(ai_settings, screen, ship, aliens, bullets, alien_bullets, sb, stats):
    """Update position of bullets and get rid of old bullets"""
    # Update bullet positions
    bullets.update()
    alien_bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Get rid of alien bullets that have disappeared
    for bullet in alien_bullets.copy():
        if bullet.rect.top >= ai_settings.screen_height:
            alien_bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens, bullets=bullets,
                                  sb=sb, stats=stats)
    check_bullet_ship_collision(ai_settings=ai_settings, screen=screen, ship=ship, alien_bullets=alien_bullets, sb=sb, stats=stats, aliens=aliens, bullets=bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, sb, stats):
    # check if any bullets have hit aliens
    # if so, remove bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                stats.score += alien.score_value
                alien.boom()
            sb.prep_score()
        check_high_score(stats=stats, sb=sb)

    if len(aliens) == 0:
        # if the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings=ai_settings, screen=screen, ship=ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, aliens, ship):
    """Create a fleet of aliens"""
    """Create an alien and find the number of aliens in a row, where the spacing between each alien is one alien width"""
    alien = Alien(ai_settings=ai_settings, screen=screen, row_number=0)
    number_aliens_x = get_number_aliens_x(ai_settings=ai_settings, alien_width=alien.rect.width)
    number_rows = get_number_rows(ai_settings=ai_settings, ship_height=ship.rect.height, alien_height=alien.rect.height)

    # Create the fleet
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings=ai_settings, screen=screen, aliens=aliens, alien_number=alien_number,
                         row_number=row_number)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    alien = Alien(ai_settings=ai_settings, screen=screen, row_number=row_number % 3)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fir on the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_settings, stats, screen, bullets, aliens, ship, sb, alien_bullets):
    """Update the positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings=ai_settings, aliens=aliens)
    aliens.update()

    if (pygame.time.get_ticks() % (2 ** ai_settings.fire_frequency)) == 0:
        random.choice(aliens.sprites()).fire_bullet(alien_bullets)

    # Check for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings=ai_settings, stats=stats, screen=screen, ship=ship, aliens=aliens, bullets=bullets, sb=sb)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings=ai_settings, stats=stats, screen=screen, ship=ship, aliens=aliens, bullets=bullets,
                        sb=sb)


def check_fleet_edges(ai_settings, aliens):
    """Respond to aliens reaching an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings=ai_settings, aliens=aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the fleet down and change its direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb, alien_bullets):
    """Respond to ship being hit by alien"""
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings=ai_settings, stats=stats, screen=screen, ship=ship, aliens=aliens, bullets=bullets,
                     sb=sb)
            break


def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, sb):
    """Start a new game when the player clicks Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game settings
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens)
        ship.center_ship()

        # Play the music
        pygame.mixer.music.play(loops=-1)


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_ship_collision(ai_settings, screen, ship, alien_bullets, sb, stats, aliens, bullets):
    collisions = pygame.sprite.spritecollide(ship, alien_bullets, True)
    if len(collisions) > 0:
        ship_hit(ai_settings=ai_settings, stats=stats, screen=screen, ship=ship, aliens=aliens, bullets=bullets, sb=sb, alien_bullets=alien_bullets)
