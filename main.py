import pygame
from pygame.locals import *
from settings import LARGURA, ALTURA, FPS, GREEN, BLACK
from player_andrews import Player
from platform_andrews import Platform 
from enemy import Enemy
import sys

# Inicializa o Pygame
pygame.init()
pygame.font.init()
fonte = pygame.font.Font('graphics/RasterForgeRegular-JpBgm.ttf', 32)
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
enemies = pygame.sprite.Group() 
enemies.add(enemy)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)
all_sprites.add(*platforms)

# Funcao draw_text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

# Textos botoes
text_play = fonte.render('jogar', False, (255, 255, 255))
text_quit = fonte.render('quit', False, (255, 255, 255))

def main_menu ():
    while True:

        screen.fill((0, 0, 0))
        draw_text('main menu', fonte, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        
        button_1 = pygame.Rect(50, 100, 200, 50)
        
        button_2 = pygame.Rect(50, 200, 200, 50)
        

        

        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                quit()
        pygame.draw.rect(screen, (20, 70, 150), button_1)
        text_rect = text_play.get_rect(center=button_1.center)
        screen.blit(text_play, text_rect)

        pygame.draw.rect(screen, (20, 70, 150), button_2)
        text_rect = text_quit.get_rect(center=button_2.center)
        screen.blit(text_quit, text_rect)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()
        clock.tick(FPS)


# Loop principal

def game():
    kills = 0
    going = True
    while going:
        screen.fill((0,0,0))
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    going = False
                    
        
        player.update(platforms)
        enemy.update()

        if player.colisao_inimigo(enemies) and enemy.vida > 0:
            enemy.vida -= 1
            enemy.die()
            kills += 1

        player.morte()
        player.sofreu_dano(all_sprites)

        # Desenhar na tela
        screen.fill(GREEN)
        screen.blit(fundo, (0,0))
        mensagem = pygame.transform.scale_by((fonte.render(f"Monstros mortos: {kills}", True, BLACK)), 0.7)
        screen.blit(mensagem, (500, 10))
        all_sprites.draw(screen)
        pygame.display.update()

def quit():
    pygame.quit()
    sys.exit()
    


main_menu()
    
pygame.quit()