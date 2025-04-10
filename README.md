![image](https://github.com/user-attachments/assets/323c27aa-f845-4893-982a-e366e5c38885)# Projeto-IP-Equipe-8
# Titulo do trabalho
## Membros
Guilherme Cintra (gcucc), Thales Rafael (trcs), José Bruno (jbnos), Vitória das Dores (vdsn), Andrews Anaxceu (aags), Vinícius Lopes (vlf)

## Como o codigo foi organizado
Ha 3 funcoes basicas usadas para mudar telas entre o jogo: main_menu(), game() e play_again(). Alem da funcao quit_game(), usada para parar a execucao do programa. A funcao main_menu() é chamada sempre que o arquivo main.py é executado, as outras vão sendo chamadas ao decorrer do jogo, a depender de condições diferentes.

## Capturas de tela
![image](https://github.com/user-attachments/assets/f3e57b6e-40f6-45e5-b23c-18c8747e99c9)
![image](https://github.com/user-attachments/assets/ecce2676-1dbd-451d-8f9f-ebb36735a792)
![image](https://github.com/user-attachments/assets/962ae675-e297-446b-957c-c034d5f7c994)
![image](https://github.com/user-attachments/assets/b373bacc-5573-468d-b710-652f69ebfeb6)

## Ferramentas, bibliotecas e frameworks utilizados e razao

## Divisão de trabalho
  ### General (Andrews, Jose, Thales e Guilherme Cintra)
    - Andrews: [29/03]: Crie um código para servir como base para o projeto, adicionando um player, a movimentação do player, evitando que ele saia pelas laterais, ou suba demais. Além disso, adicionei as 3 plataformas utilizadas no jogo.
    - Andrews e Thales [31/03]: Adicionamos um background.
    - Andrews, José e Thales [07/04]: Como havia mais de uma branch e arquivos com o mesmo código, com pouquíssimas diferenças, unificamos os códigos para que o projeto ficasse mais fácil de entender.
    - Guilherme Cintra [09/04]: Agora o jogo reinicia quando o player mata 2 inimigos e coleta 3 moedas 
  ### Player (Thales)
    - Thales: [01/04: Melhorei a movimentação do player para evitar que ele atravessasse plataformas. Além disso, corrigi a lógica da colisão lateral do player com a plataforma, 
            que estava com alguns bugs.] 
            [03/04: Colisão do player com o inimigo foi adicionada, agora o inimigo só morre quando o player pula em cima dele.]
  
  ### Inimigos (Andrews e Thales)
    - Andrews [01/04]: Iniciei a classe inimigos, a sua movimentação na plataforma, e a lógica de matar o inimigo.
    - Andrews e Thales [01/04-02/04]: Correção de alguns bugs que aconteciam com a morte do inimigo. Ao utilizarmos o método self.kill(), o retangulo permanecia no jogo. Logo, ao chamarmos a função para verificar a colisão do jogador, o programa contava a sua morte mais de uma vez. 

  ### UI (Guilherme Cintra e Vitoria das Dores)
    - Guilherme Cintra: [07/04/25, inicio da implementacao de menus]
                      [09/04/25, organizacao dos arquivos]
                      [09/04/25, tela de replay]
    - Vitória das Dores: [02/04/25, Documento de Planjamento]
                       [09/04/25, Configuração e layout do Background]
                       [09/04/25, sprites da plataforma e dos inimigos]
    
  ### Coletáveis (Vinicius Lopes)
    - Vinícius Lopes: [08/04: Criei um novo coletável (as moedas) e inseri no main.py.]
                    [08/04: Criei um novo coletável (a vida) e inseri no main.py.]
                    [09/04: Corrigi alguns erros na função game(), no main.py (na parte das moedas) e no moedas.py, que estavam fazendo as moedas aparecerem infinitamente qaundo não eram coletadas (ficavam aparecendo moedas até que três tivessem sido coletadas).]
                    [09/04: Atualizei a lógica das vidas coletáveis dentro da função game() para que só aparecessem duas vidas ao longo da fase (com intervalo de 7 segundos do começo do jogo até a aparição da primeira vida e intervalo de 7 segundos entre uma vida e                           outra) e adicionei um placar que contabiliza as vidas coletadas.]
                    [09/04: Mudei o placar que mostrava a qauntidade de vidas coletadas para o total de vida do player.] 
                      
## Conceitos da disciplina no projeto

## Dificuldades e erros
