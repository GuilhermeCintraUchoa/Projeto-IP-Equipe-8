import pygame
from pygame.locals import *
from settings import LARGURA, ALTURA, FPS, GREEN, BLACK
from Background import ParallaxBackground
from player_andrews import Player
from platform_andrews import Platform 
from enemy import Enemy
from sword_hitbox import SwordHitbox
import sys
from moeda import Moeda
import random
from vidas import Vida

# Inicializa o Pygame
pygame.init()
pygame.font.init()
fonte = pygame.font.Font('graphics/RasterForgeRegular-JpBgm.ttf', 32)
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Plataforma Pygame")
clock = pygame.time.Clock()

background = ParallaxBackground("Background.png", 0.2, 0)
clouds = ParallaxBackground("Nuvens.png", speed=0.2, y_pos=0, auto_scroll_speed=0.3)


# Criar objetos
player = Player(100, ALTURA - 100)
platforms = pygame.sprite.Group()
platforms.add(Platform(200, 350, 200, 20))
platforms.add(Platform(450, 250, 200, 20))
platforms.add(Platform(130, 150, 200, 20))
enemy_1 = Enemy(130, 100, 130, 370, 27)
enemy_2 = Enemy(450, 200, 450, 700, vida=100)
enemies = pygame.sprite.Group() 
enemies.add(enemy_1)
enemies.add(enemy_2)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)
all_sprites.add(*platforms)

player_prev_x = player.rect.x

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

def main_menu():
    global click
    while True:
        screen.fill((0, 0, 0))
        draw_text('main menu', fonte, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()
        
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game()
                return
        if button_2.collidepoint((mx, my)):
            if click:
                quit_game()

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

def game():
    global player_prev_x
    kills = 0

    #moedas
    moeda_atual = None
    moeda_visivel = False
    moedas_apareceram = 0
    moedas_coletadas = 0
    tempo_ultima_moeda = pygame.time.get_ticks()
    MAX_MOEDAS = 3
    
    #vidas
    vida_extra = None
    vida_extra_visivel = False
    tempo_inicio_jogo = pygame.time.get_ticks()
    tempo_vida_extra = None
    invulneravel_ate = 0
    jogador_invulneravel = False

    going = True
    while going:
        screen.fill((0, 0, 0))
        clock.tick(FPS)    

        for event in pygame.event.get():
            if event.type == QUIT:
                going = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # Attack when "n" is pressed
                    player.attack()

        player.sword.update()
        player.update(platforms)
        enemies.update()

        player_dx = player.rect.x - player_prev_x
        player_prev_x = player.rect.x

        for plat in platforms:
            plat.rect.x -= int(player_dx * 0.3)  
    
        for plat in platforms:
            if plat.rect.right < 0:
                plat.rect.left = LARGURA
            elif plat.rect.left > LARGURA:
                plat.rect.right = 0
        

        background.update(player_dx)
        clouds.update(player_dx)

        # Lógica da moeda com tempo entre uma e outra
        tempo_atual_moeda = pygame.time.get_ticks()

        # Criar nova moeda se não tiver nenhuma visível e ainda não atingimos o máximo
        if not moeda_visivel and moedas_apareceram < MAX_MOEDAS:
            if tempo_atual_moeda - tempo_ultima_moeda >= 3000:
                moeda_atual = Moeda()
                moeda_visivel = True
                moedas_apareceram += 1  # Conta como "moeda que apareceu"
                tempo_ultima_moeda = tempo_atual_moeda  # Marca o tempo que apareceu

        # Atualizar moeda visível
        if moeda_visivel and moeda_atual is not None:
            moeda_atual.cair()

            # Se foi coletada
            if moeda_atual.verificar_colisao(player.rect):
                moedas_coletadas += 1
                moeda_visivel = False
                moeda_atual = None

            # Se saiu da tela
            elif moeda_atual.y > ALTURA:
                moeda_visivel = False
                moeda_atual = None

        # Mostrar vida extra após 5 segundos (só uma vez)
        tempo_atual_vida = pygame.time.get_ticks()
        if not vida_extra_visivel and vida_extra is None and tempo_atual_vida - tempo_inicio_jogo >= 5000:
            vida_extra = Vida()
            vida_extra_visivel = True


        if vida_extra_visivel and vida_extra:
            vida_extra.cair()
            if vida_extra.verificar_colisao(player.rect):
                player.vida += 1
                jogador_invulneravel = True
                tempo_fim_invulnerabilidade = tempo_atual_vida + 3000
                vida_extra = None
                vida_extra_visivel = False
            elif vida_extra.rect.y > ALTURA:
                vida_extra = None
                vida_extra_visivel = False

        if jogador_invulneravel and tempo_atual_vida >= tempo_fim_invulnerabilidade:
            jogador_invulneravel = False


        if player.sword.active:
            hits = pygame.sprite.spritecollide(player.sword, enemies, dokill=False)
            for enemy in hits:
                enemy.levar_dano(player.sword.dano)  # Aplica dano ao inimigo
                if enemy.vida <= 0:
                    enemy.kill()
                    kills += 1
        colisao_inimigo, enemie = player.colisao_inimigo(enemies)
        if colisao_inimigo:
            enemie.die()  # Mata o inimigo instantaneamente
            kills += 1

        player.morte()
        player.sofreu_dano(all_sprites)

        # Desenhar na tela
        screen.fill(GREEN)
        background.draw(screen)  
        clouds.draw(screen)

        if vida_extra_visivel and vida_extra is not None:
            vida_extra.desenhar(screen)

        mensagem = fonte.render(f"Monstros mortos: {kills}", True, BLACK)
        screen.blit(mensagem, (400, 10))
        all_sprites.draw(screen)

        # exibe placar de moedas coletadas
        moedas_txt = fonte.render(f"Moedas: {moedas_coletadas}", True, BLACK)
        screen.blit(moedas_txt, (400, 50))

        if player.sword.active:
            screen.blit(player.sword.image, player.sword.rect.topleft)

        if moeda_visivel:
            moeda_atual.desenhar(screen)

        pygame.display.flip()

def quit_game():
    pygame.quit()
    sys.exit()

if __name__:
    main_menu()