import pygame
import os
import random
import neat
from math import sqrt

# Mudar para True se quiser a IA jogando ou para False se quiser jogar
ai_jogando = True
hard = False

geracao = 0

LARG_TELA = 500
ALT_TELA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
IMAGEM_BG = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "part0.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "part1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "part2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "part3.png")))
]
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 25)


class Passaro:
    # Constantes

    IMGS = IMAGENS_PASSARO

    # Animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    # Atributos

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    # Funções

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # Calcular deslocamento

        self.tempo += 1

        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        # Restringir deslocamento

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # Angulo do Passaro

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # Definir imagem passaro

        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # Controlar batida de asa se caindo

        if self.angulo < -80:
            self.imagem = self.IMGS[1]

        # Desenhar a imagem

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_img = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_img)

        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    # Constantes

    DISTANCIA = 200
    VELOCIDADE = 5
    MAX_Y = 50
    MIN_Y = 450

    # Atributos

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()
        self.velocidade_y = random.choice([-2, 2])

    # Funções

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

        if hard:

            if self.pos_topo + self.CANO_TOPO.get_height() <= self.MAX_Y:
                self.velocidade_y = 2
            if self.pos_base - self.DISTANCIA >= self.MIN_Y:
                self.velocidade_y = -2

            self.pos_topo += self.velocidade_y
            self.pos_base += self.velocidade_y
            self.altura += self.velocidade_y

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if topo_ponto or base_ponto:
            return True
        else:
            return False


class Chao:
    # Constantes

    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    # Atributos

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    # Funções

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


class BG:

    def __init__(self):
        self.nuvem_x0 = 0
        self.nuvem_x1 = IMAGEM_BG[1].get_width()

        self.velocidade_nuvem = 1

        self.predios_x0 = 0
        self.predios_x1 = IMAGEM_BG[2].get_width()

        self.velocidade_predios = 3

        self.grama_x0 = 0
        self.grama_x1 = IMAGEM_BG[3].get_width()

        self.velocidade_grama = 4

    def mover(self):

        self.nuvem_x0 -= self.velocidade_nuvem
        self.nuvem_x1 -= self.velocidade_nuvem

        if self.nuvem_x0 + IMAGEM_BG[1].get_width() < 0:
            self.nuvem_x0 = self.nuvem_x1 + IMAGEM_BG[1].get_width()
        if self.nuvem_x1 + IMAGEM_BG[1].get_width() < 0:
            self.nuvem_x1 = self.nuvem_x0 + IMAGEM_BG[1].get_width()

        self.predios_x0 -= self.velocidade_predios
        self.predios_x1 -= self.velocidade_predios

        if self.predios_x0 + IMAGEM_BG[2].get_width() < 0:
            self.predios_x0 = self.predios_x1 + IMAGEM_BG[2].get_width()
        if self.predios_x1 + IMAGEM_BG[2].get_width() < 0:
            self.predios_x1 = self.predios_x0 + IMAGEM_BG[2].get_width()

        self.grama_x0 -= self.velocidade_grama
        self.grama_x1 -= self.velocidade_grama

        if self.grama_x0 + IMAGEM_BG[3].get_width() < 0:
            self.grama_x0 = self.grama_x1 + IMAGEM_BG[3].get_width()
        if self.grama_x1 + IMAGEM_BG[3].get_width() < 0:
            self.grama_x1 = self.grama_x0 + IMAGEM_BG[3].get_width()

    def desenhar_bg(self, tela):

        tela.blit(IMAGEM_BG[0], (0, 0))

        tela.blit(IMAGEM_BG[1], (self.nuvem_x0, -200))
        tela.blit(IMAGEM_BG[1], (self.nuvem_x1, -200))

        tela.blit(IMAGEM_BG[2], (self.predios_x0, -250))
        tela.blit(IMAGEM_BG[2], (self.predios_x1, -250))

        tela.blit(IMAGEM_BG[3], (self.grama_x0, -250))
        tela.blit(IMAGEM_BG[3], (self.grama_x1, -250))


