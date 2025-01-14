from core.game_object import GameObject
from config import config
from physics.constants import *
import math
import Box2D as b2

class Player(GameObject):
    def __init__(self, physics_world, x, y):
        super().__init__(physics_world, x, y, config.PLAYER_WIDTH, config.PLAYER_HEIGHT)
        self.coins = 0
        self.jump_force = pixels_to_meters(config.JUMP_FORCE)
        
        # Set up player-specific physics properties
        self.body.fixedRotation = True
        for fixture in self.body.fixtures:
            fixture.friction = 0.0  # Reduce friction to prevent wall sticking
            fixture.restitution = 0.0  # No bouncing
            
            # Create a separate fixture for ground contact with higher friction
            ground_sensor = self.body.CreateFixture(
                shape=b2.b2PolygonShape(box=(
                    pixels_to_meters(config.PLAYER_WIDTH/2 - 2),  # Slightly smaller than player
                    pixels_to_meters(2),  # Small height for ground detection
                )),
                friction=0.3,  # Higher friction for ground movement
                isSensor=False
            )
    
    def move(self, direction):
        velocity = self.body.linearVelocity
        desired_velocity = 5.0 * direction  # 5 m/s
        
        # Change velocity while maintaining vertical speed 
        self.body.linearVelocity = (desired_velocity, velocity.y)
    
    def jump(self):
        # Check if player's bottom edge is touching something
        can_jump = False
        contact_body = None
        player_bottom = self.body.position.y + pixels_to_meters(self.height/2)
        
        # Get all contacts
        for edge in self.body.contacts:
            if not edge.contact:
                continue
                
            if not edge.contact.touching:
                continue
                
            # Get the manifold points to check contact position
            manifold = edge.contact.manifold
            normal = manifold.localNormal
            
            # Check if contact normal is pointing upward (bottom collision)
            if math.fabs(normal.y) > 0.707:  # cos(45°) ≈ 0.707, allows for some slope
                # Get the other body
                other_body = edge.contact.fixtureB.body if edge.contact.fixtureA.body == self.body else edge.contact.fixtureA.body
                can_jump = True
                contact_body = other_body
                break
        
        if can_jump and contact_body:
            # Calculate jump impulse based on mass
            impulse_magnitude = -self.jump_force * self.body.mass
            
            # Apply upward impulse to player
            self.body.ApplyLinearImpulse(
                (0, impulse_magnitude),
                (self.body.worldCenter),
                True
            )
            
            # Apply equal and opposite impulse to the contact body
            # Only if it's not a static body
            if contact_body.type != b2.b2_staticBody:
                contact_body.ApplyLinearImpulse(
                    (0, -impulse_magnitude),
                    contact_body.worldCenter,
                    True
                )
            
            # Play jump sound
            self.audio_manager.play_sound('jump')
    
    def collect_coin(self):
        self.coins += 1
    
    def reset_stats(self):
        self.coins = 0