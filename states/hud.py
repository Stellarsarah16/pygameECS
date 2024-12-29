import pygame
from scripts.settings import *

class HUD:
    def __init__(self, game, player):
        self.player = player
        self.game = game
        self.font = pygame.font.Font(None, 32)  # Initialize font, size 32

    def update(self):
        # This method can be used to update HUD elements if they depend on changing game state
        pass

    # Modify the draw method to accept the screen argument
    def draw(self, screen):
        # Display Left Top
        health_text = self.game.font2.render(f'Health: ', True, (100, 255, 255))
        screen.blit(health_text, (10, 10))  # Position at top-left corner
        health_text2 = self.game.font2.render(f'{self.player.health}', True, self.getColor())
        screen.blit(health_text2, (health_text.get_width() + 10, 10))

        # Display Center Top
        clock_text = self.game.font2.render(f'Elapsed: {self.game.elapsed}', True, (100, 255, 100))
        screen.blit(clock_text, ((WIDTH/2) - (clock_text.get_width()/2), 10))  # Centered at the top

        # Display Right Top
        experience_text = self.game.font2.render(f'Experience: {self.game.game_data['enemies_killed']}', True, (100, 255, 100))
        screen.blit(experience_text, (WIDTH - experience_text.get_width() - 10, 10))  # Right-aligned at the top
        gems_text = self.game.font2.render(f'Gems: {self.game.game_data['gems']}', True, (100, 255, 100))
        screen.blit(gems_text, (WIDTH - gems_text.get_width() - 10, 40))  # Right-aligned at the top

    def getColor(self):
        if self.player.health > 50:
            return (GREEN)
        elif self.player.health > 25:
            return (YELLOW)
        else:
            return (RED)
