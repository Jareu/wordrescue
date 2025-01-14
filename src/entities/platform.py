import pygame
from core.game_object import GameObject
from physics.constants import *
from config import config

class Platform(GameObject):
    def __init__(self, physics_world, x, y, width, height):
        # Don't call GameObject.__init__ since we want a static body
        self.width = width
        self.height = height
        self.original_y = y
        self.components = {}
        
        # Create static body
        self.body = physics_world.create_static_body(x, y, width, height)
        self.body.userData = self
        
        # Create pygame rect for rendering
        self.rect = pygame.Rect(x, y, width, height)
        
        # Platform specific properties
        self.color = config.GREEN
    
    def update(self):
        # Static bodies don't need position updates, but components might need updating
        for component in self.components.values():
            component.update()
    
    def draw(self, screen, camera):
        platform_pos = to_pygame_coordinates(self.body.position)
        fixture = self.body.fixtures[0]
        
        # Get the half-width and half-height from the shape's vertices
        vertices = fixture.shape.vertices
        half_width = abs(vertices[0][0])  # Distance from center to edge
        half_height = abs(vertices[0][1])  # Distance from center to edge
        
        # Calculate the rect based on the Box2D body
        self.rect = pygame.Rect(
            platform_pos[0] - meters_to_pixels(half_width),
            platform_pos[1] - meters_to_pixels(half_height),
            meters_to_pixels(half_width * 2),
            meters_to_pixels(half_height * 2)
        )
        
        pygame.draw.rect(screen, self.color, camera.apply(self.rect)) 