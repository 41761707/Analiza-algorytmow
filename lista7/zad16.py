import sys

import random

calls = 0

def recursive_algorithm(arr):
    n = len(arr)
    global calls
    calls = calls + 1
    if n < 2:
        return

    for k in range(1, n+1):
        if random.random() < 0.5:
            index = random.randint(0,n-k)
            subarray = arr[index:index+k]
            recursive_algorithm(subarray)

n = int(sys.argv[1])
attempts = int(sys.argv[2])
array = [x for x in range(n)]
for _ in range(attempts):
    recursive_algorithm(array)

print(f"{n} : {calls/attempts}")