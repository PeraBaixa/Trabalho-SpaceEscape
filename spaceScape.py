##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.3                      ###
##############################################################
### Objetivo: desviar dos meteoros que caem.               ###
### Cada colisão tira uma vida. Sobreviva o máximo que     ###
### conseguir!                                             ###
##############################################################
### Prof. Filipo Novo Mor - github.com/ProfessorFilipo     ###
##############################################################
import sys
from turtle import Screen

from pygame.time import Clock

import Jogador

import pygame
import random
import os

# Inicializa o PyGame
pygame.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS DO JOGO
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape")
metQunt = 5
logado = False

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS (os alunos podem trocar os arquivos aqui)
# ----------------------------------------------------------
# Dica: coloque as imagens e sons na mesma pasta do arquivo .py
# e troque apenas os nomes abaixo.

ASSETS = {
    "backmenu": "Background_menu.png",                          # imagem de fundo do menu
    "background": "fundo_espacial.png",                         # imagem de fundo do primeiro nível
    "player": "nave001.png",                                    # imagem da nave
    "meteor": "meteoro001.png",                                 # imagem do meteoro
    "sound_point": "classic-game-action-positive-5-224402.mp3", # som ao desviar com sucesso
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",                # som de colisão
    "music": "game-gaming-background-music-385611.mp3"          # música de fundo. direitos: Music by Maksym Malko from Pixabay
}

# ----------------------------------------------------------
# 🖼️ CARREGAMENTO DE IMAGENS E SONS
# ----------------------------------------------------------
# Cores para fallback (caso os arquivos não existam)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
YELLOW = (255, 255, 0)
RED = (255, 60, 60)
BLUE = (60, 100, 255)

# Tela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Função auxiliar para carregar imagens de forma segura
def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    else:
        # Gera uma superfície simples colorida se a imagem não existir
        surf = pygame.Surface(size or (50, 50))
        surf.fill(fallback_color)
        return surf

# Carrega imagens
background = load_image(ASSETS["backmenu"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))

# Sons
def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])

# Música de fundo (opcional)
if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(-1)  # loop infinito

# ----------------------------------------------------------
# 🧠 VARIÁVEIS DE JOGO
# ----------------------------------------------------------
player_speed = 7

def criaMeteoros():
    meteor_list = []
    for _ in range(metQunt):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-500, -40)
        meteor_list.append(pygame.Rect(x, y, 40, 40))
    return meteor_list

font = pygame.font.Font(None, 36)
fontmenu = pygame.font.Font(None, 50)
clock = pygame.time.Clock()


#bloco de códigos pra testes de tela



# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
def fase1():
    meteor_speed = 5
    meteor_list = criaMeteoros()

    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    ponto = 1
    score = 0
    lives = 3

    back = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
    fontpausa = pygame.font.Font(None, 42)
    pausado = False

    running = True
    while running:
        clock.tick(FPS)
        screen.blit(back, (0, 0))

        # --- Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Movimento do jogador ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0 and not pausado:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH and not pausado:
            player_rect.x += player_speed
        #Tela de pausa
        if keys[pygame.K_ESCAPE]:
            if pausado:
                pausado = False
            else:
                pausado = True


        # --- Movimento dos meteoros ---
        if not pausado:
            for meteor in meteor_list:
                meteor.y += meteor_speed

                # Saiu da tela → reposiciona e soma pontos
                if meteor.y > HEIGHT:
                    meteor.y = random.randint(-100, -40)
                    meteor.x = random.randint(0, WIDTH - meteor.width)
                    score += ponto
                    if sound_point:
                        sound_point.play()

                # Colisão
                if meteor.colliderect(player_rect):
                    lives -= 1
                    meteor.y = random.randint(-100, -40)
                    meteor.x = random.randint(0, WIDTH - meteor.width)
                    if sound_hit:
                        pygame.mixer.music.set_volume(0)
                        sound_hit.play()
                    if lives <= 0:
                        running = False

        # --- Desenha tudo ---
        screen.blit(player_img, player_rect)
        for meteor in meteor_list:
            screen.blit(meteor_img, meteor)

        # --- Exibe pontuação e vidas ---
        text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
        screen.blit(text, (10, 10))

        #Tela de pausa
        if pausado:
            pausa = fontpausa.render("Pausa", True, WHITE)
            screen.blit(pausa, (int(WIDTH * 0.2), int(HEIGHT * 0.4)))

        #Aumenta a dificuldade automaticamente
        if score > 50 and score < 75:
            meteor_speed = 6
        elif score >= 75 and score < 100:
            meteor_speed = 7
            ponto = 2
        elif score >= 150 and score < 200:
            meteor_speed = 8
            ponto = 3
        elif score >= 200 and score < 300:
            meteor_speed = 9
            ponto = 4
        elif score >= 300:
            ponto = 5
            meteor_speed = 10

        pygame.display.flip()
    telaFim(score)

    if Jogador.recordes[0] < score:
        Jogador.recordes[0] = score

