import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.colors import LightSource
from scipy.linalg import sqrtm
from scipy.special import erf
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
    ]),
    'other': np.array([
        [1/6, 0, 0, -1j/6],
        [0, 1/3, 1/3, 0],
        [0, 1/3, 1/3, 0],
        [1j/6, 0, 0, 1/6]
    ])
}

parameters = ['H', 'V', 'D', 'A', 'R', 'L']
basis = [''.join(p) for p in product(parameters, repeat=__DIMENSION__)]


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
    print(obj_x)
    for base in basis:
        _n = tensor_multiplication(states[base[0]], states[base[1]]).dot(obj_r.dot(tensor_multiplication(states[base[0]], states[base[1]]).H))
        obj_output += ((_n - obj_p["Coincidence counts"][base])**2)/(2*_n)
    time.sleep(0.01)
    print(np.real(obj_output))
    time.sleep(0.0036)
    return np.real(obj_output)


def ax_format(_ax):
    _ax.set_xticks([0.5, 1.5, 2.5, 3.5], ['|HH>', '|HV>', '|VH>', '|VV>'])
    _ax.set_yticks([0.5, 1.5, 2.5, 3.5], ['|HH>', '|HV>', '|VH>', '|VV>'])
    # _ax.set_zticks([])
    _ax.view_init(34, 20)
    _ax.set_proj_type('persp', focal_length=0.2)
    _ax.grid(False)


def rounded_box(_ax, _x, _y, _z, r, p, c):
    k = p
    theta = np.linspace(start=0, stop=2 * np.pi, num=50)
    x1 = (((erf(theta - np.pi) ** k - 0.5) * 2) * r) + _x
    y1 = (-np.sin(theta) * r) + _y
    z1 = 0

    x2 = x1
    y2 = y1
    z2 = _z

    _ax.fill_between(x1, y1, z1, x2, y2, z2, color=c, edgecolor=c, shade=True)
    _ax.fill_between(x1, y1, z1, x2, y2, z1, color=c, edgecolor=c, shade=True)


P = pd.read_csv(filepath_or_buffer='./QST_data_97.csv', sep=',', index_col=0)

# <editor-fold desc="auto normalization">
indices = [1 for _ in range(len(basis))]
for idx, item in enumerate(basis):
    for base in item:
        if base != "H" and base != "V":
            indices[idx] = 0
norm_basis_group = []
for idx, var in enumerate(indices):
    if var:
        norm_basis_group.append(basis[idx])
norm = 0
for base in norm_basis_group:
    norm += P["Coincidence counts"][base]
P = P/norm
# </editor-fold>

# <editor-fold desc="Stocks method">
output_stocks = np.zeros(shape=[4, 4], dtype = 'complex')
T = np.zeros(shape=(4, 4))
stocks_index = [['H', 'V', 1, 1], ['D', 'A', 1, -1], ['R', 'L', 1, -1], ['H', 'V', 1, -1]]

for i in range(4):
    for j in range(4):
        for m in range(2):
            for n in range(2):
                parity = stocks_index[i][m+2] * stocks_index[j][n+2]
                T[i][j] += parity * P["Coincidence counts"][''.join([stocks_index[i][m], stocks_index[j][n]])]   # eq. 39

for i in range(4):
    for j in range(4):
        output_stocks += 0.25 * T[i][j] * tensor_multiplication(operator[stocks_index[i][0]] + (stocks_index[i][3] * operator[stocks_index[i][1]]),
                                                         operator[stocks_index[j][0]] + (stocks_index[j][3]*operator[stocks_index[j][1]]))
#</editor-fold>

# <editor-fold desc="MLE method">
output_MLE = np.zeros(shape=[4, 4], dtype = 'complex')
MLE_Model = minimize(
    obj_function,
    x0=np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])*0.25,
    args=P,
    method="COBYLA"
)
print(MLE_Model)

output_MLE = density_matrix(MLE_Model.x)
# </editor-fold>

fig = plt.figure(figsize=(14, 10), dpi=80)
for idx in range(2):
    output = output_MLE
    if idx == 1:
        output = output_stocks
    fidelity = np.real(np.trace(sqrtm(sqrtm(output).dot(target['psi+'].dot(sqrtm(output)))))**2)
    purity = np.real(np.trace(output.dot(output)))
    spin_flip = tensor_multiplication(operator['R']-operator['L'], operator['R']-operator['L'])
    row = spin_flip*(np.asmatrix(output).H)*spin_flip
    r, v = np.linalg.eig(sqrtm(sqrtm(output).dot(row.dot(sqrtm(output)))))
    r = sorted(r, reverse=True)
    concurrence = np.real(max(0, r[0] - r[1] - r[2] - r[3]))

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
    ls = LightSource(azdeg=135, altdeg=45)
    ax = fig.add_subplot(2, 5, (1+row, 2+row), projection='3d')
    colors = cmap(norm(result_real))*0.8 + 0.2

    ax.bar3d(x, y, z, dx, dy, result_real.ravel(), color=colors, shade=True, lightsource=ls)
    # for i in range(4):
    #     for j in range(4):
    #         rounded_box(ax, i+0.5, j+0.5, result_real[i+4*j], 0.3, 20, colors[i+4*j])
    ax.set_zlim(np.min([result_real, result_imag]), np.max([result_real, result_imag]))
    ax_format(_ax=ax)
    ax.set_title("Real")

    ax2 = fig.add_subplot(2, 5, (3+row, 4+row), projection='3d')
    colors = cmap(norm(result_imag))*0.8 + 0.2

    ax2.bar3d(x, y, z, dx, dy, result_imag, color=colors, shade=True, lightsource=ls)
    ax2.set_zlim(np.min([result_real, result_imag]), np.max([result_real, result_imag]))
    ax_format(_ax=ax2)
    ax2.set_title("Imaginary")

    info = fig.add_subplot(2, 5, 5+row)
    info.text(y=1, x=0.2, s="Fidelity is %.4f"%fidelity)
    info.text(y=0.9, x=0.2, s="Concurrence is %.4f"%concurrence)
    info.text(y=0.8, x=0.2, s="Purity is %.4f"%purity)
    info.set_ylim([-0.5, 1.5])
    plt.axis('off')

plt.show()
