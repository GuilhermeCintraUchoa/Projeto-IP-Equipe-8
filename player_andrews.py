import pygame
from pygame.locals import *
from settings import *
from sword_hitbox import SwordHitbox
from Spritesheet import SpriteSheet

jumpSprites = [
    (4, 8, 40, 52),
    (84, 8, 40, 52),
    (164, 8, 40, 52),
    (244, 8, 40, 52),
    (324, 8, 40, 52)
]


runSprites = [
    (24, 16, 40, 52),
    (104, 16, 40, 52),
    (184, 16, 40, 52),
    (264, 16, 40, 52),
    (344, 16, 40, 52),
    (424, 16, 40, 52),
    (504, 16, 40, 52),
    (584, 16, 40, 52)
]

idleSprites = [
    (12, 12, 44, 52),
    (76, 12, 44, 52),
    (140, 12, 44, 52),
    (204, 12, 44, 52)
]



attackSprites = [
    (4, 0, 92, 80),
    (100, 0, 92, 80),
    (196, 0, 92, 80),
    (294, 0, 92, 80),
    (388, 0, 92, 80),
    (484, 0, 92, 80),
    (580, 0, 92, 80),
    (676, 0, 92, 80)
]

deathSprites = [
    (0, 0, 64, 56),
    (80, 0, 64, 56),
    (160, 0, 64, 56),
    (240, 0, 64, 56),
    (320, 0, 64, 56),
    (400, 0, 64, 56),
    (480, 0, 64, 56),
    (560, 0, 64, 56)
]

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, faceRight):
        super().__init__()

        self.vida = 3
        self.moedas = 0
        self.image = pygame.Surface((60, 60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.invulnerabilidade = False #Se o player não pular em cima do inimigo, ex: Colidir lateralmente, ele perderá vida e entrará em um estado invulnerável
        self.start_time = 0 #Será guardado aqui o exato momento em que o player sofreu dano, pois aqui inicia o estado invunerável
        self.sword = SwordHitbox(x+50, y, 80, 100, dano=1)

        # Load spritesheets
        idleSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Idle/Idle-Sheet.png", idleSprites)
        runSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Run/Run-Sheet.png", runSprites)
        attackSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Attack-01/Attack-01-Sheet.png", attackSprites)
        jumpSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Jump/Jump-All-Sheet.png", jumpSprites)

        self.spriteSheets = {
            'IDLE'   : idleSpriteSheet,
            'RUN'    : runSpriteSheet,
            'ATTACK' : attackSpriteSheet,
            'JUMP'   : jumpSpriteSheet
        }

        self.animationIndex = 0
        self.facingRight = faceRight
        self.currentState = 'IDLE'
        self.xDir = 0
        self.speed = SPEED_HERO
        self.xPos = x
        self.yPos = y
        
    def update(self, platforms):
        self.previousState = self.currentState
        self.xDir = 0

        # ---------------------------
        # MOVIMENTO HORIZONTAL
        # ---------------------------
        keys = pygame.key.get_pressed()
        if self.currentState != 'ATTACK':
            if keys[K_n]:
                self.currentState = 'ATTACK'
            else:
                if keys[K_LEFT] or keys[K_a]:
                    self.facingRight = False
                    self.xDir = -1
                    self.currentState = 'RUN'
                if keys[K_RIGHT] or keys[K_d]:
                    self.facingRight = True
                    self.xDir = 1
                    self.currentState = 'RUN'
                if (keys[K_SPACE] or keys[K_w] or keys[K_UP]) and self.on_ground:
                    self.vel_y = -15
                    self.on_ground = False
                    self.currentState = 'JUMP'

                


        # ---------------------------
        # APLICA MOVIMENTO HORIZONTAL
        # ---------------------------
        self.rect.x += self.xDir * self.speed

        # Colisão horizontal (impede atravessar plataformas lateralmente)
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.xDir > 0:
                    self.rect.right = plat.rect.left
                elif self.xDir < 0:
                    self.rect.left = plat.rect.right

        # ---------------------------
        # APLICA GRAVIDADE
        # ---------------------------
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # ---------------------------
        # COLISÃO VERTICAL COM PLATAFORMAS
        # ---------------------------
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0:  # caindo
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # subindo
                    self.rect.top = plat.rect.bottom
                    self.vel_y = 0


        # ---------------------------
        # COLISÃO COM O CHÃO DA TELA
        # ---------------------------
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA
            self.vel_y = 0
            self.on_ground = True

        # ---------------------------
        # LIMITES DA TELA
        # ---------------------------
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

        # Animação de pulo ativada apenas quando estiver no ar (subindo ou descendo)
            if self.vel_y != 0 and self.currentState not in ['ATTACK', 'JUMP']:
                self.currentState = 'JUMP'
        # ---------------------------
        # ANIMAÇÃO
        # ---------------------------
        self.selectAnimation()

        if self.previousState != self.currentState:
            self.animationIndex = 0

        self.image = self.currentAnimation[int(self.animationIndex)]

        # Ajusta hitbox dependendo da animação
        if self.currentState == 'IDLE':
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 44, 52)
        elif self.currentState == 'RUN':
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 40, 48)
        elif self.currentState == 'ATTACK':
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 88, 64)
        elif self.currentState == 'JUMP':
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 40, 52)


        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            self.animationIndex = 0
            self.currentState = 'IDLE'


    def draw(self, displaySurface):
        displaySurface.blit(self.image, self.rect)


    def selectAnimation(self):
        self.animationSpeed = ANIMSPEED_HERO_DEFAULT
        if self.currentState == 'IDLE':
            self.animationSpeed = ANIMSPEED_HERO_IDLE

        spriteSheet = self.spriteSheets[self.currentState]
        self.currentAnimation = spriteSheet.getSprites(flipped = not self.facingRight)


        

            

    def colisao_inimigo(self, enemies):
        hits = pygame.sprite.spritecollide(self, enemies, dokill=False)
        for enemy in enemies:   
          if enemy in hits:  # Verifica colisão
            if self.vel_y > 0 and not self.invulnerabilidade:
              return True, enemy  # Retorna True se houve colisão e o inimigo morreu
            
            elif not self.invulnerabilidade: 
                self.start_time = pygame.time.get_ticks() #Inicia o estado em que o player fica invulnerável            
                self.invulnerabilidade = True 
                self.vida -= 1 

        return False, None  # Retorna False se o inimigo não morreu ou se não houve colisão 
    
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

    def attack(self):
        sword_x = self.rect.x + (10 * self.vel_x)
        sword_y = self.rect.y - 15
        self.sword.activate(sword_x, sword_y, self.vel_x)
            
    def morte(self):
        if self.vida == 0:
            self.kill()