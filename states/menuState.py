import pygame
from states.state import GameState
from settings import *
from components import Cooldown

class MenuState(GameState):
    def __init__(self, state_manager, screen, font_manager, input_manager):
        self.state_manager = state_manager
        self.input_manager = input_manager
        self.screen = screen
        self.font_manager = font_manager
        self.title_font = font_manager.get_font(2)
        self.menu_font = font_manager.get_font(3)

        self.cooldown = Cooldown(200)
        # Menu options and cursor management
        self.options = ["Start Game", "Quit", "Settings"]
        self.selected_index = 0  # Index to track the currently selected button
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = 0

        self.mid_w = self.screen.get_rect().centerx
        self.mid_h = self.screen.get_rect().centery

    def handle_input(self, events):
        intent = self.input_manager.intent
        if self.cooldown.is_ready():
            print("MenuState: intent =", intent['select'])
            # Navigate menu
            if intent['up'] == 1:  # Up
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif intent['down'] == -1:  # Down
                self.selected_index = (self.selected_index + 1) % len(self.options)

            # Select menu item
            if intent['select']:
                if self.selected_index == 0:  # Start Game
                    print("MenuState: start game selected")
                    from states.playingState import PlayingState
                    self.state_manager.push(PlayingState(self.state_manager, self.screen, 
                                                         self.font_manager, self.input_manager))
                    pygame.time.delay(100)
                elif self.selected_index == 1:  # Quit
                    pygame.quit()
                    exit()

    def update(self, dt):
        pass


    def render(self, screen):
        screen.fill(COLORS["darksky"])

        # Draw the title/logo centered on the screen
        self.draw_text_centered("Stellaria", self.title_font, COLORS["white"], screen, self.mid_w, self.mid_h - 140)

        # Draw menu options centered below the logo
        for index, option in enumerate(self.options):
            if index == self.selected_index:
                color = COLORS["yellow"]  # Highlight the selected option
            else:
                color = COLORS["white"]
            # Center the menu options vertically with some spacing
            self.draw_text_centered(option, self.menu_font, color, screen, self.mid_w, self.mid_h + index * 40 - 20)

    def draw_text_centered(self, text, font, color, surface, x, y):
        """Helper function to draw text centered at the given (x, y) position."""
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect(center=(x, y))  # Center the text around the (x, y) position
        surface.blit(textobj, textrect)
