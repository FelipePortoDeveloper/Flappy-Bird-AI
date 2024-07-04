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

