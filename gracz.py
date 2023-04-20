# Kamil Balcerzak

import pygame

class Gracz:
    pozycja = pygame.Vector2() # wektor dwuwymiarowy
    pozycja.xy = 295, 0
    predkosc = pygame.Vector2()
    predkosc.xy = 3, 0
    przyspieszenie = 0.1
    prawoObiekt = pygame.image.load('data/png/gracz.png')
    lewoObiekt = pygame.transform.flip(prawoObiekt, True, False)
    aktualnyObiekt = prawoObiekt