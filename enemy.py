import pygame
from settings import RED

import pygame
from settings import RED

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, left_limit, right_limit):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_x = 5  # Velocidade horizontal
        self.left_limit = left_limit
        self.right_limit = right_limit - self.rect.width  # Ajuste para evitar saída
        self.on_ground = False
        self.vida = 1
        
    def update(self):
        # Movimentação do inimigo
        self.rect.x += self.vel_x

        # Inverte direção se atingir os limites
        if self.rect.right >= self.right_limit or self.rect.left <= self.left_limit:
            self.vel_x *= -1
    
    def levar_dano(self, dano):
        self.vida -= dano
        self.image.fill((255, 100, 100))
        if self.vida <= 0:
            self.die()
    
    def die(self):
        pygame.time.delay(100)
        self.kill()
