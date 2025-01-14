PIXELS_PER_METER = 50.0
METERS_PER_PIXEL = 1.0 / PIXELS_PER_METER

def pixels_to_meters(pixels):
    return pixels * METERS_PER_PIXEL

def meters_to_pixels(meters):
    return meters * PIXELS_PER_METER

def to_pygame_coordinates(body_position):
    """Convert Box2D coordinates to Pygame coordinates"""
    return (
        meters_to_pixels(body_position[0]),
        meters_to_pixels(body_position[1])
    )

def to_box2d_coordinates(pygame_position):
    """Convert Pygame coordinates to Box2D coordinates"""
    return (
        pixels_to_meters(pygame_position[0]),
        pixels_to_meters(pygame_position[1])
    )