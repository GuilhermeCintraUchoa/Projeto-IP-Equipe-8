import random
import pygame
from settings import LARGURA, ALTURA

DOURADO = (255, 223, 0)

# Criando a classe Moeda
class Moeda:
    def __init__(self):
        self.x = random.randint(0, LARGURA - 50)  # Posição aleatória no topo
        self.y = -50  # Começa acima da tela
        self.velocidade = 2
        self.coletada = False

    def cair(self):
        if not self.coletada:
            self.y += self.velocidade
            if self.y > ALTURA:
                self.reset()
    # Aparência da moeda
    def desenhar(self, surface):
        coletada = 0
        if (not self.coletada) and (coletada <= 3):
            pygame.draw.circle(surface, DOURADO, (self.x, self.y), 15)
            coletada+=1

    def verificar_colisao(self, jogador_rect):
        moeda_rect = pygame.Rect(self.x - 15, self.y - 15, 30, 30)  
        if jogador_rect.colliderect(moeda_rect):
            self.coletada = True
            return True
        return False

    def reset(self):
        self.coletada = False
        self.x = random.randint(0, LARGURA - 50)
        self.y = -50
