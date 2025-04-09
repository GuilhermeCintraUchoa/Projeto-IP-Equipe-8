import pygame

pygame.init()

class SwordHitbox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, dano=1):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.active = False
        self.timer = 0
        self.dano = dano

    def activate(self, x, y, direction):
        if direction < 0:  # Para esquerda
            self.rect.topleft = (x - 40, y - 10)
        else:  # Para direita
            self.rect.topleft = (x + 40, y - 10)
        self.active = True
        self.timer = 10

    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.deactivate()

    def deactivate(self):
        self.active = False
