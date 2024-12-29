import pygame

class Cooldown:
    def __init__(self, duration):
        self.duration = duration
        self.last_used = 0
        

    def is_ready(self):
        current_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_used > self.duration:
            self.last_used = pygame.time.get_ticks()
            return True
        return False