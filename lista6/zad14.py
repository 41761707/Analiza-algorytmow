import sys
import numpy as np
import matplotlib.pyplot as plt

def stationary_distribution(transition_matrix):
    eigenvalues, eigenvectors = np.linalg.eig(transition_matrix.T)
    stationary_index = np.where(np.isclose(eigenvalues,1))[0]
    stationary_distribution = np.zeros(eigenvalues.shape)
    for index in stationary_index:
        one_vector = np.real(np.transpose(eigenvectors[:,index]))
        one_vector = np.abs(one_vector) / sum(np.abs(one_vector))
        stationary_distribution = stationary_distribution + one_vector
    stationary_distribution = stationary_distribution / sum(stationary_distribution)

    return stationary_distribution

def vector(alpha,p_g,n):
    j_n = np.ones((n, n))
    m_g = (1-alpha) * p_g + alpha * (1/n) * j_n
    return m_g
    #stationary_vector = stationary_distribution(m_g)
    #return stationary_vector
def main():
    n_g = np.array([[0,1,1,0,0],
                    [0,0,0,1,0],
                    [0,1,0,1,1],
                    [1,0,0,0,0],
                    [0,0,0,0,0]])
    
    #Wyliczone recznie p na podstawie n_g
    p = np.array([[0,1/2,1/2,0,0],
                [0,0,0,1,0],
                [0,1/3,0,1/3,1/3],
                [1,0,0,0,0],
                [1/5,1/5,1/5,1/5,1/5]])
    
    n_states = p.shape[0]
    
    initial_distribution = np.ones(n_states) / n_states
    '''e = 0.001
    t = 1
    while t<30:
        row = np.dot(initial_distribution,np.linalg.matrix_power(p,t))
        #print(row)
        #print(stationary)
        if np.max(np.abs(row-initial_distribution)) <= e:
            break
        t = t + 1
    print(f"{e} : {t} - {row}")'''
    alphas = [0,0.25,0.5,0.75,0.85,1]
    results = []
    new_vector = initial_distribution[:]
    for a in alphas:
        plt.title("Zadanie 14, zmiana z liczbą kroków, alpha: {}".format(a))
        plt.xlabel('Kroki')
        plt.ylabel('Prawd.')
        new_p = vector(a,p,n_states)
        for t in range(25):
            row = np.dot(initial_distribution,np.linalg.matrix_power(new_p,t))
            results.append(row)
        #print(results)
        plt.plot(range(25), results)
        plt.ylim(0, 0.5)
        plt.legend(['1','2','3','4','5'])
        plt.savefig('Zad14_changes{}.png'.format(a))
        plt.clf()
        plt.title("Zadanie 14, wykres kolumnowy, alpha: {}".format(a))
        plt.xlabel('Strona')
        plt.ylabel('Prawd.')
        for i,element in enumerate(results[-1]):
            plt.bar(i,element)
        plt.savefig('Zad14_hist{}.png'.format(a))
        plt.clf()
        results.clear()
        #results.append([a,new_p])
        #print(stationary_distribution(new_p))
    #print(results)
    print(stationary_distribution(p))

if __name__ == '__main__':
    main()