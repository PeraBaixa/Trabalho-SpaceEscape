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

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS (os alunos podem trocar os arquivos aqui)
# ----------------------------------------------------------
# Dica: coloque as imagens e sons na mesma pasta do arquivo .py
# e troque apenas os nomes abaixo.

ASSETS = {
    "backmenu": "Background_menu.png",                                             # imagem de fundo do menu
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
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
player_speed = 7

meteor_list = []
for _ in range(metQunt):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-500, -40)
    meteor_list.append(pygame.Rect(x, y, 40, 40))

score = 0
lives = 3
font = pygame.font.Font(None, 36)
fontmenu = pygame.font.Font(None, 50)
clock = pygame.time.Clock()

# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
def fase1():
    global score, lives
    meteor_speed = 5

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
                running = False

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
        elif score >= 150 and score < 200:
            meteor_speed = 8
        elif score >= 200 and score < 300:
            meteor_speed = 9
        elif score >= 300:
            meteor_speed = 10

        pygame.display.flip()
    telaFim()

def fase2():
    global score, lives
    meteor_speed = 5

    objetivo = 10 #alvo de score
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
                running = False

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
    else:
        telaRes(f"O tempo acabou faltando {objetivo-score} para vencer")
# ----------------------------------------------------------
# 🏁 TELA DE FIM DE JOGO
# ----------------------------------------------------------
def telaFim():
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
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
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

while True:
    clock.tick(10)
    screen.blit(background, (0, 0))

    if lig[1] == 5:
        lig[0] = (False if lig[0] else True)
        lig[1] = 1

    lig[1] += 1
    prim = fontmenu.render("Fase 1", True, WHITE)
    segu = fontmenu.render("Fase 2", True, WHITE)
    terc = fontmenu.render("Fase 3", True, WHITE)
    sair = fontmenu.render("Sair", True, WHITE)
    screen.blit(prim, (320, 180))
    screen.blit(segu, (320, 230))
    screen.blit(terc, (320, 280))
    screen.blit(sair, (320, 330))

    rectopt = None
    match opt:
        case 0:
            rectopt = prim.get_rect()
            rectopt.topleft = (320, 180)
        case 1:
            rectopt = segu.get_rect()
            rectopt.topleft = (320, 230)
        case 2:
            rectopt = terc.get_rect()
            rectopt.topleft = (320, 280)
        case 3:
            rectopt = sair.get_rect()
            rectopt.topleft = (320, 330)
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
        if opt > 3:
            opt = 0
    if pygame.key.get_pressed()[pygame.K_UP]:
        opt -= 1
        if opt < 0: opt = 3

    if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
        match opt:
            case 0:
                fase1()
            case 1:
                fase2()
            case 2:
                pass
            case 3:
                break


    pygame.display.flip()

pygame.quit()