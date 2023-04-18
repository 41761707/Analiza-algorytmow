from struct import unpack
import hashlib


def min_count(multiset, hash_func, k):
    M = [1] * k
    for item in multiset:
        hash_item = get_hash(hash_func, item) / 2**32
        if hash_item < M[k-1] and hash_item not in M:
            M[k-1] = hash_item
            M.sort()
    if M[k-1] == 1:
        return sum(1 for i in M if i != 1)
    return (k-1)/M[k-1]

def hyperloglog(multiset, hash_func, b):
    m = 2**b
    R = [0] * m
    for item in multiset:
        hash_item = get_hash(hash_func, item)
        rest = hash_item >> b
        reg_id = hash_item ^ (rest << b)
        #print(R[reg_id], leftmost_one_index(rest, 32-b))
        R[reg_id] = max(R[reg_id], leftmost_one_index(rest, 32-b))
    mean = 0
    for i in range(m):
        mean += 2**(-R[i])
    alpha = get_alpha(m)
    result = alpha*(m**2)/mean
    return result


def leftmost_one_index(number, size):
    binary_str = bin(number)[2:].zfill(size)
    return binary_str.index('1') + 1


def get_hash(h, m):
    b = m.encode(encoding="utf-8")
    return unpack('L', h(b).digest()[:8])[0] >> 32

def get_alpha(m):
        return 0.7213 / (1 + 1.079 / m)


def main():
    multiset = [f'{i}' for i in range(5560)]
    hash_func = hashlib.sha256
    #k = 100
    b = 5
    #alpha = 0.69712263380102416804875375530
    
    #print(min_count(multiset, hash_func, k))
    print(hyperloglog(multiset, hash_func, b))
    
    
if __name__ == '__main__':
    main()