import pygame
from pygame.locals import *
from settings import LARGURA, ALTURA, FPS, GREEN, BLACK
from player_andrews import Player
from platform_andrews import Platform 
from enemy import Enemy

# Inicializa o Pygame
pygame.init()
pygame.font.init()
fonte = pygame.font.Font('freesansbold.ttf', 32)
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Plataforma Pygame")
clock = pygame.time.Clock()

fundo = pygame.image.load('download.jpg')
fundo = pygame.transform.scale(fundo, (800, 450) )

# Criar objetos
player = Player(100, ALTURA - 100)
platforms = pygame.sprite.Group()
platforms.add(Platform(200, 350, 200, 20))
platforms.add(Platform(450, 250, 200, 20))
platforms.add(Platform(130, 150, 200, 20))
enemy = Enemy(130, 100, 130, 370)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(*platforms)

# Loop principal

kills = 0
going = True
while going:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            going = False
    
    player.update(platforms)
    enemy.update()

    if player.colisao_inimigo(enemy) and enemy.vida > 0:
        enemy.vida -= 1
        enemy.die()
        kills += 1

    player.morte()
    player.sofreu_dano(all_sprites)

    # Desenhar na tela
    screen.fill(GREEN)
    screen.blit(fundo, (0,0))
    mensagem = fonte.render(f"Monstros mortos: {kills}", True, BLACK)
    screen.blit(mensagem, (400, 10))
    all_sprites.draw(screen)

    
    pygame.display.flip()
    
    
pygame.quit()