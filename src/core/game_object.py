import pygame
from physics.constants import *
from .audio import AudioManager

class GameObject:
    def __init__(self, physics_world, x, y, width, height):
        self.width = width
        self.height = height
        self.original_y = y
        self.audio_manager = AudioManager.get_instance()
        self.body = None
        self.components = {}
        
        # Create Box2D body
        if(physics_world):
            self.body = physics_world.create_dynamic_body(x, y, width, height)
            self.body.userData = self  # Link the physics body back to this object
        
        # Create pygame rect for rendering
        self.rect = pygame.Rect(x, y, width, height)
    
    def update(self):
        # Update pygame rect position from physics body
        if(self.body):
            pos = self.body.position
            self.rect.center = to_pygame_coordinates(pos)
        
        # Update components
        for component in self.components.values():
            component.update()
    
    def add_component(self, component_name: str, component):
        component.game_object = self
        self.components[component_name] = component
    
    def get_component(self, component_name: str):
        return self.components.get(component_name)