def fase2():
    meteor_speed = 5
    meteor_list = criaMeteoros()

    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    objetivo = 100 #alvo de score
    score = 0
    lives = 3

    back = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
    fontpausa = pygame.font.Font(None, 42)
    pausado = False

    venceu = False
    relogio = 300
    frames = 1

    running = True
    while running:
        clock.tick(FPS)
        screen.blit(back, (0, 0))
        
        # --- Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Movimento do jogador ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0 and not pausado:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH and not pausado:
            player_rect.x += player_speed
        #Tela de pausa
        if keys[pygame.K_ESCAPE]:
            if pausado:
                pausado = False
            else:
                pausado = True


        # --- Movimento dos meteoros ---
        if not pausado:
            for meteor in meteor_list:
                meteor.y += meteor_speed

                # Saiu da tela → reposiciona e soma pontos
                if meteor.y > HEIGHT:
                    meteor.y = random.randint(-100, -40)
                    meteor.x = random.randint(0, WIDTH - meteor.width)
                    score += 1
                    if sound_point:
                        sound_point.play()
                        pygame.mixer.music.set_volume(0)

                # Colisão
                if meteor.colliderect(player_rect):
                    lives -= 1
                    meteor.y = random.randint(-100, -40)
                    meteor.x = random.randint(0, WIDTH - meteor.width)
                    if sound_hit:
                        sound_hit.play()
                    if lives <= 0:
                        running = False

        # --- Desenha tudo ---
        screen.blit(player_img, player_rect)
        for meteor in meteor_list:
            screen.blit(meteor_img, meteor)

        # --- Exibe pontuação e vidas ---
        text = font.render(f"Pontos: {score}\\{objetivo}   Vidas: {lives}", True, WHITE)
        screen.blit(text, (10, 10))
        # Coloca o relógio na tela
        relog = font.render(f"{relogio}", True, WHITE)
        relogloc = relog.get_rect()
        relogloc.topright = (WIDTH, 0)
        screen.blit(relog, relogloc)
        frames += 1

        #decrementa o relógio
        if frames == 60:
            relogio -= 1
            frames = 1

        #Tela de pausa
        if pausado:
            pausa = fontpausa.render("Pausa", True, WHITE)
            screen.blit(pausa, (int(WIDTH * 0.2), int(HEIGHT * 0.4)))
        
        if relogio == 0:
            running = False

        if score >= objetivo:
            venceu = True
            running = False

        pygame.display.flip()
    
    if venceu:
        telaRes(f"Você cumpriu o desafio com {relogio} segundos restando", True)
        if Jogador.recordes[1] > relogio:
            Jogador.recordes[1] = relogio
    else:
        telaRes(f"O tempo acabou faltando {objetivo-score} pontos para vencer", False)

