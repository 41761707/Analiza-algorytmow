import math
import mmh3
import random
from collections import Counter
from hashlib import sha256, sha1, blake2s, md5, shake_128
from zlib import crc32
import matplotlib.pyplot as plt
from struct import unpack

def bytes_to_float(byte,option):
    return {
        'crc32' : crc32(bytes(byte, encoding='utf-8')) / 2**32,
        'sha256' : int(sha256(bytes(byte, encoding='utf-8')).hexdigest(), 16) / 2**256,
        #'sha256' : int(sha256(bytes(byte, encoding='utf-8')).hexdigest()[:8], 16) / 2**32,
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


class HyperLogLogPlusPlus:
    def __init__(self,b):
        self.b = b #b in 4,..,16
        self.m = 2 ** b
        self.M = [0] * self.m
    def add(self,array,func):
        for v in array:
            x = bin(int.from_bytes(func(bytes(v, encoding='utf-8')).digest(), 'little'))[-32:]
            j = int(x[:self.b],2)
            w = x[self.b:]
            self.M[j] = max(self.M[j], self.rho(w))

    def get_alpha(self):
        if(self.m==16):
            return 0.673
        elif(self.m==32):
            return 0.697
        elif(self.m==64):
            return 0.709
        return 0.7213 / (1 + 1.079 / self.m)

    def get_E(self):
        #print(self.M)
        sum_M = 0
        for j in range(len(self.M)):
            sum_M = sum_M + 2**-self.M[j]
        E = self.get_alpha()*self.m*self.m*(sum_M**-1)
        return E
    
    def count(self):
        E_star = 0
        E = self.get_E()
        if E <= 2.5 * self.m:
            zeros = self.M.count(0)
            if(zeros != 0):
                E_star = self.m * math.log(float(self.m) / zeros)
            else:
                E_star = E
        elif E <= (1/30) * 2**32:
            E_star = E
        else:
            E_star = -2**32 * math.log(1-(float(E)/(2**32)))
        return E_star
    
    def rho(self,w):
        for i in range(len(w)):
            if(w[i] == '1'):
                return i+1
        return len(w)+1
    
def main():
    '''
    for b in range(4,17): #4,17
        results = []
        hll = HyperLogLogPlusPlus(b)
        for n in range(1,10001):
            array = [str(x) for x in range(n)]
            hll.add(array)
            results.append(hll.count()/n)
        plt.title("Zadanie 8, b:{}".format(b))
        plt.xlabel('n')
        plt.ylabel('licznik/n')
        plt.plot([n for n in range(1,10001)],results)
        plt.savefig("{}_wynik.png".format(b))
        plt.clf()
    '''
    '''
    plt.title("Zadanie 8, b:{}".format(11))
    plt.xlabel('n')
    plt.ylabel('licznik/n')
    funcs = [sha256, sha1, blake2s, md5]
    for func in funcs:
        results = []
        hll = HyperLogLogPlusPlus(11)
        for n in range(1,10001):
            array = [str(x) for x in range(n)]
            hll.add(array,func)
            results.append(hll.count()/n)
        plt.plot([n for n in range(1,10001)], results, label='hash: {}'.format(func))
    plt.legend(loc="lower right")
    plt.savefig("{}_porownanie.png".format(11))
    plt.clf()
    '''
    plt.title("Zadanie 8, porównanie".format(11))
    plt.xlabel('n')
    plt.ylabel('licznik/n')
    funcs = [sha256]
    for func in funcs:
        for b in [5,6,7,8]:
            results_hyper = []
            results_mincount = []
            hll = HyperLogLogPlusPlus(5)
            for n in range(1,10001):
                array = [str(x) for x in range(n)]
                hll.add(array,func)
                results_hyper.append(hll.count()/n)
                value = minCount(array,'sha256',int((2**5 * b)/32))
                results_mincount.append(value/n)
            plt.plot([n for n in range(1,10001)], results_hyper, label='algorytm: {}'.format("HyperLogLog"))
            plt.plot([n for n in range(1,10001)], results_mincount, label='hash: {}'.format("MinCount"))
        plt.legend(loc="lower right")
        plt.savefig("{}_algorytmy_{}.png".format(11,b))
        plt.clf()
if __name__ =='__main__':
    main()
