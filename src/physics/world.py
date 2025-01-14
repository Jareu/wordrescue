import Box2D as b2
from .constants import *

class PhysicsWorld:
    def __init__(self):
        # Create Box2D world with downward gravity
        self.world = b2.b2World(gravity=(0, 9.81))
        
        # Physics simulation settings
        self.time_step = 1.0 / 60.0
        self.vel_iters = 6
        self.pos_iters = 2
        
        # Debug drawing (optional)
        self.debug_draw = None
    
    def create_static_body(self, x, y, width, height):
        """Create a static body (for platforms)"""
        body_def = b2.b2BodyDef()
        body_def.position = to_box2d_coordinates((x + width/2, y + height/2))
        
        body = self.world.CreateBody(body_def)
        
        shape = b2.b2PolygonShape()
        shape.SetAsBox(
            pixels_to_meters(width/2),
            pixels_to_meters(height/2)
        )
        
        body.CreateFixture(
            shape=shape,
            friction=0.3
        )
        
        return body
    
    def create_dynamic_body(self, x, y, width, height, density=1.0):
        """Create a dynamic body (for players, enemies)"""
        body_def = b2.b2BodyDef()
        body_def.type = b2.b2_dynamicBody
        body_def.position = to_box2d_coordinates((x + width/2, y + height/2))
        body_def.fixedRotation = True  # Prevent rotation
        
        body = self.world.CreateBody(body_def)
        
        shape = b2.b2PolygonShape()
        shape.SetAsBox(
            pixels_to_meters(width/2),
            pixels_to_meters(height/2)
        )
        
        body.CreateFixture(
            shape=shape,
            density=density,
            friction=0.3
        )
        
        return body

    def update(self):
        self.world.Step(self.time_step, self.vel_iters, self.pos_iters)
        self.world.ClearForces()