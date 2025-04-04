import pygame
from pygame.locals import *
from settings import WHITE, ALTURA, LARGURA

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.vida = 3
        self.image = pygame.Surface((60, 60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.on_ground = False
        self.invulnerabilidade = False #Se o player não pular em cima do inimigo, ex: Colidir lateralmente, ele perderá vida e entrará em um estado invulnerável
        self.start_time = 0 #Será guardado aqui o exato momento em que o player sofreu dano, pois aqui inicia o estado invunerável
    
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

        if (keys[K_SPACE] or keys[K_w] or keys[K_UP]) and self.on_ground:
            self.vel_y = -15
                   
        self.vel_y += 1
        self.rect.y += self.vel_y  
        self.on_ground = False  

        # Colisão com as plataformas
        for plat in platforms:
            if self.rect.colliderect(plat) :
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

    def colisao_inimigo(self, enemy):
        if self.rect.colliderect(enemy):  # Verifica colisão
            if self.vel_y > 0 and not self.invulnerabilidade:
              return True  # Retorna True se houve colisão e o inimigo morreu
            
            elif not self.invulnerabilidade: 
                self.start_time = pygame.time.get_ticks() #Inicia o estado em que o player fica invulnerável            
                self.invulnerabilidade = True 
                self.vida -= 1 

        return False  # Retorna False se o inimigo não morreu ou se não houve colisão 
    
    def sofreu_dano(self, all_sprites):
        if self.invulnerabilidade and self.vida > 0: 
            if pygame.time.get_ticks() - self.start_time <= 2000: # Quando passar 2 segundos, o player sairá do estado invunerável 
              if (pygame.time.get_ticks() // 100) % 2 == 0: #Alterna a cada 100ms fazendo a sprite do player sumir e voltar 
                self.kill()
              else: 
                all_sprites.add(self)  
            else:
                all_sprites.add(self)
                self.invulnerabilidade = False 
            
    def morte(self):
        if self.vida == 0:
            self.kill()