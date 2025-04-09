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
text_restart = fonte.render('restart', False, (255, 255, 255))

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
    vidas_apareceram = 0
    vidas_coletadas = 0
    tempo_ultima_vida = pygame.time.get_ticks()
    MAX_VIDAS = 2

    going = True
    while going:
        screen.fill((0, 0, 0))
        clock.tick(FPS)    

        for event in pygame.event.get():
            
            if event.type == QUIT:
                going = False
                pygame.quit()
                sys.exit()

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
                

        # Mostrar vida extra com intervalo de 5s entre uma e outra e com limite de 2 vidas
        tempo_atual_vida = pygame.time.get_ticks()
        if (not vida_extra_visivel and vida_extra is None 
            and tempo_atual_vida - tempo_inicio_jogo >= 7000 
            and vidas_apareceram < MAX_VIDAS 
            and tempo_atual_vida - tempo_ultima_vida >= 7000):
            vida_extra = Vida()
            vida_extra_visivel = True
            vidas_apareceram += 1
            tempo_ultima_vida = tempo_atual_vida

        if vida_extra_visivel and vida_extra:
            vida_extra.cair()
            if vida_extra.verificar_colisao(player.rect):
                player.vida += 1
                vidas_coletadas += 1
                vida_extra = None
                vida_extra_visivel = False
            elif vida_extra.rect.y > ALTURA:
                vida_extra = None
                vida_extra_visivel = False


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
        if player.vida == 0:
            going = False
            play_again()

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

        # exibe placar de vidas coletadas
        vidas_txt = fonte.render(f"Vidas coletadas: {vidas_coletadas}", True, BLACK)
        screen.blit(vidas_txt, (400, 90))

        if player.sword.active:
            screen.blit(player.sword.image, player.sword.rect.topleft)

        if moeda_visivel:
            moeda_atual.desenhar(screen)

        pygame.display.flip()

def play_again():
    text_play_again = fonte.render('Play again?', 13, (0, 0, 0))
    textx_playagain = LARGURA / 2 - text_play_again.get_width() / 2
    texty_playagain = (ALTURA / 2 - text_play_again.get_height() / 2) - 40
    textx_size_playagain = text_play_again.get_width()
    texty_size_playagain = text_play_again.get_height()

    text_quit = fonte.render('QUIT', 13, (0, 0, 0))
    textx_quit = LARGURA / 2 - text_quit.get_width() / 2
    texty_quit = (ALTURA / 2 - text_quit.get_height() / 2) + 40
    textx_size_quit = text_quit.get_width()
    texty_size_quit = text_quit.get_height()

    pygame.draw.rect(screen, (255, 255, 255), ((textx_playagain - 5, texty_playagain - 5),
                                               (textx_size_playagain + 10, texty_size_playagain +
                                                10)))

    pygame.draw.rect(screen, (255, 255, 255), ((textx_quit -5, texty_quit -5),
                                               (textx_size_quit + 10, texty_size_quit +
                                                10)))

    screen.blit(text_play_again, ((LARGURA / 2 - text_play_again.get_width() / 2),
                       (ALTURA / 2 - text_play_again.get_height() / 2)-40))
    
    screen.blit(text_quit, ((LARGURA / 2 - text_quit.get_width() / 2),
                       (ALTURA / 2 - text_quit.get_height() / 2)+40))

    clock = pygame.time.Clock()
    pygame.display.flip()
    in_main_menu = True
    while in_main_menu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.display.quit()
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if x >= textx_playagain - 5 and x <= textx_playagain + textx_size_playagain + 5:
                    if y >= texty_playagain - 5 and y <= texty_playagain + texty_size_playagain + 5:
                        in_main_menu = False
                        game()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                z, w = event.pos
                if z >= textx_quit - 5 and z <= textx_quit + textx_size_quit + 5:
                    if w >= texty_quit - 5 and w <= texty_quit + texty_size_quit + 5:
                        in_main_menu = False
                        quit_game()

def quit_game():
    pygame.quit()
    sys.exit()

if __name__:
    main_menu()