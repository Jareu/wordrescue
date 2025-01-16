import pygame
import sys
from config import config
from core.camera import Camera
from entities.player import Player
from entities.items import Coin, JumpBoost
from entities.enemy import Slime, Goblin, Ghost
from ui.overlay import GameUI
from physics.world import PhysicsWorld
from physics.constants import *
from entities.platform import Platform
from core.audio import AudioManager
from core.background import ParallaxBackground, TileMode

audio_manager = AudioManager()
player, platforms, collectibles, enemies = None, None, None, None
is_paused = False

# Add death zone constant
DEATH_ZONE = config.LEVEL_HEIGHT + 300  # 300 pixels below level bottom

def create_platforms(physics_world):
    """Create all platforms for the level"""
    return [
        Platform(physics_world, 0, config.LEVEL_HEIGHT - 40, 300, 40),
        Platform(physics_world, 400, config.LEVEL_HEIGHT - 40, 200, 40),
        Platform(physics_world, 700, config.LEVEL_HEIGHT - 40, 400, 40),
        Platform(physics_world, 1200, config.LEVEL_HEIGHT - 40, 200, 40),
        Platform(physics_world, 1500, config.LEVEL_HEIGHT - 40, 300, 40),
        Platform(physics_world, 1900, config.LEVEL_HEIGHT - 40, 500, 40),
        # Add more platforms for different levels
        Platform(physics_world, 300, config.LEVEL_HEIGHT - 200, 200, 20),
        Platform(physics_world, 600, config.LEVEL_HEIGHT - 300, 200, 20),
        Platform(physics_world, 900, config.LEVEL_HEIGHT - 400, 200, 20),
    ]

def reset_game(physics_world):
    """Reset the game to initial state"""
    global player, platforms, collectibles, enemies
    player = Player(physics_world, 100, 300)
    platforms = create_platforms(physics_world)
    collectibles = [
        Coin(300, config.LEVEL_HEIGHT - 100),
        Coin(500, config.LEVEL_HEIGHT - 100),
        Coin(700, 300),
        JumpBoost(900, config.LEVEL_HEIGHT - 100),
        Coin(1200, 200),
        JumpBoost(1500, 300),
    ]
    enemies = [
        Slime(physics_world, 400, config.LEVEL_HEIGHT - 60),
        Goblin(physics_world, 800, config.LEVEL_HEIGHT - 80),
        Ghost(physics_world, 1200, config.LEVEL_HEIGHT - 90),
        Slime(physics_world, 1600, config.LEVEL_HEIGHT - 60),
    ]

def handle_pause():
    global is_paused
    is_paused = not is_paused

    if is_paused:
        audio_manager.play_sound('pause')
    else:
        audio_manager.play_sound('unpause')

def main():
    global is_paused
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    physics_world = PhysicsWorld()
    camera = Camera(config.LEVEL_WIDTH, config.LEVEL_HEIGHT)
    ui = GameUI()
    
    reset_game(physics_world)
    is_paused = False

    # Initialize background
    background = ParallaxBackground()
    background.add_layer("assets/backgrounds/sky.png", 2.0, TileMode.HORIZONTAL)
    background.add_layer("assets/backgrounds/landscape5.png", 0.99, TileMode.NONE, scale=1.7, y_offset=-350)  
    background.add_layer("assets/backgrounds/mountains2.png", 0.97, TileMode.NONE, scale=0.8, x_offset=-100, y_offset=250)
    background.add_layer("assets/backgrounds/landscape2.png", 0.93, TileMode.HORIZONTAL, scale=0.8, x_offset=0, y_offset=50) 
    background.add_layer("assets/backgrounds/landscape1.png", 0.92, TileMode.HORIZONTAL, scale=0.8, x_offset=0, y_offset=50) 
    background.add_layer("assets/backgrounds/grass.png", 0.90, TileMode.NONE, scale=0.8, x_offset=0, y_offset=175) 
    #background.add_layer("../assets/backgrounds/trees.png", 0.6, TileMode.HORIZONTAL)  # Trees tile horizontally
    
    while True:
        # Always handle events, even when paused
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r and not is_paused:
                    reset_game(physics_world, audio_manager)
                elif event.key == pygame.K_p:
                    handle_pause()
                elif event.key == pygame.K_w and not is_paused:
                    player.jump()

        # Only process game logic if not paused
        if not is_paused:
            # Handle movement input
            keys = pygame.key.get_pressed()
            direction = 0
            if keys[pygame.K_a]:
                direction = -1
            if keys[pygame.K_d]:
                direction = 1
            player.move(direction)

            # Update physics world
            physics_world.update()
            
            # Update game objects
            player.update()
            
            for platform in platforms:
                platform.update()
            
            # Check death zone
            if player.rect.top >= DEATH_ZONE:
                reset_game(physics_world)
                audio_manager.play_sound('death')

            camera.update(player)

            for collectible in collectibles:
                collectible.update(player)
            
            # Update enemies with physics
            for enemy in enemies:
                enemy.update(player)
                if enemy.rect.colliderect(player.rect):
                    reset_game(physics_world)
                    audio_manager.play_sound('death')

        # Always update UI and draw
        ui.update_coin_count(player.coins)

        # Draw game state
        screen.fill(config.BLACK)
        
        # Draw background layers first
        background.draw(screen, camera)
    
        # Draw platforms using their draw method
        for platform in platforms:
            platform.draw(screen, camera)
        
        for collectible in collectibles:
            collectible.draw(screen, camera)
        
        for enemy in enemies:
            enemy.draw(screen, camera)
        
        if player.rect.top < DEATH_ZONE:
            pygame.draw.rect(screen, config.RED, camera.apply(player.rect))

        # Draw UI last, including pause overlay if paused
        ui.draw(screen, is_paused)

        pygame.display.flip()
        clock.tick(config.FPS)

if __name__ == "__main__":
    main()