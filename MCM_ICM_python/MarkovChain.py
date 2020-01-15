import numpy as np
def markov():
    init_array = np.array([0.1, 0.2, 0.7])
    transfer_matrix = np.array([[0.9, 0.075, 0.025],
                               [0.15, 0.8, 0.05],
                               [0.25, 0.25, 0.5]])
    restmp = init_array
    for i in range(25):
        res = np.dot(restmp, transfer_matrix)
        print(i, "\t", res)
        restmp = res

markov()

def matrixpower():
    transfer_matrix = np.array([[0.9, 0.075, 0.025],
                               [0.15, 0.8, 0.05],
                               [0.25, 0.25, 0.5]])
    restmp = transfer_matrix
    for i in range(25):
        res = np.dot(restmp, transfer_matrix)
        print(i, "\t", res)
        restmp = res

matrixpower()

