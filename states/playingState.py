import pygame, os
from ecs import Entity
from components import Cooldown, Transform, BoxImage, SpriteImage, Movement, Camera, Animation
from components import Collision
from systems import RenderSystem, HealthSystem, CollisionSystem, MovementSystem, AnimationSystem
from systems import CameraSystem, PlayerSystem, PhysicsSystem
from states.state import GameState
from states.pauseState import PauseState
from settings import *
from managers import EntityManager, InputManager, TextureManager, SystemManager
from debug import Debug

class PlayingState(GameState):
    def __init__(self, state_manager, screen, font_manager, input_manager):
        self.state_manager = state_manager
        self.screen = screen
        self.font_manager = font_manager
        self.title_font = font_manager.get_font(2)
        self.menu_font = font_manager.get_font(3)
        self.entities = []
        self.input_manager = input_manager
        self.pause_state = PauseState(self.state_manager, self.screen, self.font_manager, self.input_manager)
        self.dt = 0

        self.entity_manager = EntityManager()
        self.texture_manager = TextureManager()
        self.debug_system = Debug(self.screen, self.font_manager.get_font(1))
        self.init_game_entities()
        self.system_manager = SystemManager(self.entity_manager, self.input_manager, self)

    def init_game_entities(self):
        # Player
        player_entity = Entity()
        player_entity.add_component("Transform", Transform(CENTER_SCREEN))
        player_entity.add_component("BoxImage", BoxImage(32, 48, COLORS["red"]))
        player_entity.add_component("SpriteImage", SpriteImage(self.texture_manager.get_idle_texture()))
        player_entity.add_component("Movement", Movement())
        player_entity.add_component("Camera", Camera(CENTER_SCREEN))
        player_entity.add_component("Collision", Collision())
        player_entity.add_component("Animation", Animation(self.texture_manager.player_textures, "idle"))
        self.entity_manager.add_entity(player_entity)

        #Floor
        for i in range(0):
            block_entity = Entity()
            block_entity.add_component("Transform", Transform((i * 32, 600), (32, 32)))
            block_entity.add_component("BoxImage", BoxImage(32, 32))
            block_entity.add_component("Collision", Collision())
            self.entity_manager.add_entity(block_entity)



#  Game Loop
# --------------------------------------------------------------- #

    def handle_input(self, events):
        '''handle_input called from StateManager'''
        intent = self.input_manager.intent
        if intent['pause'] == True:
            self.state_manager.push(self.pause_state)

    # Update
    # ------------------------------------- #
    def update(self, dt):
        self.system_manager.update(dt)
        self.debug_system.update(self.entity_manager, self.input_manager)

    def render(self, surface):
        pass