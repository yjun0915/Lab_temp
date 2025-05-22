import cv2
import numpy as np
import sympy
from sympy import Symbol
from sympy.printing.latex import latex

debug = False

### DOMAIN ###
domain = [-10, 10, 500]
x = np.linspace(start=domain[0], stop=domain[1], num=domain[2])
y = x
X, Y = np.meshgrid(x, y)

### FUNCTION ###
r, phi, z = sympy.symbols('r φ z', real=True)
w_0, k, z_R = sympy.symbols('w_0 k z_R')
# hybrid binary fork grating

# Laguerre-Gaussian function
def _w(w_0, z, z_R):
    return w_0*sympy.sqrt(1+(z/z_R)**2)

def _R(z, z_R):
    return (z**2 + z_R**2)/z

def _G(w_0, w, r, k, phi, z, R):
        return (w_0/w)*sympy.exp(-r**2/w**2)*sympy.exp(-sympy.I*k*z - (sympy.I*k*r**2/(2*R)))

w = _w(w_0, z, z_R)
if debug: print(latex(w))

R = _R(z, z_R)
if debug: print(latex(R))

G = _G(w_0, w, r, k, phi, z, R)
if debug: sympy.pprint(latex(G))

_k = 2*sympy.pi*12345.67901235  # cm^-1
_w_0 = 10e-5
_z_R = (_w_0**2)*_k/2

G = G.subs({w_0:_w_0, k:_k, z_R:_z_R})

sympy.plotting.plot3d(sympy.Abs(G), (r, -1e-3, 1e-3), (z, -1e-3, 1e-3))

phase = np.exp((X + Y*1j)*2*np.pi/(X**2 + Y**2))

amplitude = phase
intensity = amplitude*np.conj(amplitude)

cv2.imshow(winname='intensity', mat=intensity.real)
cv2.waitKey()
