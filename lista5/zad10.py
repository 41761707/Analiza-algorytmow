import sys
from datetime import datetime

def generate_permutations(n):
    A = [0] * n 
    permutations = []

    def generate(index):
        if index == len(A):
            permutations.append(A.copy())
        else:
            for i in range(n+1):
                A[index] = i
                generate(index + 1)

    generate(0)
    return permutations

def privileges(c,n):
    true_counter = 0
    if c[0] == c[n-1]:
        true_counter = true_counter + 1
    for i in range(1,n):
        if c[i] != c[i-1]:
            true_counter = true_counter + 1
    if true_counter == 1:
        return True
    return False


def generate_new_states(c,indices,n):
    c_depth= 0
    def generate_depth(c,depth=0):
        nonlocal c_depth
        if privileges(c,n):
            if depth > c_depth:
                c_depth = depth
            return 0
        max_depth = 0
        if tuple(c) in indices:
            max_depth = depth + indices[tuple(c)]
            if max_depth > c_depth:
                c_depth = max_depth
            return indices[tuple(c)]
        if c[0] == c[n-1]:
            new_c = c[:]
            new_c[0] = (new_c[0]+1) % (n+1)
            max_depth = max(max_depth, generate_depth(new_c, depth+1) + 1)
        for i in range(1,n):
            if c[i] != c[i-1]:
                new_c = c[:]
                new_c[i] = new_c[i-1]
                max_depth = max(max_depth, generate_depth(new_c, depth+1) + 1)
        indices[tuple(c)] = max_depth
        return max_depth
    generate_depth(c)
    return c_depth

'''OTRZYMANE WYNIKI:'''
# n=3: Najwieksza liczba krokow dla zadanego przypadku: 2, czas:0:00:00.000228
# n=4: Najwieksza liczba krokow dla zadanego przypadku: 13, czas:0:00:00.002815 
# n=5: Najwieksza liczba krokow dla zadanego przypadku: 24, czas:0:00:00.052937
# n=6: Najwieksza liczba krokow dla zadanego przypadku: 38, czas:0:00:01.061237
# n=7: Najwieksza liczba krokow dla zadanego przypadku: 55, czas:0:00:28.283628
# n=8: 
# n=9:
# n=10:
def main():
    start_time = datetime.now()
    n = int(sys.argv[1]) #liczba procesów w pierścieniu
    cs = generate_permutations(n)
    indices = {}
    max_depth = 0
    nr_of_exec = 0
    for c in cs:
        depth = generate_new_states(c,indices,n)
        if depth > max_depth:
            max_depth = depth
    end_time = datetime.now()
    print("Najwieksza liczba krokow dla zadanego przypadku: {}, czas:{}".format(max_depth,end_time - start_time))



if __name__ == '__main__':
    main()