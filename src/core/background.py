import pygame
from enum import Enum
from config import config

class TileMode(Enum):
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2
    BOTH = 3

class BackgroundLayer:
    def __init__(self, image_path, distance, tile_mode=TileMode.NONE, scale=1.0):
        """
        Initialize a background layer
        
        Args:
            image_path: Path to the image file
            distance: Float between 0 and 1, where 1 is furthest (moves least)
            tile_mode: TileMode enum indicating how the image should be tiled
            scale: Scale factor for the image (after height scaling)
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.tile_mode = tile_mode
        
        # First scale to match window height
        height_scale = config.WINDOW_HEIGHT / self.image.get_height()
        new_width = int(self.image.get_width() * height_scale)
        new_height = config.WINDOW_HEIGHT
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
        # Then apply additional scaling if requested
        if scale != 1.0:
            new_width = int(self.image.get_width() * scale)
            new_height = int(self.image.get_height() * scale)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
        self.distance = max(0.1, min(distance, 1.0))  # Clamp between 0.1 and 1
        self.width = self.image.get_width()
        
        # Only calculate number of copies if tiling horizontally
        if tile_mode in [TileMode.HORIZONTAL, TileMode.BOTH]:
            self.num_copies = (config.LEVEL_WIDTH // self.width) + 3
        else:
            self.num_copies = 1

class ParallaxBackground:
    def __init__(self):
        self.layers = []

    def add_layer(self, image_path, distance, tile_mode=TileMode.NONE, scale=1.0):
        """Add a new background layer"""
        layer = BackgroundLayer(image_path, distance, tile_mode, scale)
        self.layers.append(layer)
        # Sort layers by distance (furthest first)
        self.layers.sort(key=lambda x: x.distance, reverse=True)

    def draw(self, screen, camera):
        """Draw all background layers with parallax effect"""
        for layer in self.layers:
            # Calculate parallax offset based on camera position
            parallax_offset = -(camera.camera.x * (1 - layer.distance))
            
            if layer.tile_mode in [TileMode.HORIZONTAL, TileMode.BOTH]:
                # Calculate the first visible copy's position for tiled layers
                start_x = parallax_offset % layer.width
                
                # Draw enough copies to fill the screen
                for i in range(layer.num_copies):
                    x = start_x + (i * layer.width)
                    if x > config.WINDOW_WIDTH:
                        break
                    screen.blit(layer.image, (x, 0))
            else:
                # For non-tiled layers, just draw once at the parallax offset
                screen.blit(layer.image, (parallax_offset, 0)) 