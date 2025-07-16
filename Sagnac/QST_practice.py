import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.linalg import sqrtm
from scipy.optimize import minimize

from itertools import product


__DIMENSION__ = 2

operator = {
    'H': np.array([[1, 0], [0, 0]]),
    'V': np.array([[0, 0], [0, 1]]),
    'D': np.array([[1/2, 1/2], [1/2, 1/2]]),
    'A': np.array([[1/2, -1/2], [-1/2, 1/2]]),
    'R': np.array([[1/2, -1j/2], [1j/2, 1/2]]),
    'L': np.array([[1/2, 1j/2], [-1j/2, 1/2]])
}

states = {
    'H': np.array([[1, 0]]),
    'V': np.array([[0, 1]]),
    'D': np.array([[1/2, 1/2]]),
    'A': np.array([[1/2, -1/2]]),
    'R': np.array([[1/2, 1j/2]]),
    'L': np.array([[1/2, -1j/2]])
}

target = {
    'psi+': np.array([
        [0, 0, 0, 0],
        [0, 0.5, 0.5 ,0],
        [0, 0.5, 0.5, 0],
        [0, 0, 0, 0]
    ]),
    'psi-': np.array([
        [0, 0, 0, 0],
        [0, 0.5, -0.5 ,0],
        [0, -0.5, 0.5, 0],
        [0, 0, 0, 0]
    ]),
    'phi+': np.array([
        [0.5, 0, 0, 0.5],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0.5, 0, 0, 0.5],
    ]),
    'phi-': np.array([
        [0.5, 0, 0, -0.5],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [-0.5, 0, 0, 0.5],
    ])
}

parameters = ['H', 'V', 'D', 'A', 'R', 'L']
basis = np.array(list(product(parameters, repeat=__DIMENSION__)))


def tensor_multiplication(tensor1, tensor2):
    tensor1 = np.array(tensor1)
    tensor2 = np.array(tensor2)
    d1, d2 = tensor1.shape, tensor2.shape
    tm_output = np.zeros(shape=[d1[0]*d2[0], d1[1]*d2[1]], dtype = 'complex')

    for tm_i in range(d1[0]):
        for tm_j in range(d1[1]):
            for tm_m in range(d2[0]):
                for tm_n in range(d2[1]):
                    tm_output[d1[0]*tm_i + tm_m][d1[1]*tm_j + tm_n] = tensor1[tm_i][tm_j]*tensor2[tm_m][tm_n]

    return np.asmatrix(tm_output)


def density_matrix(dm_x):
    dm_r = np.asmatrix([
        [dm_x[0], 0, 0, 0],
        [dm_x[4] + 1j * dm_x[5], dm_x[1], 0, 0],
        [dm_x[6] + 1j * dm_x[7], dm_x[8] + 1j * dm_x[9], dm_x[2], 0],
        [dm_x[10] + 1j * dm_x[11], dm_x[12] + 1j * dm_x[13], dm_x[14] + 1j * dm_x[15], dm_x[3]]
    ], dtype='complex')
    return (dm_r * dm_r.H) / np.trace(dm_r * dm_r.H) # eq. 68


def obj_function(obj_x, obj_p):
    obj_r = density_matrix(obj_x)
    obj_output = 1
    for base in basis:
        _n = tensor_multiplication(states[base[0]], states[base[1]]).dot(obj_r.dot(tensor_multiplication(states[base[0]], states[base[1]]).H))
        obj_output += ((_n - obj_p[base[0]][base[1]])**2)/(2*_n)
    return np.real(obj_output)


P = pd.read_csv(filepath_or_buffer='./QST_data.csv', sep=',', index_col=0)
info = P.describe()

if P['H']['H']+P['H']['V']+P['V']['H']+P['V']['V'] != 0:
    P = P/(P['H']['H']+P['H']['V']+P['V']['H']+P['V']['V'])

output_stocks = np.zeros(shape=[4, 4], dtype = 'complex')
T = np.zeros(shape=(4, 4))
stocks_index = [['H', 'V', 1, 1], ['D', 'A', 1, -1], ['R', 'L', 1, -1], ['H', 'V', 1, -1]]

for i in range(4):
    for j in range(4):
        for m in range(2):
            for n in range(2):
                parity = stocks_index[i][m+2] * stocks_index[j][n+2]
                T[i][j] += parity * P[stocks_index[i][m]][stocks_index[j][n]]   # eq. 39

for i in range(4):
    for j in range(4):
        output_stocks += 0.25 * T[i][j] * tensor_multiplication(operator[stocks_index[i][0]] + (stocks_index[i][3] * operator[stocks_index[i][1]]),
                                                         operator[stocks_index[j][0]] + (stocks_index[j][3]*operator[stocks_index[j][1]]))


output_MLE = np.zeros(shape=[4, 4], dtype = 'complex')
MLE_Model = minimize(
    obj_function,
    x0=np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])*0.25,
    args=P,
    method='COBYLA'
)
print(MLE_Model)

output_MLE = density_matrix(MLE_Model.x)


fig = plt.figure(figsize=(16, 10), dpi=100)
for idx in range(2):
    output = output_MLE
    if idx == 1:
        output = output_stocks
    fidelity = np.trace(sqrtm(sqrtm(output).dot(target['psi+'].dot(sqrtm(output)))))**2
    purity = np.trace(output.dot(output))
    r, v = np.linalg.eig(output)
    r = sorted(r, reverse=True)
    concurrence = max(0, r[0] - r[1] - r[2] - r[3])

    result_real = np.squeeze(np.asarray(np.real(output).ravel()))
    result_imag = np.squeeze(np.asarray(np.imag(output).ravel()))


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

    row = idx*5
    ax = fig.add_subplot(2, 5, (1+row, 2+row), projection='3d')
    colors = cmap(norm(result_real))

    ax.bar3d(x, y, z, dx, dy, result_real.ravel(), color=colors, shade=True)
    ax.set_zlim(np.min([result_real, result_imag]), np.max([result_real, result_imag]))
    ax.set_xticks([0.5, 1.5, 2.5, 3.5], ['|HH>', '|HV>', '|VH>', '|VV>'])
    ax.set_yticks([0.5, 1.5, 2.5, 3.5], ['|HH>', '|HV>', '|VH>', '|VV>'])

    ax2 = fig.add_subplot(2, 5, (3+row, 4+row), projection='3d')
    colors = cmap(norm(result_imag))

    ax2.bar3d(x, y, z, dx, dy, result_imag, color=colors, shade=True)
    ax2.set_zlim(np.min([result_real, result_imag]), np.max([result_real, result_imag]))
    ax2.set_xticks([0.5, 1.5, 2.5, 3.5], ['|HH>', '|HV>', '|VH>', '|VV>'])
    ax2.set_yticks([0.5, 1.5, 2.5, 3.5], ['|HH>', '|HV>', '|VH>', '|VV>'])

    info = fig.add_subplot(2, 5, 5+row)
    info.text(y=1, x=0.2, s="Fidelity is %.4f"%fidelity)
    info.text(y=0.9, x=0.2, s="Concurrence is %.4f"%concurrence)
    info.text(y=0.8, x=0.2, s="Purity is %.4f"%purity)
    info.set_ylim([-0.5, 1.5])
    plt.axis('off')

plt.show()
