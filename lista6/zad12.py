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

def vector(alpha,p_g,n):
    j_n = np.ones((n, n))
    m_g = (1-alpha) * p_g + alpha * (1/n) * j_n
    stationary_vector = stationary_distribution(m_g)
    return stationary_vector
def main():
    n=6
    p_g = np.array([[1,0,0,0,0,0],
                   [0,0,0.5,0,0.5,0],
                   [1,0,0,0,0,0],
                   [0,0.5,0,0,0.5,0],
                   [0,0,0,1,0,0],
                   [0,0,1,0,0,0]])
    alpha = [0,0.15,0.5,1]
    for a in alpha:
        print(f"alpha: {a} - ",vector(a,p_g,n))
    p_g_modified = np.array([[1,0,0,0,0,0],
                   [0,0,0,0,1,0],
                   [1,0,0,0,0,0],
                   [0,0.5,0,0,0.5,0],
                   [0,0,0,1,0,0],
                   [0,0,1,0,0,0]])
    print("MODIFIED")
    for a in alpha:
        print(f"alpha: {a} - ",vector(a,p_g_modified ,n))

if __name__ == '__main__':
    main()