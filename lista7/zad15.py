import sys

def f(n):
    if n == 0:
        return 0
    
    global_s = 0
    
    for i in range(n):
        s= f(i)
    
        global_s = global_s + s + 1
        
    return global_s

def main():
    for i in range(20):
        print(f"{i}, liczba wywołań: {f(i)}")
if __name__ == '__main__':
    main()