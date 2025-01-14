import math
import pygame

class FloatingAnimation:
    def __init__(self, amplitude=1, speed=0.0001):
        self.game_object = None
        self.amplitude = amplitude
        self.speed = speed

    def update(self):
        offset = math.sin(pygame.time.get_ticks() * self.speed) * self.amplitude
        self.game_object.rect.y = self.game_object.original_y + offset

class PulsingAnimation:
    def __init__(self, scale_range=0.15, speed=0.003):
        self.game_object = None
        self.scale_range = scale_range
        self.speed = speed
        self.original_size = None

    def update(self):
        if self.original_size is None:
            self.original_size = (self.game_object.rect.width, self.game_object.rect.height)
        
        scale = 1 + math.sin(pygame.time.get_ticks() * self.speed) * self.scale_range
        center = self.game_object.rect.center
        self.game_object.rect.width = int(self.original_size[0] * scale)
        self.game_object.rect.height = int(self.original_size[1] * scale)
        self.game_object.rect.center = center