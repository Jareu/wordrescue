from typing import Protocol

from core.game_object import GameObject

class Component(Protocol):
    game_object: 'GameObject'

    def update(self):
        pass