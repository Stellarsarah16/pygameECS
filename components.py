import pygame
from ecs import Component

class Transform(Component):
    def __init__(self, position: pygame.math.Vector2=(0, 0), scale: float=1, rotation: float=0):
        self.position = pygame.math.Vector2(position)
        self.scale = scale
        self.rotation = rotation
        
class Cooldown(Component):
    def __init__(self, duration: int=1000):
        self.duration = duration
        self.last_used = 0

    def is_ready(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_used > self.duration:
            self.last_used = current_time
            return True
        return False
    
class Camera(Component):
    def __init__(self, offset: pygame.math.Vector2=(0, 0)):
        self.offset = pygame.math.Vector2(offset)

    def follow(self, position):
        self.offset = position

class Collision(Component):
    def __init__(self):
        pass
    
class BoxImage(Component, pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, color: tuple=(215, 255, 155)):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

class SpriteImage(Component, pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, offset_angle=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.offset_angle = offset_angle
        self.flipped = False

class Movement(Component):
    def __init__(self, max_velocity=10, terminal_velocity=10):
        self.velocity = pygame.math.Vector2(0, 0)
        self.terminal_velocity = terminal_velocity
        self.grounded = True

class Health(Component):
    def __init__(self, max_health = 100):
        self.max_health = max_health
        self.health = max_health

class Animation(Component):
    def __init__(self, sprite_dict, state="idle", frame_rate=200):
        """sprite_dict[state][frame]"""
        self.sprite_dict = sprite_dict  
        self.frame_rate = frame_rate
        animation_speed = 0.015
        self.current_frame = 0
        self.current_state = state
        self.frames = self.sprite_dict[self.current_state]
        self.last_update_time = pygame.time.get_ticks()

    def get_current_frame(self):
        return self.frames[self.current_frame]

    def set_state(self, state):
        self.current_state = state
        self.frames = self.sprite_dict[state]
        self.reset()

    def reset(self):
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()

    def __repr__(self):
        return f"Animation: {self.sprite_dict}"
    
