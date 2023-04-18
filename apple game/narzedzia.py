# Kamil Balcerzak

def klamra(wartosc, min, max): # prędkości, przyśpieszenia
    if wartosc < min:
        return min
    if wartosc > max:
        return max
    return wartosc

def sprawdzanieKolizji(a_x, a_y, a_szerokosc, a_wysokosc, b_x, b_y, b_szerokosc, b_wysokosc):
    return (a_x + a_szerokosc > b_x) and (a_x < b_x + b_szerokosc) and (a_y + a_wysokosc > b_y) and (a_y < b_y + b_wysokosc)
