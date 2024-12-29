from cooldown import Cooldown
from settings import *
from components import Transform, Movement, BoxImage, SpriteImage, Camera, Animation

class Debug:
    def __init__(self, screen, font, font_size=10):
        self.screen = screen
        self.font = font
        self.font_size = font_size
        self.line_spacing=1
        self.cooldown = Cooldown(10)
        self.text_color = (255, 255, 255)
        self.debug_info = []
        
    def clear(self):
        self.debug_info = []

    def update(self, entity_manager, input_manager):
        player_entity = entity_manager.player_entity
        input = input_manager.intent

        self.clear()

        transform = player_entity.get_component("Transform")
        animation = player_entity.get_component("Animation")
        image = player_entity.get_component("SpriteImage")

        if player_entity.has_component("Transform"):
            self.debug_info.append(f"Player position: ({transform.position.x:.2f}, {transform.position.y:.2f})")
        if entity_manager.entities:
            self.debug_info.append(f"{len(entity_manager.entities)} entities")

        # Render debug info
        y = HEIGHT - 50
        if self.cooldown.is_ready():
            for line in self.debug_info:
                text_surface = self.font.render(line, True, self.text_color)
                self.screen.blit(text_surface, (10, y))
                y -= text_surface.get_height() + self.line_spacing

                #self.print_info(animation, image)

    def print_info(self, animation, image):
        print(f"current_frame: {animation.current_frame}  --  state: " +
                f"{animation.current_state} " +
                f" --  flipped: {image.flipped}")

    def draw_gizmos(self, screen):
        for entity in (self.entity_manager.movable_entities):
            if entity.has_component("Transform"):
                position = entity.get_component("Transform").position
                rect = entity.get_component("BoxImage").rect

                camera_position = self.entity_manager.player_entity.get_component("Camera").position
                entity_position = position - camera_position
                new_collide_position = rect.topleft - camera_position
                new_collide_rect = pygame.Rect(new_collide_position, rect.size)
                pygame.draw.rect(screen, (255, 0, 0), new_collide_rect, 1)
                #pygame.draw.circle(screen, (0, 255, 0), entity_position, 5)
