import itertools
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.special as scp #dwumian Newtona

#Wszystkie odniesienia odnośnie sekcji,
#dowodów bądź lematów znajdują
#swoje odzwierciedlenie w wykładzie
#"Procesy stochastyczne, analiza blokchain"
#Autorstwa dr inż. Jakuba Lemiesza

#na mocy lematu 3
def equality_of_longest_branch(n,q):
    p = 1 - q
    return (q/p)**n

#Sekcja 8 - Analiza Nakamoto
def nakamoto(n,q):
    p = 1 - q
    lam = n * (q / p)
    p_n = 0
    for k in range(0,n):
        p_n = p_n + math.exp(-lam) * ( pow(lam,k) / math.factorial(k) ) * ( 1 - equality_of_longest_branch(n-k,q) )
    p_n = 1 - p_n
    return p_n

#Najmniejsze n, dla którego mamy dopuszczalne
#prawdopodobieństwo sukcesu
def best_n(q,func,limit):
    n = 1
    while func(n,q) >= limit:
        n = n + 1
    return n

#Sekcja 9 - Analiza Grunspan'a
def grunspan(n,q):
    p = 1 - q
    p_n = 0
    for k in range(0,n):
        p_n = p_n + (p**n * q**k - q**n * p**k ) * scp.comb(k + n - 1, k)
    p_n = 1 - p_n
    return p_n

#Sekcje 5,6,7 - Atak podwójnego wydatkowania
#W pierwotnym ataku nalezy wylosować liczbę nounce z zadanego zakresu
#Dokonać hashowania H(nounce||h_prev||[lista transakcji])
#I sprawdzić, czy otrzymany wynik jest mniejszy niż wskazana liczba delta

#Załóżmy, że posiadamy dobrą funkcję hashującą, tzn. zmiana jednego bitu wejścia 
#zmienia ~len(hash)/2 bitów hasha oraz prawdopodobieństwa otrzymania wskazanego outputu przez funkcję hashującą
#jest identyczne dla każdego outputu z zakresu funkcji hashującej

#Wtedy cały proces hashowania możemy sprowadzić do prostego wylosowania liczby z przedziału (0,...,1)
#Oczywiście losowanie musi być dobre, skorzystamy z wbudowanego modułu random.uniform, który bazuje 
#na algorytmie Mersenne Twister

#Dodatkowo atrybut delta decyduje o trudności problemu i czasie potrzebnym do jego rozwiązania
#Więc musi być skorelowany z mocą obliczeniową jaką dysponują odpowiednio adwesarz jak i 
#uczciwi użytkownicy (bo decyduje jak długo generuje się blok, a generowanie bloku zależne jest od mocy obliczeniowej)

#Na podstawie powyższego ustanawia się następujący model ataku:
# 1. Wylosuj liczbę z przedziału 0,...,1
# 2. Jesli wylosowana liczba mniejsza niż q to adwesarz dodaje blok do swojej gałęzi
# 3. Jeśli nie, to uczciwi użytkownicy dodają blok do swojej 
# 4. Jeśli uczciwi użytkownicy osiągną wskazaną długość (limit+n) to wygrywają
# Jeśli przed osiągnięciem wskazanego pułapku adwesarz przegoni uczciwych to on wygrywa

#double_spending_attack - funkcja implementująca powyżej opisany atak podwójnego wydatkowania 
# @param n - liczba bloków, którymi należy nadbudować gałąź
# @param q - moc obliczeniowa adwesarza
def double_spending_attack(n,q):
    #Jakaś stała określająca ile transakcji jest potrzebnych do uformowania bloku
    limit = 0
    # Aktualny stan długości gałęzi adwesarza
    honest_users_branch = 0
    # Aktualny stan długości gałęzi uczciwych użytkowników
    adversary_branch = 0
    #Wyścig
    counter = 0
    while counter<=1000:
        if random.uniform(0,1) < q:
            adversary_branch = adversary_branch + 1
        if random.uniform(0,1) >= q:
            honest_users_branch = honest_users_branch + 1

        if honest_users_branch < n:
            continue

        if adversary_branch >= honest_users_branch:
            return True
        counter = counter + 1
    return False
        
