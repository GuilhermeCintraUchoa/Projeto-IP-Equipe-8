import pygame
from pygame.locals import *
from settings import LARGURA, ALTURA, FPS, GREEN, BLACK
from player_andrews import Player
from platform_andrews import Platform 
from enemy import Enemy
from sword_hitbox import SwordHitbox

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
enemy_1 = Enemy(130, 100, 130, 370, vida=27)
enemy_2 = Enemy(450, 200, 450, 700, vida=100)
enemies = pygame.sprite.Group()
enemies.add(enemy_1)
enemies.add(enemy_2)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)
all_sprites.add(*platforms)

# Loop principal

kills = 0
going = True
while going:
    clock.tick(FPS)
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            going = False
         
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                player.attack(keys)

    player.sword.update()
    player.update(platforms)
    enemies.update()

    if player.sword.active:
        hits = pygame.sprite.spritecollide(player.sword, enemies, dokill=False)
        for enemy in hits:
            enemy.levar_dano(player.sword.dano)  # Aplica dano ao inimigo
            if enemy.vida <= 0:
                enemy.kill()
                kills += 1

    for enemy in enemies:
        if player.colisao_inimigo(enemy) and enemy.vida > 0:
            enemy.die()  # Mata o inimigo instantaneamente
            kills += 1
            
    player.morte()
    player.sofreu_dano(all_sprites)

    # Desenhar na tela
    screen.fill(GREEN)
    screen.blit(fundo, (0,0))
    mensagem = fonte.render(f"Monstros mortos: {kills}", True, BLACK)
    screen.blit(mensagem, (400, 10))
    all_sprites.draw(screen)

    if player.sword.active:
        screen.blit(player.sword.image, player.sword.rect.topleft)

    
    pygame.display.flip()
    
    
pygame.quit()
