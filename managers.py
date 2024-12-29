import pygame
from components import Transform, Camera, Movement, BoxImage, SpriteImage
from systems import RenderSystem, PlayerSystem, MovementSystem, PhysicsSystem, AnimationSystem, CollisionSystem
from systems import CameraSystem
from settings import *
from texturedata import *

#  -----  Font Manager  ------------------------------------------------------- #


class FontManager:
    def __init__(self):
        self.fonts = []

        for font in FONTS:
            self.fonts.append(pygame.font.Font(FONTS[font], 32))

    def get_font(self, index):
        """Retrieve a font by name."""
        return self.fonts[int(index)]


#  -----  Entity Manager  ----------------------------------------------------- #


class EntityManager:
    def __init__(self):
        self.entities = {}  # Store all entities by their ID
        self.component_groups = {}  # Group entities by component name
        self.player_entity = None

    def add_entity(self, entity):
        # Add the entity to the main dictionary
        self.entities[entity.id] = entity

        if entity.has_component("Camera"):
            self.player_entity = entity
        
        # Place the entity into appropriate component groups
        for component_name in entity.components.keys():
            if component_name not in self.component_groups:
                self.component_groups[component_name] = []
            self.component_groups[component_name].append(entity)
    
    def get_entities_with_component(self, component_name):
        return self.component_groups.get(component_name, [])

#  -------Systems Manager  ---------------------------------------------------- #


class SystemManager:
    def __init__(self, entity_manager, input_manager, game):
        self.entity_manager = entity_manager
        self.game = game
        self.input_manager = input_manager
        # init systems    

        self.render_system = RenderSystem(game.screen, self.entity_manager.player_entity.get_component("Camera"))
        self.camera_system = CameraSystem(game.screen, self.entity_manager.player_entity)
        self.player_system = PlayerSystem(self.input_manager)
        self.movement_system = MovementSystem()
        self.physics_system = PhysicsSystem()
        self.animation_system = AnimationSystem()
        self.collision_system = CollisionSystem()

    def update(self, delta_time):
        entities = self.entity_manager.entities.values()

        self.player_system.update(self.entity_manager.player_entity, delta_time)
        self.movement_and_physics_update(delta_time, entities)
        self.animation_update(entities)
        self.collision_update(entities)
        self.render_update(entities)


    def collision_update(self, entities):
        for entity in entities:
            if entity.has_component("Collision"):
                self.collision_system.update(entity)

    def animation_update(self, entities):
        for entity in entities:
            if entity.has_component("Animation") and entity.has_component("Movement"):
                self.animation_system.update(entity)

    def movement_and_physics_update(self, delta_time, entities):
        for entity in entities:
            if entity.has_component("Movement") and entity.has_component("Transform"):
                self.movement_system.update(entity, delta_time)
                self.physics_system.update(entity, delta_time)

    def render_update(self, entities):
        for entity in entities:
            if entity.has_component("Transform"):
                if entity.has_component("BoxImage") or entity.has_component("SpriteImage"):
                    self.render_system.render(entity)

#  -----  Input Manager  ------------------------------------------------------ #


class InputManager():
    def __init__(self):
        self.intent = {'up': False, 'down': False, 
                                        'jump': False,
                                        'left': False, 'right': False,
                                        'pause': False, 'select': False}
        self.key_states = {}  # Tracks the state of each key

    def __repr__(self):
        return f"Intent: {self.intent}, Key States: {self.key_states}"

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key not in self.key_states or not self.key_states[event.key]:
                    # First time key is pressed
                    self.key_states[event.key] = True
                    if event.key == pygame.K_UP:
                        self.intent['up'] = 1
                    elif event.key == pygame.K_DOWN:
                        self.intent['down'] = -1
                    elif event.key == pygame.K_LEFT:
                        self.intent['left'] = 1
                    elif event.key == pygame.K_RIGHT:
                        self.intent['right'] = 1
                    elif event.key == pygame.K_ESCAPE:
                        self.intent['pause'] = True
                    elif event.key == pygame.K_SPACE:
                        self.intent['jump'] = True
                    elif event.key == pygame.K_RETURN:
                        self.intent['select'] = True
            elif event.type == pygame.KEYUP:
                if event.key in self.key_states:
                    self.key_states[event.key] = False
                    if event.key == pygame.K_UP:
                        self.intent['up'] = 0
                    elif event.key == pygame.K_DOWN:
                        self.intent['down'] = 0
                    elif event.key == pygame.K_LEFT:
                        self.intent['left'] = 0
                    elif event.key == pygame.K_RIGHT:
                        self.intent['right'] = 0
                    elif event.key == pygame.K_ESCAPE:
                        self.intent['pause'] = False
                    elif event.key == pygame.K_SPACE:
                        self.intent['jump'] = False
                    elif event.key == pygame.K_RETURN:
                        self.intent['select'] = False


#  -----  Textures Manager   -------------------------------------------------- #


class TextureManager():
    def __init__(self):
        self.block_textures = {}
        self.item_textures = {}
        self.player_textures = {}

        self.gen_block_textures(block_path)
        self.gen_player_textures(PLAYER_PATH)
        self.gen_item_textures()

    def gen_player_textures(self, path):
        atlas_img = pygame.transform.scale(
            pygame.image.load(path).convert_alpha(),
            (PLAYERSIZEX * 10, PLAYERSIZEY * 10)
        )

        # Initialize grouped textures

        for state, frames in PLAYER_ATLAS.items():
            self.player_textures[state] = []
            for frame_data in frames:
                frame = pygame.Surface.subsurface(
                    atlas_img,
                    pygame.Rect(frame_data["position"], frame_data["size"])
                )
                self.player_textures[state].append(frame)

    
    def gen_block_textures(self, path):
        atlas_img = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (PLAYERSIZEX * 10, PLAYERSIZEY * 10))
    
        for name, data in block_atlas.items():
            self.block_textures[name] = pygame.Surface.subsurface(atlas_img, pygame.Rect(data["position"], data["size"]))

    

    def gen_item_textures(self):
        pass

    def get_idle_texture(self):
        return self.player_textures["idle"][0]

    def get_player_sheet(self, state):

        if state in self.player_textures:
            return self.player_textures[state]
        else:
            raise ValueError(f"Unknown texture category: {state}")
        

