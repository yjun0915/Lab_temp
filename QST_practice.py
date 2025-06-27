import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from itertools import product

def tm(tensor1, tensor2):
    tensor1 = np.array(tensor1)
    tensor2 = np.array(tensor2)
    d1, d2 = tensor1.shape, tensor2.shape
    output = np.zeros(shape=[d1[0]*d2[0], d1[1]*d2[1]], dtype = 'complex')

    for i in range(d1[0]):
        for j in range(d1[1]):
            for m in range(d2[0]):
                for n in range(d2[1]):
                    output[d1[0]*i + m][d1[1]*j + n] = tensor1[i][j]*tensor2[m][n]

    return output

S = pd.read_csv(filepath_or_buffer='./QST_example_2qubit.csv', sep=',', index_col=0)
info = S.describe()

normalizer = 1/(info.loc['mean']*6).sum()

S = normalizer*S
info = S.describe()
# print(S['H']['H'])

operator = {
    'H': [[1, 0], [0, -1]],
    'V': [[-1, 0], [0, 1]],
    'D': [[0, 1], [1, 0]],
    'A': [[0, -1], [-1, 0]],
    'R': [[0, 1j], [-1j, 0]],
    'L': [[0, -1j], [1j, 0]]
}
# print(tm(operator['H'], operator['D']))

parameters = ['H', 'V', 'D', 'A', 'R', 'L']
basis = np.array(list(product(parameters, parameters)))
# print(basis)

output = np.zeros(shape=[4, 4], dtype = 'complex')

for idx in range(basis.shape[0]):
    output += 0.5*S[basis[idx][0]][basis[idx][1]]*tm(operator[basis[idx][0]], operator[basis[idx][1]])

print(np.real(output))

plt.imshow(np.real(output))
plt.colorbar()

plt.show()
