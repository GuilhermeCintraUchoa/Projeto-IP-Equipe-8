import pygame

pygame.init()

class SwordHitbox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, dano=1):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.active = False
        self.timer = 0
        self.dano = dano

    def activate(self, x, y, direction):
        if not direction:  # Para esquerda
            self.rect.topleft = (x - 20, y - 5)
        else:  # Para direita
            self.rect.topleft = (x + 30, y - 5)
        self.active = True
        self.timer = 10

    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.deactivate()

    def deactivate(self):
        self.active = False
