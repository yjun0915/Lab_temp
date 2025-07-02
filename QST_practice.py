import pandas as pd
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize
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

operator = {
    'H': np.array([[1, 0], [0, -1]]),
    'V': np.array([[-1, 0], [0, 1]]),
    'D': np.array([[0, 1], [1, 0]]),
    'A': np.array([[0, -1], [-1, 0]]),
    'R': np.array([[0, 1j], [-1j, 0]]),
    'L': np.array([[0, -1j], [1j, 0]])
}
# print(tm(operator['H'], operator['D']))
states = {
    'H': np.array([[1, 0]]),
    'V': np.array([[0, 1]]),
    'D': np.array([[1/2, 1/2]]),
    'A': np.array([[1/2, -1/2]]),
    'R': np.array([[1/2, 1j/2]]),
    'L': np.array([[1/2, -1j/2]])
}
# print(tm(states['H'], states['H']).ravel())

parameters = ['H', 'V', 'D', 'A', 'R', 'L']
basis = np.array(list(product(parameters, parameters)))
# print(basis)


T = pd.read_csv(filepath_or_buffer='./QST_example_2qubit.csv', sep=',', index_col=0)
info = T.describe()
# print(S['H']['H'])


output = np.zeros(shape=[4, 4], dtype = 'complex')

for idx in range(basis.shape[0]):
    output += 0.5*T[basis[idx][0]][basis[idx][1]]*tm(operator[basis[idx][0]], operator[basis[idx][1]])


result = np.real(output).ravel()
print(result)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

_x = np.arange(4)
_y = np.arange(4)
_xx, _yy = np.meshgrid(_x, _y)
x, y = _xx.ravel(), _yy.ravel()
z = np.zeros_like(x)

dx = dy = 0.8

norm = Normalize(vmin=result.min(), vmax=result.max())
cmap = cm.bwr
colors = cmap(norm(result))

plot = ax.bar3d(x, y, z, dx, dy, result, color=colors, shade=True)
ax.set_zlim(np.min(result), np.max(result))

plt.show()
