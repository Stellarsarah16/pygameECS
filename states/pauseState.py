import pygame
from states.state import GameState
from states.menuState import MenuState

from settings import *
from components import Cooldown

class PauseState(GameState):
    def __init__(self, state_manager, screen, font_manager, input_manager):
        self.state_manager = state_manager
        self.screen = screen

        self.font_manager = font_manager
        self.title_font = font_manager.get_font(2)
        self.menu_font = font_manager.get_font(3)
        self.cooldown = Cooldown(150)
        self.overlay = pygame.Surface((WIDTH, HEIGHT))
        self.overlay.fill(COLORS["blueblack"])   
        self.overlay.set_alpha(120)
        self.mid_w = self.screen.get_rect().centerx
        self.mid_h = self.screen.get_rect().centery

        self.input = input
        self.input_manager = input_manager

        self.options = ["Resume", "Restart", "Main Menu"]
        self.selected_index = 0  # Index to track the currently selected button
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)

    def handle_input(self, events):
        if self.cooldown.is_ready():

            # Get the updated intents
            intent = self.input_manager.intent
            # Navigate menu
            if intent['up'] == 1:  # Up
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif intent['down'] == -1:  # Down
                self.selected_index = (self.selected_index + 1) % len(self.options)
            # Select menu item
            if intent['select']:
                print(self.selected_index)
                if self.selected_index == 0:  # Resume
                    self.state_manager.pop()
                    pygame.time.delay(100)
                elif self.selected_index == 1:  # Restart
                    self.state_manager.pop()
                    from states.playingState import PlayingState
                    self.state_manager.push(PlayingState(self.state_manager, 
                                        self.screen, self.font_manager, self.input_manager))
                    pygame.time.delay(100)
                elif self.selected_index == 2:  # Main Menu

                    self.state_manager.pop_to_menu()
                    pygame.time.delay(100)

                # Clear intents after handling
                intent['vy'] = 0
                intent['select'] = False
                pygame.event.clear()


    def update(self, dt):
        pass  # Menu has no active logic for now

    def render(self, screen):
        screen.blit(self.overlay, (0, 0))
        # Draw the title/logo centered on the screen
        self.draw_text_centered("Stellar Survivor", self.title_font, COLORS["white"], screen, self.mid_w, self.mid_h - 100)

        # Draw menu options centered below the logo
        for index, option in enumerate(self.options):
            if index == self.selected_index:
                color = COLORS["yellow"]  # Highlight the selected option
            else:
                color = COLORS["white"]
            # Center the menu options vertically with some spacing
            self.draw_text_centered(option, self.menu_font, color, screen, self.mid_w, self.mid_h + index * 30 - 20)

    def draw_text_centered(self, text, font, color, surface, x, y):
        """Helper function to draw text centered at the given (x, y) position."""
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect(center=(x, y))  # Center the text around the (x, y) position
        surface.blit(textobj, textrect)