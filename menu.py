import pygame.font


class Menu:

    def __init__(self, screen, play_button, is_start):
        """Initialize menu attributes"""

        # Set dimensions of the menu
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 500, 500
        self.menu_color = (0, 0, 0)
        self.text_color = (0, 255, 0)
        self.font = pygame.font.SysFont(None, 80)
        self.border_color = (0, 255, 0)

        # Build the menu's rect and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

        # prep title
        self.title_image = None
        self.title_image_rect = None

        # prep button
        self.play_button = play_button

        self.prep_menu(self.play_button, is_start)

    def prep_menu(self, play_button, is_start):
        if is_start:
            self.title_image = self.font.render("Space Invaders", True, self.text_color, self.menu_color)
            self.title_image_rect = self.title_image.get_rect()
            self.title_image_rect.center = (self.rect.centerx, self.rect.centery - 100)

    def draw_menu(self):
        """Draw blank menu, then draw contents"""
        self.screen.fill(self.menu_color, self.rect)
        pygame.draw.rect(self.screen, self.border_color, self.rect, 5)
        self.screen.blit(self.title_image, self.title_image_rect)

        self.play_button.draw_button()