def fase3():
    meteor_speed = 5
    back = load_image(ASSETS['background'], WHITE, (WIDTH // 2, HEIGHT))

    player_men = load_image(ASSETS["player"], BLUE, (40, 30))
    player1loc = player_men.get_rect(center=(WIDTH // 4, HEIGHT - 60))
    player2loc = player_men.get_rect(center=(WIDTH * 3 // 4, HEIGHT - 60))

    vidas = [3, 3]
    points = [0, 0]

    met1 = criaMeteoros()
    met2 = criaMeteoros()

    fontpausa = pygame.font.Font(None, 42)
    fontmet = pygame.font.Font(None, 18)
    pausado = False

    running = True
    while running:
        clock.tick(FPS)
        screen.blit(back, (0, 0))
        screen.blit(back, (WIDTH//2, 0))
        pygame.draw.line(screen, (0, 0, 0), (WIDTH//2, 0), (WIDTH//2, HEIGHT), 4)

        # --- Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # controla o movimento dos jogadores:
        # Player 1, na tela da esquerda
        if pygame.key.get_pressed()[pygame.K_a] and player1loc.x > 0:
            player1loc.x -= player_speed
        if pygame.key.get_pressed()[pygame.K_d] and player1loc.x < WIDTH // 2 - 80:
            player1loc.x += player_speed

        # Player 2, na tela da direita
        if pygame.key.get_pressed()[pygame.K_LEFT] and player2loc.x > WIDTH // 2:
            player2loc.x -= player_speed
        if pygame.key.get_pressed()[pygame.K_RIGHT] and player2loc.x < WIDTH - 80:
            player2loc.x += player_speed

        #Tela de pausa
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            if pausado:
                pausado = False
            else:
                pausado = True


        # --- Movimento dos meteoros ---
        if not pausado:
            for meteor in (met1 + met2):
                meteor.y += meteor_speed

                # Saiu da tela → reposiciona e soma pontos
                if meteor.y > HEIGHT:
                    meteor.y = random.randint(-100, -40)
                    meteor.x = random.randint(0, WIDTH - meteor.width)

                    i = (0 if meteor in met1 else 1)
                    points[i] +=1

                    if sound_point:
                        sound_point.play()

                # Colisão
                if meteor.colliderect(player1loc) or meteor.colliderect(player2loc):
                    i = (0 if meteor.colliderect(player1loc) else 1)
                    vidas[i] -= 1
                    meteor.y = random.randint(-100, -40)
                    meteor.x = random.randint(0, WIDTH - meteor.width)
                    if sound_hit:
                        sound_hit.play()
                    if 0 in vidas:
                        running = False

        # --- Desenha tudo ---
        screen.blit(player_men, player1loc)
        screen.blit(player_men, player2loc)
        for meteor in (met1 + met2):
            screen.blit(meteor_img, meteor)

        # --- Exibe pontuação e vidas ---
        placar = [
            fontmet.render(f"Pontos: {points[0]}   Vidas: {vidas[0]}", True, WHITE),
            fontmet.render(f"Pontos: {points[1]}   Vidas: {vidas[1]}", True, WHITE)
        ]
        screen.blit(placar[0], (10, 10))
        screen.blit(placar[1], (WIDTH // 2 + 10, 10))

        #Tela de pausa
        if pausado:
            pausa = fontpausa.render("Pausa", True, WHITE)
            screen.blit(pausa, (int(WIDTH * 0.2), int(HEIGHT * 0.4)))

        pygame.display.flip()

    telaRes(f"{"Jogador 1" if vidas[0] > 0 else "Jogador 2"} venceu!", True)

def recordes():
    recs1, recs2 = Jogador.pegaRecordes()
    fase = 1
    fontmenor = pygame.font.Font(None, 30)

    while True:
        clock.tick(15)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        lista = (recs1 if fase == 1 else recs2)
        nomet = ("COMBATE INFINITO" if fase == 1 else "DESAFIO DE TEMPO")
        titulo = font.render(f"RECORDES - {nomet}", True, WHITE)
        screen.blit(titulo, titulo.get_rect(center=(WIDTH//2, HEIGHT//20)))

        locpri = HEIGHT//20+36
        for jog in lista:
            linha = fontmenor.render(f"{jog["nome"]} - {jog["reco"]}", True, YELLOW)
            screen.blit(linha, linha.get_rect(center=(WIDTH//2, locpri)))
            locpri += 30

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            fase = 2
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            fase = 1
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            break

        pygame.display.flip()

def logar():
    global logado
    nome = ""
    while True:
        clock.tick(13)
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, WHITE, (WIDTH // 4, HEIGHT // 2 - 20, WIDTH // 2, 40))
        n = font.render(nome, True, BLACK)
        screen.blit(n, (WIDTH // 4 + 10, HEIGHT // 2 - 12))

        if True in (letra := pygame.key.get_pressed()):
            for l in "abcdefghijklmnopqrstuvwxyz":
                if letra[pygame.key.key_code(l)]:
                    nome += l

            if letra[pygame.K_BACKSPACE]:
                nome = nome[:-2]

            if letra[pygame.K_RETURN] and nome != "":
                logado = True
                Jogador.achaJog(nome)
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()

# ----------------------------------------------------------
# 🏁 TELA DE FIM DE JOGO
# ----------------------------------------------------------
def telaFim(score):
    pygame.mixer.music.stop()
    screen.fill((20, 20, 20))
    end_text = font.render("Fim de jogo! Pressione qualquer tecla para sair.", True, WHITE)

    final_score = font.render(f"Pontuação final: {score}", True, WHITE)
    screen.blit(end_text, (150, 260))
    screen.blit(final_score, (300, 300))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def telaRes(msg, vit):
    vicDer = ("VITÓRIA" if vit else "DERROTA")

    pygame.mixer.music.stop()
    screen.fill((20, 20, 20))
    fonteMenor = pygame.font.Font(None, 22)
    qlqtTecla = fonteMenor.render("Pressione qualquer tecla para sair", True, WHITE)
    loc = qlqtTecla.get_rect()
    loc.center = (WIDTH//2, HEIGHT-30)
    screen.blit(qlqtTecla, loc)

    fonteGrande = pygame.font.Font(None, 60)
    vitoria = fonteGrande.render(vicDer, True, WHITE)
    loc = vitoria.get_rect()
    loc.center = (WIDTH//2, HEIGHT//2)
    screen.blit(vitoria, loc)

    mensagem = font.render(msg, True, WHITE)
    loc = mensagem.get_rect()
    loc.center = (WIDTH//2, HEIGHT//2+60)
    screen.blit(mensagem, loc)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

#Loop do menu
opt = 0
lig = [False, 1]
fontusu = pygame.font.Font(None, 20)
while True:
    clock.tick(12)
    screen.blit(background, (0, 0))

    if lig[1] == 6:
        lig[0] = (False if lig[0] else True)
        lig[1] = 1

    lig[1] += 1
    prim = fontmenu.render("Combate infinito", True, WHITE)
    segu = fontmenu.render("Desafio de tempo", True, (WHITE if Jogador.recordes[0] > 0 else GREY))
    terc = fontmenu.render("Duelo entre jogadores", True, (WHITE if Jogador.recordes[1] < 300 else GREY))
    reco = fontmenu.render("Recordes", True, WHITE)
    logi = fontmenu.render(("Deslogar" if logado else "logar"), True, WHITE)
    sair = fontmenu.render("Sair", True, WHITE)
    screen.blit(prim, prim.get_rect(center=(WIDTH//2, 130)))
    screen.blit(segu, segu.get_rect(center=(WIDTH//2, 180)))
    screen.blit(terc, terc.get_rect(center=(WIDTH//2, 230)))
    screen.blit(reco, reco.get_rect(center=(WIDTH//2, 280)))
    screen.blit(logi, logi.get_rect(center=(WIDTH//2, 330)))
    screen.blit(sair, sair.get_rect(center=(WIDTH//2, 380)))

    rectopt = None
    match opt:
        case 0:
            rectopt = prim.get_rect(center=(WIDTH//2, 130))
        case 1:
            rectopt = segu.get_rect(center=(WIDTH//2, 180))
        case 2:
            rectopt = terc.get_rect(center=(WIDTH//2, 230))
        case 3:
            rectopt = reco.get_rect(center=(WIDTH // 2, 280))
        case 4:
            rectopt = logi.get_rect(center=(WIDTH//2, 330))
        case 5:
            rectopt = sair.get_rect(center=(WIDTH//2, 380))
    if lig[0]:
        pygame.draw.rect(screen, (255, 255, 255, 20), rectopt)

    escape = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            escape = True
    if escape:
        break
    
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        opt += 1
        if opt == 1 and Jogador.recordes[0] == 0: opt += 2
        elif opt == 2 and Jogador.recordes[1] == 300: opt += 1
        if opt > 5:
            opt = 0

    if pygame.key.get_pressed()[pygame.K_UP]:
        opt -= 1
        if opt == 1 and Jogador.recordes[0] == 0: opt -= 1
        elif opt == 2 and Jogador.recordes[1] == 300: opt -= (1 if Jogador.recordes[0] != 0 else 2)
        if opt < 0: opt = 5

    if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
        match opt:
            case 0:
                fase1()
            case 1:
                fase2()
            case 2:
                fase3()
            case 3:
                recordes()
            case 4:
                if logado:
                    Jogador.nome = "anônimo"
                    Jogador.recordes = [0,300]
                    Jogador.usuNovo = True
                else:
                    logar()
                    print(Jogador.recordes)
            case 5:
                if logado: Jogador.salvar()
                break

    #Desenha a parte do usuário
    recs = Jogador.recordes
    nick = fontusu.render((Jogador.nome if logado else "Anônimo"), True, WHITE)
    recs = fontusu.render(f"{recs[0] if recs[0] > 0 else "-"}|{recs[1] if recs[1] < 300 else "-"}", True, WHITE)
    screen.blit(nick, nick.get_rect(topright=(WIDTH, 0)))
    screen.blit(recs, recs.get_rect(topright=(WIDTH, 20)))

    pygame.display.flip()

pygame.quit()