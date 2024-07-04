from math import floor

import pygame
import os
import random

LARG_TELA = 500
ALT_TELA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
IMAGEM_BG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 50)


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

        if self.contagem_imagem <= 15:
            self.imagem = self.IMGS[floor(self.contagem_imagem / 3)]
        else:
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
        pygame.mask.from_surface(self.imagem)
