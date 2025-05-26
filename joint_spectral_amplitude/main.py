import sympy
import matplotlib.pyplot as plt
from sellmiere_equation import excute
from spb import plot

fig, ax = plt.subplots()
plt.axis("off")

lambda_sym, T_sym = sympy.symbols('λ T')

n_z, n_y = excute(ax, lambda_sym, T_sym)
T = 25.6667
pz = sympy.plot(n_z.subs(T_sym, T)*1e-6, (lambda_sym, 0.4, 1.8), show=False)
py = sympy.plot(n_y.subs(T_sym, T)*1e-6, (lambda_sym, 0.4, 1.8), show=False)
pz.extend(py)

T = 125.6667
pz_1 = sympy.plot(n_z.subs(T_sym, T)*1e-6, (lambda_sym, 0.4, 1.8), show=False)
py_1 = sympy.plot(n_y.subs(T_sym, T)*1e-6, (lambda_sym, 0.4, 1.8), show=False)
pz.extend(pz_1)
pz.extend(py_1)

pz = plot(n_z.subs(lambda_sym, 0.4)*1e-6 + 1.922, (T_sym, 100, 110), grid=False, show=False)
# py = sympy.plot(n_y.subs(lambda_sym, 0.4)*1e-6 + 1.880, (T_sym, 0, 180), show=False)
# pz.extend(py)



pz.show()

plt.show()
