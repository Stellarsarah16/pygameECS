import pygame
from components import Cooldown, Transform, BoxImage, SpriteImage, Movement, Camera
from components import Collision, Animation
from ecs import System
from settings import *
from cooldown import Cooldown

class RenderSystem(System):
    def __init__(self, screen, camera):
        super().__init__()
        self.screen = screen
        self.camera = camera
        self.entities = pygame.sprite.Group()

    def render(self, entity):
        self.screen.fill((100, 150, 205))
        camera_position = self.camera.offset

        if entity.has_component("Transform"):
            position = entity.get_component("Transform").position
            #handle BoxImage component
            if entity.has_component("SpriteImage"):
                sprite_image = entity.get_component("SpriteImage")
                if entity.has_component("Animation"):
                    animation = entity.get_component("Animation")
                    current_frame = animation.frames[animation.current_frame]
                    if sprite_image.flipped:
                        sprite_image.image = current_frame
                    else:
                        sprite_image.image = pygame.transform.flip(current_frame, True, False)
                    #sprite_image.image = animation.frames[animation.current_frame]
                self.entities.add(sprite_image)
            elif entity.has_component("BoxImage"):
                box_image = entity.get_component("BoxImage")
                self.entities.add(box_image)
            #handle SpriteImage component


        self.entities.draw(self.screen)

class HealthSystem(System):
    def __init__(self):
        super().__init__()
    def update(self, entity):
        pass

class CollisionSystem(System):
    def __init__(self):
        super().__init__()
    def update(self, entities, delta_time):
        pass

class CameraSystem(System):
    def __init__(self, screen, target):
        super().__init__()
        self.screen = screen
        self.camera = target.get_component("Camera").offset
        self.target = target.get_component("Transform").position

    def update(self, entity):
        if self.target.has_component(Camera):
            self.camera.follow(self.target)

class MovementSystem(System):
    def __init__(self):
        super().__init__()

    def update(self, entity, delta_time):
        if entity.has_component("Movement") and entity.has_component("Transform"):
                movement = entity.get_component("Movement")
                transform = entity.get_component("Transform")
                transform.position += movement.velocity * delta_time
                if entity.has_component("BoxImage"):
                    entity.get_component("BoxImage").rect.topleft = transform.position
                if entity.has_component("SpriteImage"):
                    entity.get_component("SpriteImage").rect.topleft = transform.position

class PlayerSystem(System):
    def __init__(self, input_component):
        super().__init__()
        self.input_component = input_component

    def update(self, player_entity, delta_time):
        if player_entity.has_component("Movement") and player_entity.has_component("Transform"):
            movement = player_entity.get_component("Movement")
            transform = player_entity.get_component("Transform")

            if self.input_component.intent['left'] == 1:
                movement.velocity.x = -15
            elif self.input_component.intent['right'] == 1:
                    movement.velocity.x = 15
            else:
                movement.velocity.x = 0

            if self.input_component.intent['jump'] == True:
                movement.velocity.y = -50
                movement.grounded = False

    def is_on_ground(self, transform):
        # Check if the player is on the ground (should match PhysicsSystem logic)
        return transform.position.y >= HEIGHT - 50

class PhysicsSystem(System):
    def __init__(self, gravity=40):
        super().__init__()
        self.gravity = gravity  # Gravity force, e.g., 9.8 m/s²

    def update(self, entity,delta_time):
        movement = entity.get_component("Movement")
        transform = entity.get_component("Transform")

        # Apply gravity to vertical velocity
        movement.velocity.y += self.gravity * delta_time

        # Update the position based on velocity
        transform.position += movement.velocity * delta_time

        # Stop falling if we detect ground (simplified collision handling)
        if self.is_on_ground(transform):
            movement.velocity.y = 0
            transform.position.y = self.get_ground_level(transform)
            movement.grounded = True

    def is_on_ground(self, transform):
        # Dummy ground collision detection logic (replace with actual checks)
        return transform.position.y >= HEIGHT - 350  # Assume ground is at y=500

    def get_ground_level(self, transform):
        # Returns the ground level (replace with actual terrain logic)
        return HEIGHT - 350  # Assume ground is at y=500

class AnimationSystem(System):
    def __init__(self):
        super().__init__()
        self.last_system_update = pygame.time.get_ticks()
        
    def update(self, entity):
        current_time = pygame.time.get_ticks()
        animation = entity.get_component("Animation")
        movement = entity.get_component("Movement")
        image = entity.get_component("SpriteImage")
        elapsed_time = current_time - animation.last_update_time

        if elapsed_time >= animation.frame_rate:
            if movement.velocity.x > 0:
                image.flipped = False
                if animation.current_state != "walk":
                    animation.set_state("walk")
                    
            elif movement.velocity.x < 0:
                image.flipped = True
                if animation.current_state != "walk":
                    animation.set_state("walk")
            else:
                if animation.current_state != "idle":
                    animation.set_state("idle")

            animation.last_update_time = current_time
            state_frames = animation.sprite_dict[animation.current_state]
            animation.current_frame = (animation.current_frame + 1) % len(state_frames)

class CollisionSystem(System):
    def __init__(self):
        super().__init__()
        self.cooldown = Cooldown(1000)

    def update(self, delta_time):
        for entity in self.entities:
            
            if entity.has_component("Transform"):
                transform = entity.get_component("Transform")
                if self.cooldown.is_ready():
                    for other_entity in self.entities:
                        if other_entity.has_component("Transform"):
                            other_transform = other_entity.get_component("Transform")
                            rect = entity.get_component("BoxImage").rect if entity.has_component("BoxImage") else entity.get_component("SpriteImage").rect
                            other_rect = other_entity.get_component("BoxImage").rect if other_entity.has_component("BoxImage") else other_entity.get_component("SpriteImage").rect
                            if rect.colliderect(other_rect):
                                print("Collision detected!")
