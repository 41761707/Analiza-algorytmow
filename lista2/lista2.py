import sys
import random
import time
import math
from collections import Counter
from struct import unpack
from hashlib import sha256, sha1, blake2s, md5, shake_128
import numpy as np
import matplotlib.pyplot as plt
from zlib import crc32

class mset:
    def __init__(self,s,m):
        self.s = s
        self.m = m
    def get_s(self):
        return self.s
    def get_m(self):
        return self.m

def bytes_to_float(byte,option):
    return {
        'crc32' : int(crc32(bytes(byte, encoding='utf-8'))) / 2**32,
        #'sha256' : int(sha256(bytes(byte, encoding='utf-8')).hexdigest(), 16) / 2**256,
        'sha256' : int(sha256(bytes(byte, encoding='utf-8')).hexdigest()[:8], 16) / 2**32,
        'sha1' : int(sha1(bytes(byte, encoding='utf-8')).hexdigest(), 16) / 2**160,
        'md5' : int(md5(bytes(byte, encoding='utf-8')).hexdigest(), 16) / 2**128,
        'shake128' : int(shake_128(bytes(byte, encoding='utf-8')).hexdigest(1), 16) / 2**8
    }[option]
'''
return {
        'crc32' : crc32(bytes(byte, encoding='utf-8')) / 2**32,
        'sha256' : int(sha256(bytes(byte, encoding='utf-8')).hexdigest()[:8], 16) / 2**32,
        'sha1' : int(sha1(bytes(byte, encoding='utf-8')).hexdigest()[:8], 16) / 2**20,
        'md5' : int(md5(bytes(byte, encoding='utf-8')).hexdigest()[:8], 16) / 2**16,
        'shake128' : int(shake_128(bytes(byte, encoding='utf-8')).hexdigest(1), 16) / 2**8
    }[option]
'''

def minCount(numbers,h,k):
    M = [1] * k
    for x in numbers:
        hash = bytes_to_float(str(x),h)
        if(hash < M[k-1] and hash not in M):
            M[k-1] = hash
            M.sort()
    if(M[k-1]==1):
        return len(M) - M.count(1)
    else:
        return (k-1)/M[k-1]
    
def better_plot(tab,r):
    plt.title("Zadanie 5, podpunkt b")
    plt.xlabel('n')
    plt.ylabel('n^')
    k=[2,3,5,10,100,400]
    for i in range(len(tab)):
        plt.plot(range(1,r+1), tab[i], label='k: {}'.format(k[i]))
    plt.legend(loc="upper left")
    plt.savefig("zad5_b_line")
    plt.clf()
def zad1(S,r,filename):
    plt.title("Zadanie 5, podpunkt b")
    plt.xlabel('n')
    plt.ylabel('n^/n')
    better_plot_tab = []
    for k in [2,3,10,100,400]:
        results = []
        plot_tab = []
        for element in S:
            multiset = mset(element,[])
            numbers = multiset.get_s()
            value = minCount(numbers,'crc32',k)
            plot_tab.append(value)
            results.append(value/len(element))
        plt.plot(range(1,r+1), results, label='k: {}'.format(k))
        better_plot_tab.append(plot_tab)
    print(results)
    plt.legend(loc="upper left")
    plt.savefig(filename)
    plt.clf()
    better_plot(better_plot_tab,r)

def generate_set(r):
    S = [[] for _ in range(r)]
    cnt = 1
    temp = 1
    while (cnt <= r):
        S[cnt-1] = [i for i in range(temp, temp+cnt)]
        temp = temp+cnt
        cnt += 1
    return S

def zad1c(S,filename):
    found_ks = []
    results = []
    values = []
    p = 100
    q = 400
    ccc=0
    while(ccc<9):
        counter = 0
        k = (p+q)//2
        for element in S:
            multiset = mset(element,[])
            numbers = multiset.get_s()
            if(abs((minCount(numbers,"sha256",k))/len(element)-1)<0.1):
                counter = counter + 1
        if(counter/len(S) > 0.95):
            print("FOUND")
            found_ks.append(k)
            print(k,p,q)
            q=k+1
        else:
            print("NOT FOUND")
            print(k,p,q)
            p=k-1
        results.append(k)
        values.append(counter/len(S))
        ccc=ccc+1
    print("---------------")
    print("FOUND KS:")
    print(found_ks.sort())
    plt.title("Zadanie 5_c")
    plt.xlabel('n')
    plt.ylabel('licznik/n')
    plt.plot(results,values, label='licznik/n')
    plt.legend(loc="lower right")
    plt.savefig(filename)
    plt.clf()

def zad2(S,filename,r):
    plt.title("Zadanie 6, hashe")
    plt.xlabel('n')
    plt.ylabel('n^')
    results = []
    for hash in ['md5','sha256','sha1','crc32','shake128']:
        results = []
        print("Rozpoczynam pracę dla hasha: {}".format(hash))
        for i in range(1,r+1):
            results.append(minCount([x for x in range(1,i+1)],hash,400))
        plt.plot(range(1,r+1), results, label='hash: {}'.format(hash))
    plt.legend(loc="upper left")
    plt.savefig(filename)
    plt.clf()

def zad3(S,filename,r,alpha):
    k = 400
    results=[]
    results_abs = []
    for element in S:
        multiset = mset(element,[])
        numbers = multiset.get_s()
        v = minCount(numbers,'sha256',k)
        results_abs.append(abs(1-(v/len(element))))
        results.append(v/len(element))
    results_abs.sort()
    lowest_delta = 0
    tmp = [x / 100.0 for x in range(1, 99, 1)]
    delta_id = int((1-alpha)*len(results_abs))
    lowest_delta = results_abs[delta_id]      
    chebyshev = math.sqrt((len(S) - k + 1) / (len(S) * (k - 2))) / math.sqrt(alpha)
    chernoff = math.sqrt(- (3 * math.log(alpha / 2)) / len(S))
    print(chebyshev)
    plt.title("Zadanie 7, ograniczenia, alpha={}".format(alpha))
    plt.xlabel('n')
    plt.ylabel('n^')
    plt.plot(range(1,r+1), results, 'bo',label='n^/n',markersize=2)
    plt.plot(range(1,r+1),[1-lowest_delta for _ in range(1,r+1)],color='black', label="1-delta",linestyle='dashed')
    plt.plot(range(1,r+1),[1+lowest_delta for _ in range(1,r+1)],color='black', label="1+delta",linestyle='dashed')
    plt.plot(range(1,r+1),[1-chernoff for _ in range(1,r+1)],color='green', label="1-chernoff",linestyle='dashed')
    plt.plot(range(1,r+1),[1+chernoff for _ in range(1,r+1)],color='green', label="1+chernoff",linestyle='dashed')
    plt.plot(range(1,r+1),[1-chebyshev for _ in range(1,r+1)],color='red', label="1+chebyshev",linestyle='dotted')
    plt.plot(range(1,r+1),[1+chebyshev for _ in range(1,r+1)],color='red', label="1+chebyshev",linestyle='dotted')
    plt.legend(loc="upper left")
    plt.savefig(filename)
    plt.clf()
    print("KONIEC_FUNKCJI")



    

        


def main():
    #zad1(generate_set(10000),10000,"zad5_b.png")
    #zad1c(generate_set(10000),"zad5_c.png")
    #zad2(generate_set(10000),"zad6.png",10000)
    for alpha in [0.05,0.01,0.005]:
        zad3(generate_set(10000),"zad7_"+str(alpha)+".png",10000,alpha)

if __name__ == '__main__':
    main()