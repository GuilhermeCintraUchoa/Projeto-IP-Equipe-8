# Projeto-IP-Equipe-8
# Titulo do trabalho
## Membros
Guilherme Cintra <gcucc>, Thales Rafael <trcs>, José Bruno <jbnos>, Vitória das Dores <vdsn>, Andrews Anaxceu <aags>, Vinícius Lopes <vlf>

# Divisão de trabalho
  ## General

    Andrews: [29/03]: Crie um código para servir como base para o projeto, adicionando um player, a movimentação do player, evitando que ele saia pelas laterais, ou suba demais. Além disso, adicionei as 3 plataformas utilizadas no jogo.

    Andrews e Thales [31/03]: Adicionamos um background.

    Andrews, José e Thales [07/04]: Como havia mais de uma branch e arquivos com o mesmo código, com pouquíssimas diferenças, unificamos os códigos para que o projeto ficasse mais fácil de entender.
  ## player

    Thales: [01/04: Melhorei a movimentação do player para evitar que ele atravessasse plataformas. Além disso, corrigi a lógica da colisão lateral do player com a plataforma, 
            que estava com alguns bugs.] 
            [03/04: Colisão do player com o inimigo foi adicionada, agora o inimigo só morre quando o player pula em cima dele.]
  
  ## Inimigos
    Andrews [01/04]: Iniciei a classe inimigos, a sua movimentação na plataforma, e a lógica de matar o inimigo.
    
    Andrews e Thales [01/04-02/04]: Correção de alguns bugs que aconteciam com a morte do inimigo. Ao utilizarmos o método self.kill(), o retangulo permanecia no jogo. Logo, ao chamarmos a função para verificar a colisão do jogador, o programa contava a sua morte mais de uma vez. 

  ## UI
    Guilherme Cintra: 07/04/25, inicio da implementacao de menus
  ## coletáveis
    Vinícius Lopes: [08/04: Criei um novo coletável (as moedas) e inseri no main.py.]
                    [08/04: Criei um novo coletável (a vida) e inseri no main.py.]
