import sympy
import matplotlib.pyplot as plt
from sellmiere_equation import excute

fig, ax = plt.subplots()
plt.axis("off")

lambda_sym, T_sym = sympy.symbols('λ T')

ax.text(x=0, y=1, s="Hello")
n_z, n_y = excute(ax, lambda_sym, T_sym)
T = 25.6667
pz = sympy.plot(n_z.subs(T_sym, T)*1e-6, (lambda_sym, 0.4, 1.8), show=False)
py = sympy.plot(n_y.subs(T_sym, T)*1e-6, (lambda_sym, 0.4, 1.8), show=False)
pz.extend(py)
pz.show()

plt.show()
