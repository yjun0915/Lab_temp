import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.linalg import fractional_matrix_power
from scipy.optimize import minimize

from itertools import product


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

    return np.asmatrix(output)


def density_matrix(x):
    r = np.asmatrix([
        [x[0], 0, 0, 0],
        [x[4] + 1j * x[5], x[1], 0, 0],
        [x[6] + 1j * x[7], x[8] + 1j * x[9], x[2], 0],
        [x[10] + 1j * x[11], x[12] + 1j * x[13], x[14] + 1j * x[15], x[3]]
    ], dtype='complex')
    return (r * r.H) / np.trace(r * r.H)


def obj_function(x, T):
    R = density_matrix(x)
    output = 1
    for base in basis:
        output = output*fractional_matrix_power((tm(states[base[0]], states[base[1]]) * R * tm(states[base[0]], states[base[1]]).H)[0][0], T[base[0]][base[1]])
    return np.real(1/output)


T = pd.read_csv(filepath_or_buffer='./QST_example_2qubit.csv', sep=',', index_col=0)
info = T.describe()

T = T/(T['H']['H']+T['H']['V']+T['V']['H']+T['V']['V'])
# print(S['H']['H'])

MLE_Model = minimize(
    obj_function,
    x0=np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    args=T
)
print(MLE_Model)

t_mat = (density_matrix(MLE_Model.x))
print(t_mat)

output = np.zeros(shape=[4, 4], dtype = 'complex')

for idx in range(basis.shape[0]):
    output += 0.5*T[basis[idx][0]][basis[idx][1]]*t_mat*tm(operator[basis[idx][0]], operator[basis[idx][1]])


result_real = np.real(output).ravel()
result_imag = np.imag(output).ravel()
# print(result_real)


fig = plt.figure()

_x = np.arange(4)
_y = np.arange(4)
_xx, _yy = np.meshgrid(_x, _y)
x, y = _xx.ravel(), _yy.ravel()
z = np.zeros_like(x)

x = x+0.2
y = y+0.2
dx = dy = 0.6

norm = Normalize(vmin=np.min([result_real, result_imag]), vmax=np.max([result_real, result_imag]))
cmap = cm.viridis

ax = fig.add_subplot(121, projection='3d')
colors = cmap(norm(result_real))

ax.bar3d(x, y, z, dx, dy, result_real, color=colors, shade=True)
ax.set_zlim(np.min([result_real, result_imag]), np.max([result_real, result_imag]))
ax.set_xticks([0.5, 1.5, 2.5, 3.5], ['|HH>', '|HV>', '|VH>', '|VV>'])
ax.set_yticks([0.5, 1.5, 2.5, 3.5], ['|HH>', '|HV>', '|VH>', '|VV>'])

ax2 = fig.add_subplot(122, projection='3d')
colors = cmap(norm(result_imag))

ax2.bar3d(x, y, z, dx, dy, result_imag, color=colors, shade=True)
ax2.set_zlim(np.min([result_real, result_imag]), np.max([result_real, result_imag]))
ax2.set_xticks([0.5, 1.5, 2.5, 3.5], ['|HH>', '|HV>', '|VH>', '|VV>'])
ax2.set_yticks([0.5, 1.5, 2.5, 3.5], ['|HH>', '|HV>', '|VH>', '|VV>'])

plt.show()