def desenhar_tela(tela, passaros, canos, chao, pontuacao, bg):
    bg.desenhar_bg(tela)

    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    chao.desenhar(tela)

    pontos_texto = FONTE_PONTOS.render(f"Pontuação: {pontuacao}", True, (255, 255, 255))
    tela.blit(pontos_texto, (LARG_TELA - 10 - pontos_texto.get_width(), 10))

    if ai_jogando:
        geracao_texto = FONTE_PONTOS.render(f"Geração: {geracao}", True, (255, 255, 255))
        tela.blit(geracao_texto, (10, 10))

    pygame.display.update()


def distancia(x0, x1, y0, y1):
    x = (x1 - x0) ** 2
    y = (y1 - y0) ** 2

    return sqrt(x + y)


def main(genomas, config):  #fitness function

    global geracao
    geracao += 1

    if ai_jogando:

        redes = []
        lista_genomas = []
        passaros = []

        for _, genoma in genomas:
            # adicionando o passaro

            passaros.append(Passaro(230, 350))

            # adicionando o genoma do passaro

            genoma.fitness = 0
            lista_genomas.append(genoma)

            # adicionando a rede neural do passaro

            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)



    else:
        passaros = [Passaro(230, 350)]

    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((LARG_TELA, ALT_TELA))
    bg = BG()
    pontos = 0
    relogio = pygame.time.Clock()

    pygame.display.set_caption("Flappy AI")
    pygame.display.set_icon(IMAGENS_PASSARO[0])

    rodando = True

    while rodando:

        relogio.tick(30)

        # Criando interação com o jogo

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

            # Permitindo ou negando a interação do usuário

            if not ai_jogando:

                # Acão do jogador (apertar espaço)

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

                # Acão do jogador (clickar no mouse)

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        for passaro in passaros:
                            passaro.pular()

        # Decidindo para onde a IA deve olhar

        indice_cano = 0

        if len(passaros) > 0:
            # Descobrir qual cano olhar

            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()):
                indice_cano = 1

        else:
            rodando = False
            break

        # mover as coisas

        adicionar_cano = False
        remover_canos = []

        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)

                    # punir passaro

                    if ai_jogando:
                        lista_genomas[i].fitness -= 1
                        lista_genomas.pop(i)
                        redes.pop(i)

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True

            cano.mover()

            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:

            pontos += 1
            canos.append(Cano(600))

            # recompensar passaro

            if ai_jogando:
                for genoma in lista_genomas:
                    genoma.fitness += 5

        for i, passaro in enumerate(passaros):
            passaro.mover()

            # pontuar o passaro por andar

            lista_genomas[i].fitness += 0.1

            # deixando a IA controlar o passaro

            # versão curso (distancia contando apenas o y)

            # output = redes[i].activate(passaro.y,
            #                            abs(passaro.y - canos[indice_cano].altura),
            #                            abs(passaro.y - canos[indice_cano].pos_base))

            # minha versão (distancia contando com o x)

            output = redes[i].activate(
                (
                    passaro.y,
                    abs(distancia(passaro.x, canos[indice_cano].x, passaro.y, canos[indice_cano].altura)),
                    abs(distancia(passaro.x, canos[indice_cano].x, passaro.y, canos[indice_cano].pos_base))
                ))

            if output[0] > 0.5:
                passaro.pular()

        bg.mover()
        chao.mover()

        for cano in remover_canos:
            canos.remove(cano)
            remover_canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

                if ai_jogando:
                    lista_genomas[i].fitness -= 0.5
                    lista_genomas.pop(i)
                    redes.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos, bg)


def rodar(caminho_config):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, caminho_config)

    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    if ai_jogando:
        populacao.run(main, 50)
    else:
        main(None, None)

    pass


if __name__ == "__main__":
    caminho = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho, "config.txt")

    rodar(caminho_config)
