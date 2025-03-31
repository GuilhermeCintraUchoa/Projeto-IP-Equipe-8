import pygame
from pygame.locals import *
from settings import LARGURA, ALTURA, FPS, GREEN
from player import Player
from platform import Platform


# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Plataforma Pygame")
clock = pygame.time.Clock()


# Criar objetos
player = Player(100, ALTURA - 100)
platforms = pygame.sprite.Group()
platforms.add(Platform(200, 350, 200, 20))
platforms.add(Platform(450, 250, 200, 20))
platforms.add(Platform(100, 150, 200, 20))

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(*platforms)

# Loop principal
going = True
while going:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            going = False
    
    player.update(platforms)
    
    # Desenhar na tela
    screen.fill(GREEN)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()