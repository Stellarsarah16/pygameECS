import pygame
from os import path
from states.state import State

img_dir = path.join(path.dirname(__file__), '../assets/Items')

class PowerUp:
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect  # Effect is a function or a value to modify player stats

    def apply(self, player):
        # Apply the effect to the player
        self.effect(player)

class PowerUpManager:
    def __init__(self):
        self.powerups = []

    def add_powerup(self, powerup):
        self.powerups.append(powerup)

class HealthPowerup(pygame.sprite.Sprite):
    def __init__(self, position, type, effect=None):
        super().__init__()
        self.type = type

        self.image =  pygame.transform.scale(
            pygame.image.load(path.join(img_dir, 'powerup.png')).convert_alpha(), (24, 24))
        self.rect = self.image.get_rect(center=position)

        self.amount = 20

        self.effect = effect  # A function or effect that this power-up will trigger
        #self.velocity = pygame.math.Vector2(0, -1)  # Adjust direction and speed as needed

    def apply(self, player):
        if self.type == 'health':
            player.health += self.amount
            player.applyHealth(self.amount) # Apply the power-up effect to the player
        self.kill()  # Remove the power-up after it's collected

    