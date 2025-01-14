import pygame
from config import config

class GameUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)  # Default pygame font, size 36
        self.coin_count = 0
        
        # Position for coin counter (top-left corner with padding)
        self.coin_counter_pos = (20, 20)
        
        # Colors
        self.text_color = config.WHITE
        self.shadow_color = config.BLACK
        
        # Pause overlay setup
        self.pause_font = pygame.font.Font(None, 72)  # Larger font for pause text
        self.pause_surface = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self.pause_surface.fill(config.BLACK)
        self.pause_surface.set_alpha(76)  # 30% opacity (76 is ~30% of 255)
        
        # Create pause text
        self.pause_text = self.pause_font.render("PAUSED", True, config.WHITE)
        self.pause_text_rect = self.pause_text.get_rect(
            center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2)
        )
        
    def update_coin_count(self, count):
        self.coin_count = count
        
    def draw(self, screen, is_paused=False):
        # Draw coin counter with shadow effect
        coin_text = f"Coins: {self.coin_count}"
        
        # Draw shadow
        shadow_surface = self.font.render(coin_text, True, self.shadow_color)
        screen.blit(shadow_surface, (self.coin_counter_pos[0] + 2, self.coin_counter_pos[1] + 2))
        
        # Draw text
        text_surface = self.font.render(coin_text, True, self.text_color)
        screen.blit(text_surface, self.coin_counter_pos)
        
        # Draw pause overlay if game is paused
        if is_paused:
            screen.blit(self.pause_surface, (0, 0))
            screen.blit(self.pause_text, self.pause_text_rect)