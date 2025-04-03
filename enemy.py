import pygame
from settings import RED

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b, all_sprites):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.vel_x = 5
        self.platform_beg = (a, b - 50) 
        self.on_ground = False

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.x >= self.platform_beg[1] or  self.rect.x <= self.platform_beg[0]:
            self.vel_x = self.vel_x * (-1)
        
