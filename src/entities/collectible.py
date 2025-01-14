from abc import ABC, abstractmethod

import pygame
from core.game_object import GameObject
from config import config

class Collectible(GameObject, ABC):
    def __init__(self, x, y, width=20, height=20):
        super().__init__(None, x, y, width, height)
        self.collected = False
        self.color = config.WHITE

    @abstractmethod
    def on_collect(self, player):
        pass

    def update(self, player):
        super().update()
        if not self.collected and self.rect.colliderect(player.rect):
            self.on_collect(player)
            self.collected = True

    def draw(self, screen, camera):
        if not self.collected:
            pygame.draw.rect(screen, self.color, camera.apply(self))

    def on_collect(self, player):
        self.audio_manager.play_sound("collect")