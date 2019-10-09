import pygame
from pygame.sprite import Sprite
from frame_timer import Timer


class Alien(Sprite):
    """A class to represent single alien in the fleet"""

    def __init__(self, ai_settings, screen, row_number):
        """Initialize the alien and set its starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Set alien type
        self.alien_type = row_number

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien{}/alien{}0.png'.format(self.alien_type, self.alien_type))
        self.rect = self.image.get_rect()
        self.frames = [pygame.image.load('images/alien{}/alien{}{}.png'.format(self.alien_type, self.alien_type,i)) for i in range(0,2)]
        self.timer = Timer(self.frames)

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)


    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.image = self.timer.imagerect()

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
