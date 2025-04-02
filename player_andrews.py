import pygame
from pygame.locals import *
from settings import WHITE, ALTURA, LARGURA

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.on_ground = False
    
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= 5
            for plat in platforms:
                if self.rect.colliderect(plat):  
                    self.rect.x += 5  # Reverte o movimento
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += 5
            for plat in platforms:
                if self.rect.colliderect(plat):  
                    self.rect.x -= 5  # Reverte o movimento
            
        self.vel_y += 1
        self.rect.y += self.vel_y  
        self.on_ground = False  

        # Colisão com as plataformas
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0:  # Se estiver caindo
                    self.rect.bottom = plat.rect.top  
                    self.vel_y = 0  
                    self.on_ground = True  # Confirma que está no chão
                elif self.vel_y < 0:  # Se bater a cabeça
                    self.rect.top = plat.rect.bottom
                    self.vel_y = 0
        
        # Colisão com o chão
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA
            self.vel_y = 0
            self.on_ground = True
        # Fazendo com que o jogador não saia da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA 

    def pular(self):
        keys = pygame.key.get_pressed()
        if (keys[K_SPACE] or keys[K_w] or keys[K_UP]) and self.on_ground:
            self.vel_y = -15