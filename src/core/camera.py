import pygame
from config import config

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.min_y = 0  # Minimum y position (top of level)
        self.max_y = height - config.WINDOW_HEIGHT  # Maximum y position (bottom of level)

    def apply(self, entity):
        if isinstance(entity, pygame.Rect):
            return pygame.Rect(entity.x - self.camera.x,
                             entity.y - self.camera.y,
                             entity.width,
                             entity.height)
        return pygame.Rect(entity.rect.x - self.camera.x,
                         entity.rect.y - self.camera.y,
                         entity.rect.width,
                         entity.rect.height)

    def update(self, target):
        # Calculate x position (horizontal scrolling remains the same)
        x = -target.rect.centerx + config.WINDOW_WIDTH // 2
        x = min(0, x)
        x = max(-(self.width - config.WINDOW_WIDTH), x)
        
        # Calculate y position (only follow player up to level bottom)
        y = -target.rect.centery + config.WINDOW_HEIGHT // 2
        y = min(0, y)  # Don't show above top of level
        y = max(-(self.max_y), y)  # Don't show below bottom of level
        
        self.camera.x = -x
        self.camera.y = -y