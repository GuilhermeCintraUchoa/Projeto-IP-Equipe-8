import pygame 

class Player:
    def __init__(self, x_player, y_player):
        self.hp = 100 
        self.velocidade = 10
        self.x = x_player
        self.y = y_player
        self.quadrado = pygame.Rect(self.x, self.y, 20, 20) 

    def mover(self, largura_mapa):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.y -= 40 
        if key[pygame.K_a]:
            self.x -= self.velocidade 
        if key[pygame.K_d] and ((self.x + 10) > (largura_mapa / 2) or (self.x + 10) < (largura_mapa / 2)):
            self.x += self.velocidade 

        self.quadrado.x = self.x
        self.quadrado.y = self.y

    def gravidade(self):
        self.y += 10
        self.quadrado.y = self.y
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, (0, 255, 0), self.quadrado)

