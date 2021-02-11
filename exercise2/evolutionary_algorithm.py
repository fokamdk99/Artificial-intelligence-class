

import numpy as np
from random import seed
from random import randint
from random import sample

def f1_skladowa(x, mu, suma):
    licznik_sklad_1 = -0.5*(x-mu).T #(1,2)
    licznik_sklad_2 = np.linalg.inv(suma) #(2,2)
    licznik_sklad_3 = x-mu #(2,1)
    licznik_mnozenie_1 = licznik_sklad_1.dot(licznik_sklad_2) #(1,2)
    licznik_mnozenie_2 = licznik_mnozenie_1.dot(licznik_sklad_3)
    licznik = np.exp(licznik_mnozenie_2)
    dzielnik_sklad_1 = (2 * np.pi)**2
    dzielnik_sklad_2 = np.linalg.det(suma)
    dzielnik = np.sqrt(dzielnik_sklad_1*dzielnik_sklad_2)
    wynik = licznik / dzielnik
    
    return wynik[0][0]

def oblicz_f2(x_value):
    sklad_1 = np.sqrt(0.5*x_value.T.dot(x_value)) * (-0.2)
    sklad_2 = 20*np.exp(sklad_1)
    sklad_3 = 0.5 * (np.cos(2*np.pi*x_value[0])) + np.cos(2*np.pi*x_value[1]) 
    sklad_4 = np.exp(sklad_3)
    #minimalizacja funkcji f2 to maksymalizacja funkcji -f2
    wynik = sklad_2 + sklad_4 + np.exp(1) + 20
    
    return wynik


def reprodukcja_turniejowa(slownik):
    #ilosc osobikow uczestniczacych w turnieju
    rozmiar_turnieju = 2
    
    potomki = []
    n = len(slownik)
    
    while (len(potomki) != n ):
        losy = sample(range(0, n), rozmiar_turnieju)
        konkurenci = [slownik[los] for los in losy]
        zwyciezcy = sorted(konkurenci, key = lambda k: k['przystosowanie'], reverse = True)
        zwyciezca = zwyciezcy[0]['ranga'] - 1
        potomki.append(slownik[zwyciezca].copy())

    return potomki

def mutacja(slownik, mu1, mu2, mu3, suma1, suma2, suma3, funkcja):
    #odchylenie standardowe mutacji
    if funkcja == 1:
        sigma = 0.3
    else:
        sigma = 0.2

    for i  in range(len(slownik)):
        slownik[i]['punkt'][0][0] += (np.random.normal(0,1,1) * sigma)
        slownik[i]['punkt'][1][0] += (np.random.normal(0,1,1) * sigma)
        
        if funkcja == 1:
            slownik[i]['przystosowanie'] = f1_skladowa(slownik[i]['punkt'],mu1,suma1) + f1_skladowa(slownik[i]['punkt'],mu2,suma2) + f1_skladowa(slownik[i]['punkt'],mu3,suma3)  
        else:
            slownik[i]['przystosowanie'] = oblicz_f2(slownik[i]['punkt'])

    return slownik

def sukcesja_elitarna(wyniki, najlepsze, mu):
    for ind, value in enumerate(najlepsze):
        wyniki.append(value.copy())

    wyniki = sorted(wyniki, key = lambda k: k['przystosowanie'], reverse = True)

    #wybierz mu najlepszych osobnikow z populacji potomnej
    wyniki = wyniki[:mu].copy()
    
    for ind, x_value in enumerate(wyniki):
        x_value['ranga'] = ind+1

    return wyniki
    

def __main__():
    #numer funkcji badanej
    nr_funkcji = 1
    
    #inicjalizacja ziarna oraz stalych
    seed(2)
    
    mu1 = np.array([14, -11]).reshape(2,1)
    mu2 = np.array([10, -10]).reshape(2,1)
    mu3 = np.array([7, -13]).reshape(2,1)
    suma1 = np.array([[1.3, -0.5],[-0.5, 0.8]])
    suma2 = np.array([[1.7, 0.4],[0.4, 1.2]])
    suma3 = np.array([[1, 0],[0, 1.5]])
    wyniki = []
    srednie = []
    maksimum = 1e-50

    #utworzenie populacji poczatkowej
    #oblicz wartosc przystosowania dla kazdego punktu z populacji poczatkowej
    #wartosci sa przechowywane w tablicy slownikow. Kazdy slownik zawiera punkt, wartosc przystosowania oraz range
    if nr_funkcji == 1:
        eta = 2
        mu = 70
        nr_iteracji = 3000
        f1_population = np.random.normal(0,1,(mu,2,1))
        for ind, x_value in enumerate(f1_population):
            wynik = f1_skladowa(x_value,mu1,suma1) + f1_skladowa(x_value,mu2,suma2) + f1_skladowa(x_value,mu3,suma3)
            slownik = dict()
            slownik['punkt'] = x_value
            slownik['przystosowanie'] = wynik
            wyniki.append(slownik)
    else:
        eta = 7
        mu = 50
        nr_iteracji = 3000
        f2_population = np.random.normal(3,1,(mu,2,1))
        for ind, x_value in enumerate(f2_population):
            wynik = oblicz_f2(x_value)
            slownik = dict()
            slownik['punkt'] = x_value
            slownik['przystosowanie'] = wynik
            wyniki.append(slownik)
    
    wyniki = sorted(wyniki, key = lambda k: k['przystosowanie'], reverse = True)
    
    
    #nadaj range w juz posortowanej wg przystosowania liscie punktow
    for ind, x_value in enumerate(wyniki):
        x_value['ranga'] = ind+1
    
    #glowna petla programu. Wybiera eta najlepszych osobnik, wykonuje reprodukcje turniejowa, mutacje gaussowska oraz sukcesje elitarna
    for i in range(1,nr_iteracji):
        najlepsze = wyniki[:eta].copy()
        potomki = reprodukcja_turniejowa(wyniki)
        potomki = mutacja(potomki, mu1, mu2, mu3, suma1, suma2, suma3, nr_funkcji)
        for ind, x_value in enumerate(potomki):
            wyniki.append(x_value.copy())
            
        wyniki = sukcesja_elitarna(wyniki, najlepsze, mu)
        srednia = sum(item['przystosowanie'] for item in wyniki)/mu
        srednie.append(srednia)
        if srednia > maksimum:
            maksimum = srednia
    srednia_calosc = sum(srednie)/(nr_iteracji-1)
    print(f"srednia za calosc: {srednia_calosc}")
    print(f"maksymalna za calosc: {maksimum}")
    

__main__()