import numpy as np

DIMENSION = 4

def phase_encoder(phase):
    output = np.zeros(shape=[DIMENSION, DIMENSION])
    for d in range(DIMENSION):
        basis = np.zeros(shape=[1, DIMENSION])
        basis[0][d] = np.exp(1j*phase[d]/2)
        output += basis.T*basis
    return output

print(phase_encoder([0, 1, 2, 3]))
