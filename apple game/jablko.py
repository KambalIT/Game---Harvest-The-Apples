# Kamil Balcerzak

import pygame
class Jablko: 
    def __init__(self): # konstruktor 
        self.obiekt = pygame.image.load('data/png/jablko.png')
        self.pozycja = pygame.Vector2()

        # self to zmienna globalna która gdy zostanie zdefiniowana staje się widoczna w każdej metodzie klasy