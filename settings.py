class Settings:
    """A class to store all settings for Alien Invastion"""

    def __init__(self):
        """Initialize the game's settings"""

        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 0, 0)

        # Scoreboard settings
        self.score_text_color = (255, 255, 255)

        # Ship settings
        self.ship_speed_factor = 3
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 15
        self.bullet_height = 30
        self.bullet_color = 255, 255, 255
        self.bullets_allowed = 10

        # Alien settings
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 10
        self.alien_bullet_speed_factor = 1
        self.fire_frequency = 10
        """fleet_direction
        1 = right
        -1 = left"""
        self.fleet_direction = 1
        self.alien_points = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed_factor = 3
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.5
        self.fire_frequency = 10

        """fleet_direction
        1 = right
        -1 = left"""
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        if self.fire_frequency >= 1:
            self.fire_frequency -= 1

        self.alien_points = int(self.alien_points * self.score_scale)
