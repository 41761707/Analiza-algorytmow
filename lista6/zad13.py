import sys
import numpy as np

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


def main():
    p = np.array([[0, 0.3, 0.1, 0.6],
                   [0.1, 0.1, 0.7, 0.1],
                   [0.1, 0.7, 0.1, 0.1],
                   [0.9, 0.1, 0, 0]])
    n_states = p.shape[0]
    stationary = stationary_distribution(p)
    print("Rozkład stacjonarny:,", stationary)
    initial_distribution = np.ones(n_states) / n_states
    start = np.array([1,0,0,0])
    #print("Prawdopodobieństwo znalezienia się w stanie 3 po 32 krokach, jeśli zaczynamy w stanie 0: ",np.dot(np.linalg.matrix_power(p,32),start))
    #print("Prawdopodobieństwo znalezienia się w stanie 3 po 128 krokach, jeśli łańcuch zaczyna się w stanie wybranym losowo w sposób jednostajny ze wszystkich czterech stanów: ", np.linalg.matrix_power(p, 128) @ initial_distribution)
    print("Prawdopodobieństwo znalezienia się w stanie 3 po 32 krokach, jeśli zaczynamy w stanie 0: ",np.dot(start,np.linalg.matrix_power(p,32))[3])
    print("Prawdopodobieństwo znalezienia się w stanie 3 po 128 krokach, jeśli łańcuch zaczyna się w stanie wybranym losowo w sposób jednostajny ze wszystkich czterech stanów: ", np.dot(initial_distribution,np.linalg.matrix_power(p, 128))[3])

    eps = [0.1,0.01,0.001]
    for e in eps:
        t = 1
        while True:
            row = np.dot(start,np.linalg.matrix_power(p,t))
            #print(row)
            #print(stationary)
            if np.max(np.abs(row-stationary)) <= e:
                break
            t = t + 1
        print(f"{e} : {t}")

if __name__ == '__main__':
    main()