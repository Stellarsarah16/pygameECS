import pygame
from scripts.settings import *
from states.state import State
from states.mainmenu import MainMenu
from scripts.level import Level

class EndGame(State):
    def __init__(self, game):
        super().__init__(game)
        self.screen = game.screen
        self.font1 = pygame.font.Font(FONTS["font1"], 32)
        self.font2 = pygame.font.Font(FONTS["font2"], 24)

def update(self, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            #self.level = Level(self.screen)
            self.game.reset_game()
            self.playing()
        elif event.key == pygame.K_q:
             Level(self.game).enter_state()
             self.game.reset_inputs()

            #self.game.state_manager.change_state(GameState.START_MENU)
    self.draw()

    def draw(self):
            self.screen.fill(BLUEBLACK)
            # Draw text
            self.draw_text("Game Over", self.font1, WHITE, self.screen, WIDTH // 2 - 100, HEIGHT/2 - 140)
            # Draw Resume button
            self.draw_text("Press R to Restart", self.font2, WHITE, self.screen, WIDTH // 2 - 100, HEIGHT/2 + 30)
            # Draw Quit button
            self.draw_text("Press Q for Main Menu", self.font2, WHITE, self.screen, WIDTH // 2 - 100, HEIGHT // 2 + 90)