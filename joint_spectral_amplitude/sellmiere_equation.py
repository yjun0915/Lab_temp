import sympy
from sympy.printing.latex import latex

a = [
    [
        [
            [9.9587, 9.9228, -8.9603, 4.1010]
        ],
        [
            [-1.1882, 10.459, -9.8136, 3.1481]
        ]
    ],
    [
        [
            [6.2897, 6.3061, -6.0629, 2.6486]
        ],
        [
            [-0.14445, 2.2244, -3.5770, 1.3470]
        ]
    ]
]
'''
a[0][0][:] = [a0, a1, a2, a3]   # z-axis n1
a[0][1][:] = [a0, a1, a2, a3]   # z-axis n2
a[1][0][:] = [a0, a1, a2, a3]   # y-axis n1
a[1][1][:] = [a0, a1, a2, a3]   # y-axis n2
'''

def excute(ax, lambda_sym, T_sym):
    expr_z = n_i(a[0][0][0], lambda_sym)*(T_sym - 25) + n_i(a[0][1][0], lambda_sym)*((T_sym - 25)**2)
    expr_y = n_i(a[1][0][0], lambda_sym)*(T_sym - 25) + n_i(a[1][1][0], lambda_sym)*((T_sym - 25)**2)
    ax.text(x=0, y=0.5, s=f"${latex(expr_z)}$")
    return expr_z, expr_y

def n_i(alist, lambda_sym):
    terms = [alist[j]/(lambda_sym**j) for j in range(len(alist))]
    return sum(terms)
