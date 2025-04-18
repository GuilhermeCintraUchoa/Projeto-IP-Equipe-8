import pygame
from settings import *
from Spritesheet import SpriteSheet


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



class Hero(pygame.sprite.Sprite):

    def __init__(self, position, faceRight):
        super().__init__()

        # Carrega SpriteSheets
        idleSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Idle/Idle-Sheet.png", idleSprites)
        runSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Run/Run-Sheet.png", runSprites)
        attackSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Attack-01/Attack-01-Sheet.png", attackSprites)
        deathSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Dead/Dead-Sheet.png", deathSprites)

        self.spriteSheets = {
            'IDLE'   : idleSpriteSheet,
            'RUN'    : runSpriteSheet,
            'ATTACK' : attackSpriteSheet,
            'DIE'    : deathSpriteSheet
        }

        self.animationIndex = 0
        self.facingRight = faceRight
        self.currentState = 'IDLE'
        self.xDir = 0
        self.speed = SPEED_HERO
        self.xPos = position[0]
        self.yPos = position[1]


    def update(self, level):
        self.previousState = self.currentState
        self.xDir = 0

        # key status
        if self.currentState != 'ATTACK' and self.currentState != 'DIE':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.currentState = 'ATTACK'
            elif keys[pygame.K_LEFT]:
                self.xDir = -1
                self.facingRight = False
                self.currentState = 'RUN'
            elif keys[pygame.K_RIGHT]:
                self.xDir = 1
                self.facingRight = True
                self.currentState = 'RUN'
            else:
                self.currentState = 'IDLE'

        # Seleciona a imagem para o estado atual (idle, run, jump, fall, etc.)
        self.selectAnimation()

        # Começa a animação do início
        if self.previousState != self.currentState:
            self.animationIndex = 0

        # Seleciona a imagem
        self.image = self.currentAnimation[int(self.animationIndex)]

        # Seleciona o tamanho do rect dependendo da animação
        # (xPos, yPos) =posição bottom-center do sprite
        if self.currentState == 'IDLE':
            self.rect = pygame.Rect(self.xPos - 22, self.yPos - 52, 44, 52)
        elif self.currentState == 'RUN':
            self.rect = pygame.Rect(self.xPos - 20, self.yPos - 48, 40, 48)
        elif self.currentState == 'ATTACK':
            self.rect = pygame.Rect(self.xPos - 44, self.yPos - 64, 88, 64)
        elif self.currentState == 'DIE':
            self.rect = pygame.Rect(self.xPos - 32, self.yPos - 48, 64, 48)

        # Roda a animação até que a animação chegue ao fim
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            if self.currentState == 'DIE':
                self.animationIndex = len(self.currentAnimation) - 1
            else:
                self.animationIndex = 0
                self.currentState = 'IDLE'

        self.moveHorizontal(level)

        # Lica com colisão com inimigos
        self.checkEnemyCollisions(level.bees)


    def selectAnimation(self):
        self.animationSpeed = ANIMSPEED_HERO_DEFAULT
        if self.currentState == 'IDLE':
            self.animationSpeed = ANIMSPEED_HERO_IDLE

        spriteSheet = self.spriteSheets[self.currentState]
        self.currentAnimation = spriteSheet.getSprites(flipped = not self.facingRight)


    def die(self):
        if self.currentState != 'DIE':
            self.currentState = 'DIE'
            self.animationIndex = 0


    def checkEnemyCollisions(self, enemies):
        # CHeca por colisões entre o jogador e todos os inimigos no spritegroup
        collidedSprites = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in collidedSprites:
            if self.currentState == 'ATTACK':
                if self.facingRight == True:
                    if enemy.rect.left < self.rect.right - 30:
                        enemy.die()
                else:
                    if enemy.rect.right > self.rect.left + 30:
                        enemy.die()
            else:
                if enemy.currentState != 'DYING':
                    if self.rect.left < enemy.rect.left:  # Colisão no lado direito
                        if self.rect.right > enemy.rect.left + 16:
                            self.die()
                    elif self.rect.right > enemy.rect.right:  # Colisão no lado esquerdo
                        if self.rect.left < enemy.rect.right - 16:
                            self.die()