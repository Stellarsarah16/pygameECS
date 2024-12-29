import pygame


from states.state import StateManager
from states.menuState import MenuState            
from states.playingState import PlayingState
 

from managers import FontManager, InputManager
from settings import *                

from ecs import Entity


class Main:
    def __init__(self):
        # Initialize Pygame

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.input_manager = InputManager()

        # Initialize Font Manager
        self.font_manager = FontManager()

        # Initialize State Manager and Push Initial State
        self.state_manager = StateManager()
        self.state_manager.push(MenuState(self.state_manager, self.screen, self.font_manager, self.input_manager))

    def run(self):

        # Main Game Loop
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            # Delegate to StateManager
            self.input_manager.update(events)

            self.state_manager.handle_input(events)
            self.state_manager.update(dt)
            self.state_manager.render(self.screen)

            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    Main().run()

