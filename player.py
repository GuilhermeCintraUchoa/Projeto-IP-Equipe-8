<<<<<<< HEAD
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
    
    def update(self, platforms):  # Agora recebe platforms como argumento
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= 5
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += 5
        if (keys[K_SPACE] or keys[K_w]) and self.on_ground:
            self.vel_y = -15
            self.on_ground = False

        self.vel_y += 1  # Gravidade
        self.rect.y += self.vel_y

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

        # Colisão com as plataformas
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True
=======
import pygame 

class Player:
    def __init__(self, x_player, y_player):
        self.hp = 100 
        self.velocidade = 10
        self.x = x_player
        self.y = y_player
        self.quadrado = pygame.Rect(self.x, self.y, 20, 20) 

    def mover(self, largura_mapa):
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.x -= self.velocidade 
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.x += self.velocidade 

        self.quadrado.x = self.x
        self.quadrado.y = self.y

    def pular(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] or key[pygame.K_SPACE]:
            self.y -= 40 
        self.quadrado.y = self.y

    def gravidade(self):
        self.y += 10
        self.quadrado.y = self.y
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, (0, 255, 0), self.quadrado)



>>>>>>> 0002b878a8b1f5d17dd08bff4df474350d6138a5
