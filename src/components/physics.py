import pygame
from config import config

class PhysicsComponent:
    def __init__(self, game_object, gravity=config.GRAVITY, 
                 terminal_velocity=config.TERMINAL_VELOCITY):
        self.game_object = game_object
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = gravity
        self.terminal_velocity = terminal_velocity
        self.on_ground = False

    def apply_gravity(self):
        self.vel_y = min(self.vel_y + self.gravity, self.terminal_velocity)

    def update(self, platforms):
        # Store original position for collision resolution
        original_x = self.game_object.rect.x
        original_y = self.game_object.rect.y

        # Apply horizontal movement
        self.game_object.rect.x += self.vel_x

        # Check level boundaries - horizontal
        if self.game_object.rect.left < 0:
            self.game_object.rect.left = 0
        elif self.game_object.rect.right > config.LEVEL_WIDTH:
            self.game_object.rect.right = config.LEVEL_WIDTH

        # Check horizontal collisions
        for platform in platforms:
            if self.game_object.rect.colliderect(platform):
                if self.vel_x > 0:
                    self.game_object.rect.right = platform.left
                elif self.vel_x < 0:
                    self.game_object.rect.left = platform.right

        # Apply vertical movement
        self.apply_gravity()
        self.game_object.rect.y += self.vel_y

        # Check level boundaries - vertical
        if self.game_object.rect.top < 0:
            self.game_object.rect.top = 0
            self.vel_y = 0

        # Check vertical collisions
        self.on_ground = False
        for platform in platforms:
            if self.game_object.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.game_object.rect.bottom = platform.top
                    self.on_ground = True
                    self.vel_y = 0
                elif self.vel_y < 0:
                    self.game_object.rect.top = platform.bottom
                    self.vel_y = 0

    def jump(self, force):
        if self.on_ground:
            self.vel_y = force
            return True
        return False