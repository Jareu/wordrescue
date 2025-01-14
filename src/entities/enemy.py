from abc import ABC, abstractmethod
import pygame
import math
import Box2D as b2
from core.game_object import GameObject
from physics.constants import *
from config import config

class EnemyStrategy(ABC):
    @abstractmethod
    def update(self, enemy, player):
        """Update enemy behavior based on player position"""
        pass

class IdleStrategy(EnemyStrategy):
    def update(self, enemy, player):
        """Default behavior when player is not in range"""
        enemy.body.linearVelocity = (0, enemy.body.linearVelocity.y)

class ChaseStrategy(EnemyStrategy):
    def __init__(self, speed):
        self.speed = speed  # Speed in meters/second

    def update(self, enemy, player):
        """Move towards player using Box2D velocity"""
        dx = player.body.position.x - enemy.body.position.x
        
        # Determine direction (-1 for left, 1 for right)
        direction = 1 if dx > 0 else -1
        
        # Set velocity directly like player movement
        velocity = enemy.body.linearVelocity
        desired_velocity = self.speed * direction
        
        # Update velocity while maintaining vertical speed
        enemy.body.linearVelocity = (desired_velocity, velocity.y)

class PatrolStrategy(EnemyStrategy):
    def __init__(self, speed, patrol_distance):
        self.speed = speed  # Speed in m/s
        self.patrol_distance = pixels_to_meters(patrol_distance)
        self.direction = 1

    def update(self, enemy, player):
        """Move back and forth using Box2D velocity"""
        current_pos = enemy.body.position.x
        spawn_pos = pixels_to_meters(enemy.spawn_x)
        
        if abs(current_pos - spawn_pos) > self.patrol_distance:
            self.direction *= -1
        
        velocity = enemy.body.linearVelocity
        desired_velocity = self.speed * self.direction
        
        # Update velocity while maintaining vertical speed
        enemy.body.linearVelocity = (desired_velocity, velocity.y)

class Enemy(GameObject):
    def __init__(self, physics_world, x, y, width, height, color, detection_radius):
        super().__init__(physics_world, x, y, width, height)
        self.color = color
        self.detection_radius = detection_radius
        self.spawn_x = x
        self.spawn_y = y
        
        # Set up physics properties
        self.body.fixedRotation = True  # Prevent rotation
        for fixture in self.body.fixtures:
            fixture.friction = 0.0
            fixture.density = 1.0
        
        # Default strategies
        self.idle_strategy = IdleStrategy()
        self.patrol_strategy = None  # Set by specific enemy types
        self.chase_strategy = None   # Set by specific enemy types
        self.active_strategy = self.idle_strategy

        # Create a separate fixture for ground contact with higher friction
        self.ground_sensor = self.body.CreateFixture(
            shape=b2.b2PolygonShape(box=(
                pixels_to_meters(width/2 - 2),  # Slightly smaller than player
                pixels_to_meters(2),  # Small height for ground detection
            )),
            friction=0.3,  # Higher friction for ground movement
            isSensor=False
        )

    def detect_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        return distance <= self.detection_radius

    def update(self, player):
        super().update()  # Update GameObject (syncs physics position)
        
        # Update strategy
        if self.detect_player(player):
            self.active_strategy = self.chase_strategy
        else:
            self.active_strategy = self.patrol_strategy
        
        # Apply current strategy
        self.active_strategy.update(self, player)

    def draw(self, screen, camera):
        pygame.draw.rect(screen, self.color, camera.apply(self.rect))

class Slime(Enemy):
    def __init__(self, physics_world, x, y):
        super().__init__(physics_world, x, y, 30, 20, (0, 255, 100), 150)
        self.patrol_strategy = PatrolStrategy(2, 100)
        self.chase_strategy = ChaseStrategy(3)
        
        # Slime-specific physics properties
        for fixture in self.body.fixtures:
            fixture.restitution = 0.2  # Slight bounce

        self.ground_sensor.friction = 0.5
        

class Goblin(Enemy):
    def __init__(self, physics_world, x, y):
        super().__init__(physics_world, x, y, 40, 40, (255, 100, 0), 250)
        self.patrol_strategy = PatrolStrategy(3, 200)
        self.chase_strategy = ChaseStrategy(4)
        
        # Goblin-specific physics properties
        for fixture in self.body.fixtures:
            fixture.restitution = 0.0  # No bounce

class Ghost(Enemy):
    def __init__(self, physics_world, x, y):
        super().__init__(physics_world, x, y, 35, 50, (200, 200, 255), 300)
        self.patrol_strategy = PatrolStrategy(1, 300)
        self.chase_strategy = ChaseStrategy(6)
        
        # Ghost-specific physics properties
        for fixture in self.body.fixtures:
            fixture.density = 0.1   # Lighter than other enemies
            fixture.restitution = 0.0
        
        self.ground_sensor.friction = 0.0