def monte_carlo(attempts,n,q):
    suc = 0
    for _ in range(attempts):
        if(double_spending_attack(n,q)):
            suc = suc + 1
    return suc/attempts


def main():
    n_arr = [1,3,6,12,24,48]
    #q_arr = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45]
    q_arr = [0.01 * i for i in range(1,49)]

    nakamoto_data = []
    grunspan_data = []
    simulator_data = []
    for n in n_arr:
        for q in q_arr:
            nakamoto_data.append((n,q,nakamoto(n,q)))
            grunspan_data.append((n,q,grunspan(n,q)))
            simulator_data.append((n,q,monte_carlo(100,n,q)))


    #for element in nakamoto_data:
    #    print(element)
    #for element in grunspan_data:
    #    print(element)
    #for element in simulator_data:
    #    print(element)

    #plot_1
    '''for n in n_arr:
        plt.title("Zadanie 9, n:{}".format(n))
        plt.xlabel('q')
        plt.ylabel('P(n,q)')
        nakamoto_n = []
        grunspan_n = []
        for element in nakamoto_data:
            if element[0] == n:
                nakamoto_n.append(element[2])
        for element in grunspan_data:
            if element[0] == n:
                grunspan_n.append(element[2])
        print(nakamoto_n)
        print(grunspan_n)
        plt.plot(q_arr, nakamoto_n, label='Nakamoto',marker="o",linestyle="")
        plt.plot(q_arr, grunspan_n, label='Grunspan',marker="o",linestyle="")
        plt.legend(loc="lower right")
        plt.savefig("{}_nakamoto_grunspan.png".format(n))
        plt.clf()
    '''

    acceptable_pr_succ = [0.001,0.01,0.1]
    new_q_arr = [0.01 * i for i in range(1,40)]

    for limit in acceptable_pr_succ:
        best_n_data_nakamoto = []
        best_n_data_grunspan = []
        for q in new_q_arr:
            best_n_data_nakamoto.append(best_n(q,nakamoto,limit))
            best_n_data_grunspan.append(best_n(q,grunspan,limit))
        #plot 2
        plt.title("Zadanie 9, prawdopodobieństwo:{}%".format(limit))
        plt.xlabel('q')
        plt.ylabel('n')
        plt.plot(new_q_arr, best_n_data_nakamoto, label='Nakamoto',marker="o",linestyle="")
        plt.plot(new_q_arr, best_n_data_grunspan, label='Grunspan',marker="o",linestyle="")
        plt.legend(loc="lower right")
        plt.savefig("{}_nakamoto_grunspan_best_n.png".format(limit))
        plt.clf()

    #plot_3
    for n in n_arr:
        plt.title("Zadanie 9, n:{}".format(n))
        plt.xlabel('q')
        plt.ylabel('P(n,q)')
        nakamoto_n = []
        grunspan_n = []
        simulator_n = []
        for element in nakamoto_data:
            if element[0] == n:
                nakamoto_n.append(element[2])
        for element in grunspan_data:
            if element[0] == n:
                grunspan_n.append(element[2])
        for element in simulator_data:
            if element[0] == n:
                print(element)
                simulator_n.append(element[2])
        
        #print(nakamoto_n)
        #print(grunspan_n)
        print(simulator_n)
        plt.plot(q_arr, nakamoto_n, label='Nakamoto',marker="o",linestyle="",markersize=3)
        plt.plot(q_arr, grunspan_n, label='Grunspan',marker="o",linestyle="",markersize=3)
        plt.plot(q_arr, simulator_n, label='Simulator',marker="o",linestyle="",markersize=3)
        plt.legend(loc="upper left")
        plt.savefig("{}_nakamoto_grunspan_simulator.png".format(n))
        plt.clf()
    print(monte_carlo(1000,1,0.1))


    

if __name__ == '__main__':
    main()
