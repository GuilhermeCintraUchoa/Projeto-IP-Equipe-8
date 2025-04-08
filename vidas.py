import pygame
import random

class Vida:
    def __init__(self):
        # Cria a superfície com canal alpha para permitir transparência
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

        # Desenha um coração estilizado (simples)
        pygame.draw.circle(self.image, (255, 100, 100), (10, 10), 10)
        pygame.draw.circle(self.image, (255, 100, 100), (20, 10), 10)
        pygame.draw.polygon(self.image, (255, 100, 100), [(0, 15), (30, 15), (15, 30)])

        # Retângulo da posição
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 770)
        self.rect.y = 0

    def cair(self):
        self.rect.y += 2

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

    def verificar_colisao(self, jogador_rect):
        return self.rect.colliderect(jogador_rect)