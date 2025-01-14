import json
import os
import sys
from typing import Dict, Any

class Config:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._load_config()
            Config._initialized = True
    
    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '../config/config.json')
        
        if not os.path.exists(config_path):
            print(f"Error: Configuration file not found at {config_path}")
            print("Please ensure config.json exists in the src directory")
            sys.exit(1)
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in config file: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading config file: {e}")
            sys.exit(1)

        try:
            # Window settings
            self.WINDOW_WIDTH = config['window']['width']
            self.WINDOW_HEIGHT = config['window']['height']
            self.FPS = config['window']['fps']

            # Level settings
            self.LEVEL_WIDTH = config['level']['width']
            self.LEVEL_HEIGHT = config['level']['height']

            # Colors
            self.WHITE = tuple(config['colors']['white'])
            self.BLACK = tuple(config['colors']['black'])
            self.RED = tuple(config['colors']['red'])
            self.GREEN = tuple(config['colors']['green'])

            # Player settings
            self.PLAYER_WIDTH = config['player']['width']
            self.PLAYER_HEIGHT = config['player']['height']
            self.PLAYER_SPEED = config['player']['speed']
            self.JUMP_FORCE = config['player']['jump_force']
            self.GRAVITY = config['player']['gravity']
            self.TERMINAL_VELOCITY = config['player']['terminal_velocity']

            # Enemy settings
            self.ENEMY_SPEED_MULTIPLIER = config['enemy']['speed_multiplier']
            
        except KeyError as e:
            print(f"Error: Missing required configuration key: {e}")
            sys.exit(1)

# Create a global instance
config = Config()