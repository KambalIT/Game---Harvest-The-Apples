# Kamil Balcerzak

import pygame, sys, time, random
from pygame.locals import * # import biblioteki klawiszy
from gracz import Gracz
from tlo import Tlo
from jablko import Jablko
from narzedzia import klamra
from narzedzia import sprawdzanieKolizji


def main():
    pygame.init() # metoda init ładuje moduły PyGame odpowiedzialne m.in za dźwięk czy grafikę i jest podstawą każdej apliakcji korzystajacej z tej biblioteki
    DISPLAY=pygame.display.set_mode((640,480)) # 640x480 rozdzielczość ekranu gry
    pygame.display.set_caption('Gra')
    czcionka = pygame.font.Font('data/czcionki/czcionka.otf', 32) # rozmiar czcionki
    interfejs = pygame.image.load('data/png/interfejs.png')
    interfejs_motyw = pygame.image.load('data/png/interfejs_motyw.png')
    reset_przycisk = pygame.image.load('data/png/reset_przycisk.png')
    skok_dzwiek = pygame.mixer.Sound("data/dzwieki/skok_dzwiek.wav")
    jablko_dzwiek = pygame.mixer.Sound("data/dzwieki/jablko_dzwiek.wav")
    przegrana_dzwiek = pygame.mixer.Sound("data/dzwieki/przegrana_dzwiek.wav")

    WHITE=(255,255,255) # stała
    rotacja = -5 # włączającgrę domyślna rotacja przedmiotu
    # tworzenie nowego obiektu
    gracz = Gracz()
    jablka = []
    for i in range(5): jablka.append(Jablko()) # wyświetlanie jablka - 5 na ekranie
    
    for jablko in jablka: # w randomowych miejscach pojawiają się jabłka
        jablko.pozycja.xy = random.randrange(0, DISPLAY.get_width() - jablko.obiekt.get_width()), jablka.index(jablko)*-200 - gracz.pozycja.y # do góy generowanie jabłek
    
    # tworzenie listy tła, gdzie każdy indeks jest obiektem
    motyw = [Tlo()]
    # kilka zmiennych, których potrzebujemy
    liczba_jablek = 0 # poczatkowa liczba jablka
    zdrowie = 100 # czas 
    moc_skoku = 4 # siła skoku
    przegrana = False
    czas = time.time()

    # główna pętla gry
    while True:
        gra= time.time() - czas
        gra*= 60 # szybkość gry
        czas = time.time()
        # ponownie, zdobądź pozycję
        myszX,myszY = pygame.mouse.get_pos() 

        skok = False 
        kliknieto = False
        # wydarzenia
        for event in pygame.event.get(): # zarzadza zdarzeniami i kolejką zdarzeń
            if event.type==pygame.KEYDOWN and event.key==K_SPACE: # .key - obsługa klawiatury, skok - spacja
                skok = True
            if event.type == pygame.MOUSEBUTTONDOWN: # używanie myszy w grze
                kliknieto = True
            if event.type==QUIT: # wyjdź z gry - lewy górny przycisk
                pygame.quit()
                sys.exit()
        
        wyswietlanie = -gracz.pozycja.y + DISPLAY.get_height()/2 # wysokość skrzynki na wyświetlaczu
        
        DISPLAY.fill(WHITE) # ustawiamy tło gry
        for o in motyw:
            DISPLAY.blit(o.obiekt, (0, o.pozycja))
        
        for jablko in jablka: # wyświetlanie jablka
            DISPLAY.blit(jablko.obiekt, (jablko.pozycja.x, jablko.pozycja.y + wyswietlanie)) 
        
        DISPLAY.blit(pygame.transform.rotate(gracz.aktualnyObiekt, klamra(gracz.predkosc.y, -10, 500)*rotacja), (gracz.pozycja.x,gracz.pozycja.y + wyswietlanie)) # gracz wyświeltanie
        DISPLAY.blit(interfejs_motyw, (0, 0)) # tło paska życia
        pygame.draw.rect(DISPLAY,(218,39,39),(21,437,150*(zdrowie/100),25)) # kolor paska życia oraz czas życia
        DISPLAY.blit(interfejs, (0, 0)) # wyświetlanie paska na dole ekranu
        
        liczba_jablekDisplay = czcionka.render(str(liczba_jablek).zfill(5), True, (0,0,0)) # 5 - ilość zer na wyświetlaczu
        DISPLAY.blit(liczba_jablekDisplay, (22, 394)) # wyświetlanie lokalizacji punktów
        if przegrana:
            DISPLAY.blit(reset_przycisk, (1, 1)) # szerokość, wysokość napisu powtórz
            przegrana_komunikat = czcionka.render("reset", True, (0, 0, 0))
            DISPLAY.blit(przegrana_komunikat, (1, 1)) # wyswietlanie przycisku 
 
        gracz.pozycja.x += gracz.predkosc.x*gra ## możemy poruszać się po grze
        if gracz.pozycja.x + gracz.aktualnyObiekt.get_size()[0] > 640: # prawa ściana
            gracz.predkosc.x = -abs(gracz.predkosc.x)
            gracz.aktualnyObiekt = gracz.lewoObiekt
            rotacja = 5 # rotacja skoku
        if gracz.pozycja.x < 0: # lewa ściana
            gracz.predkosc.x = abs(gracz.predkosc.x)
            gracz.aktualnyObiekt = gracz.prawoObiekt
            rotacja = -5 # rotacja skoku
        if skok and not przegrana: # skok
            gracz.predkosc.y = -moc_skoku
            pygame.mixer.Sound.play(skok_dzwiek) # dźwięk skoku
        gracz.pozycja.y += gracz.predkosc.y*gra # przemieszczanie się po grze
        gracz.predkosc.y = klamra(gracz.predkosc.y + gracz.przyspieszenie*gra, -99999999999, 50)

        zdrowie -= 0.2*gra # pasek życia | działanie to oznacza, że od aktualnej wartości zmiennej "zdrowie" odemujemy -0.2*gra
        if zdrowie <= 0 and not przegrana: # koniec gry jeżeli skończy się pasek życia
            przegrana = True
            pygame.mixer.Sound.play(przegrana_dzwiek) # dźwięk przegranej
            

        for jablko in jablka: # petla ta sprawdza czy zdobyliśmy punkt
            if (sprawdzanieKolizji(gracz.pozycja.x, gracz.pozycja.y, gracz.aktualnyObiekt.get_width(), gracz.aktualnyObiekt.get_height(), jablko.pozycja.x, jablko.pozycja.y, jablko.obiekt.get_width(), jablko.obiekt.get_height())):
                przegrana = False
                pygame.mixer.Sound.play(jablko_dzwiek)
                liczba_jablek += 1
                zdrowie = 100
                jablko.pozycja.y -= DISPLAY.get_height() - random.randrange(0, 1) # usuwa już zdobyte jabłka

        
        if przegrana and kliknieto and sprawdzanieKolizji(myszX, myszY, 3, 3, 4, 4, reset_przycisk.get_width(), reset_przycisk.get_height()): # przycisk - ponowna gra
            zdrowie = 100
            gracz.predkosc.xy = 3, 0
            gracz.pozycja.xy = 295, 0 # szerokość odrodzenia po przegranej
            liczba_jablek = 0
            moc_skoku = 4
            przegrana = False         
        
        pygame.display.update()
        pygame.time.delay(1)

if __name__ == "__main__": # name to specjalna zmienna, którą python przydziela naszym pliką które będziemy uruchamiali
    main() # zanim zacznie przetwarzać ich kod 


# Biografia:
# https://www.myinstants.com/instant/gta-v-wasted/ - 23.04.2022
# https://freesound.org/search/?q=jump&f=&w=&s=Duration+%28short+first%29&advanced=0&g=1 - 23.04.2022
# https://www.freefontspro.com/new-fonts/4/ - 22.04.2022
# https://www.pngall.com/apple-fruit-png/download/4687 - 22.04.2022
# https://rk.edu.pl/pl/podstawy-pygame/ - 22.04.2022
# https://analityk.edu.pl/pygame-wprowadzenie/ - 22.04.2022
# https://realpython.com/pygame-a-primer/ - 22.04.2022