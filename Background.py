import pygame
import os
from settings import LARGURA, ALTURA

class ParallaxBackground:
    def __init__(self, image_path, speed, y_pos, auto_scroll_speed=0):
        self.auto_scroll_speed = auto_scroll_speed
        self.image = pygame.image.load(os.path.join("assets", "images", image_path)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (LARGURA * 2, ALTURA))
        self.speed = speed
        self.x1 = 0 
        self.x2 = self.image.get_width() 
        self.y = y_pos

    def update(self, player_dx):
        offset = (player_dx * self.speed) + self.auto_scroll_speed
        self.x1 -= offset
        self.x2 -= offset

    
        if self.x1 <= -LARGURA * 2:
            self.x1 = LARGURA * 2
        if self.x2 <= -LARGURA * 2:
            self.x2 = LARGURA * 2

    def draw(self, surface):
        surface.blit(self.image, (self.x1, self.y))  
        surface.blit(self.image, (self.x2, self.y))




