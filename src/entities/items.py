import pygame
from physics.constants import pixels_to_meters
from .collectible import Collectible
from components.animations import FloatingAnimation, PulsingAnimation
from config import config

class Coin(Collectible):
    def __init__(self, x, y):
        super().__init__(x, y, 15, 15)
        self.color = (255, 215, 0)  # Gold color
        self.add_component('pulse', PulsingAnimation(scale_range=0.1, speed=0.003))

    def on_collect(self, player):
        self.audio_manager.play_sound('coin')
        player.collect_coin()

class JumpBoost(Collectible):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20)
        self.color = (0, 255, 255)
        self.boost_amount = 3
        self.duration = 50000
        self.end_time = 0
        self.add_component('float', FloatingAnimation(amplitude=4, speed=0.003))

    def on_collect(self, player):
        player.jump_force = pixels_to_meters(config.JUMP_FORCE) + self.boost_amount
        self.end_time = pygame.time.get_ticks() + self.duration
        self.audio_manager.play_sound("magic-boost")

    def update(self, player):
        super().update(player)
        #if self.collected and pygame.time.get_ticks() >= self.end_time:
            #player.jump_force = pixels_to_meters(config.JUMP_FORCE)
            #self.audio_manager.play_sound("expire")