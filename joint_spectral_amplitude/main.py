import sympy
import matplotlib.pyplot as plt
from sellmiere_equation import excute
from spb import plot3d
from sympy.utilities.lambdify import lambdify
import numpy as np

c = 299792485e6
pi = 3.141592

fig, ax = plt.subplots()
plt.axis("off")

lambda_sym, T_sym = sympy.symbols('λ T')

n_z, n_y = excute(ax, lambda_sym, T_sym)

pz = plot3d(n_z*1e-6, (T_sym, 0, 110), (lambda_sym, 0.4, 1.8), grid=False, line_color='black', show=False)
# pz.show()

idler = sympy.symbols("λ_{i}")

idler_n_z, idler_n_y = excute(ax, idler, T_sym)

phase_mismatch = (2*pi*c/0.4054378) - (1*pi*c*(idler_n_z*1e-6 + 1.9)/idler) - (1*pi*c*(n_z*1e-6 + 1.9)/lambda_sym) + (2*pi)/9.825

PM = sympy.sinc((phase_mismatch*10e3)/2)

# plot_PM = plot_contour(PM.subs(T_sym, 109), (idler, 0.7, 0.9), (lambda_sym, 0.7, 0.9), grid=False, show=False, n=300, colorbar=cm.coolwarm, use_cm=True)
# plot_PM.show()

lambda_PM = lambdify((idler, lambda_sym), PM.subs(T_sym, 109))

l1 = 0.7
l2 = 0.92

x = np.linspace(l1, l2, 1000)
y = x
X, Y = np.meshgrid(x, y)

amplitude = lambda_PM(X, Y)

plt.imshow(amplitude, cmap='bwr')
plt.colorbar()
pz.show()
