import pygame
import os

class AudioManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if AudioManager._instance is not None:
            raise Exception("AudioManager is a singleton!")
        pygame.mixer.init()
        self.sounds = {}
        self._load_sounds()
        
    def _load_sounds(self):
        """Load all sound files"""
        sounds_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'sounds')
        
        try:
            self.sounds['jump'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'jump.mp3'))
            self.sounds['coin'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'coin.mp3'))
            self.sounds['magic-boost'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'magic-boost.mp3'))
            self.sounds['expire'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'expire.mp3'))
            self.sounds['pause'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'pause.mp3'))
            self.sounds['unpause'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'unpause.mp3'))
            self.sounds['death'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'death.mp3'))
        except pygame.error as e:
            print(f"Warning: Could not load jump sound: {e}")
            self.sounds['jump'] = None
    
    def play_sound(self, sound_name):
        """Play a sound by name"""
        if sound := self.sounds.get(sound_name):
            sound.play() 