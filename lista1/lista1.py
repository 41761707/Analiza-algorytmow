import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import statistics

def known_n(n):
    if(n<2):
        print("Nieprawidłowa wartość parametru n. Parametr n powinien być większy niż 1")
    p = 1/n
    counter=0 #ile nadalo
    slot=0 #Ktory slot
    lider=0 #Kto liderem, wartosc z zakresu [1..n]
    while(counter != 1):
        counter = 0
        for i in range(1,n):
            rand = random.uniform(0,1)
            #print("Rand: {}, p: {}".format(rand,p))
            if(rand <= p):
                #print("Slot: {}, urzadzenie: {} NADAJE".format(slot,i))
                counter = counter + 1
                lider = i
            else:
                pass
                #print("Slot: {}, urzadzenie: {} CISZA".format(slot,i))
        slot = slot + 1
    #print("Znaleziono lidera {} w rundzie {}".format(lider,slot))
    return slot



def unknown_n(n,u):
    counter= 0 #ile nadało
    slot = 0 #który slot w rundzie
    lider = 0 #kto liderem [1..u]
    slots_per_round = math.ceil(math.log2(u))
    while(counter != 1):
        counter = 0
        for i in range(1,n):
            p = pow((1/2),slot % slots_per_round + 1)
            rand = random.uniform(0,1)
            #print("Rand: {}, p: {}".format(rand,p))
            if(rand <= p):
                #print("Slot: {}, urzadzenie: {} NADAJE".format(slot,i))
                counter = counter + 1
                lider = i
            else:
                pass
                #print("Slot: {}, urzadzenie: {} CISZA".format(slot,i))
        slot = slot + 1
    #print("Znaleziono lidera {} w rundzie {}".format(lider,slot))
    return slot
                
def zad2_known(tests,n,u):
    results = {}
    values = []
    for _ in range(tests):
        a = known_n(n)
        values.append(a)
        if a in results:
            results[a] = results[a] + 1
        else:
            results[a] = 1
    sorted_results = dict(sorted(results.items()))
    print(sorted_results)
    plt.title("Zadanie 2, znane n={}".format(n))
    plt.xlabel('Sloty')
    plt.ylabel('Liczba wystąpień')
    plt.hist(x=values, bins=range(1, max(values)), alpha=0.7, ec='black')
    plt.savefig("Zad2_known.png")
    plt.clf()

def zad2_unknown(tests,n,u,filename):
    results = {}
    values = []
    for _ in range(tests):
        a = unknown_n(n,u)
        values.append(a)
        if a in results:
            results[a] = results[a] + 1
        else:
            results[a] = 1
    sorted_results = dict(sorted(results.items()))
    print(sorted_results)
    plt.title("Zadanie 2, n={}, u={}".format(n,u))
    plt.xlabel('Sloty')
    plt.ylabel('Liczba wystąpień')
    plt.hist(x=values, bins=range(1, max(values)), alpha=0.7, ec='black')
    plt.savefig(filename)
    plt.clf()

def zad2(tests,n,u):
    zad2_known(tests,n,u)
    zad2_unknown(tests,2,u,"Zad2_unknown_1")
    zad2_unknown(tests,int(u/2),u,"Zad2_unknown_2")
    zad2_unknown(tests,u,u,"Zad2_unknown_3")

def zad3(max_n):
    values = []
    graph_expected = []
    graph_variance = []
    for n in range(100,max_n,10):
        for i in range(10):
            values.append(known_n(n))
        expected_value = statistics.mean(values)
        variance_value = statistics.variance(values)
        graph_expected.append(expected_value)
        graph_variance.append(variance_value)
    plt.title("Zadanie 3, Wartość oczekiwana, n={}".format(max_n))
    plt.xlabel('n')
    plt.ylabel('Wartość oczekiwana')
    plt.plot(range(100,max_n,10), graph_expected)
    plt.savefig("Zad3_expected.png")
    plt.clf()

    print("Srednia wartosc zmiennej losowej: {}".format(statistics.mean(graph_expected)))

    plt.title("Zadanie 3, Wariancja, n={}".format(max_n))
    plt.xlabel('n')
    plt.ylabel('Wartość Wariancja')
    plt.plot(range(100,max_n,10), graph_variance)
    plt.savefig("Zad3_variance.png")
    plt.clf()

    print("Srednia wartosc zmiennej losowej: {}".format(statistics.mean(graph_variance)))

def zad4(max_u):
    counter = 0
    rounds = 1000
    probability_2 = []
    probability_half = []
    probability_full = []
    for u in range(100,max_u,50):
        print(u) 
        probability_2.append(probability(rounds,2,u))
        probability_half.append(probability(rounds,int(u/2),u))
        probability_full.append(probability(rounds,u,u))
    print(probability_2)

    plt.title("Zadanie 4, Prawdopodobieństwa dla n=2")
    plt.xlabel('u')
    plt.ylabel('Prawdopodobieństwo')
    plt.plot(range(100,max_u,50), probability_2)
    plt.savefig("Zad4_probability_2.png")
    plt.clf()
    print(probability_half)
    plt.title("Zadanie 4, Prawdopodobieństwa dla n=u/2")
    plt.xlabel('u')
    plt.ylabel('Prawdopodobieństwo')
    plt.plot(range(100,max_u,50), probability_half)
    plt.savefig("Zad4_probability_half.png")
    plt.clf()
    print(probability_full)
    plt.title("Zadanie 4, Prawdopodobieństwa dla n=u")
    plt.xlabel('n')
    plt.ylabel('Prawdopodobieństwo')
    plt.plot(range(100,max_u,50), probability_full)
    plt.savefig("Zad4_probability_full.png")
    plt.clf()

def probability(rounds,n,u):
    counter = 0
    for i in range(rounds):
        slot=unknown_n(n,u)
        if(slot <= math.ceil(math.log2(u))):
            counter = counter+1
    return counter/rounds
    







def main():
    n = int(sys.argv[1])
    u = int(sys.argv[2])
    mode = sys.argv[3]
    if(mode == 'KNOWN'):
        print("Slot: {}".format(known_n(n)))
    if(mode == 'UNKNOWN'):
        unknown_n(n,u)
    if(mode == 'ZAD2'):
        zad2(1000,n,u)
    if(mode == 'ZAD3'):
        zad3(n)
    if(mode == 'ZAD4'):
        zad4(u)

if __name__ == '__main__':
    main()