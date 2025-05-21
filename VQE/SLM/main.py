import cv2
import numpy as np
import sympy
from sympy import Symbol
from sympy.printing.latex import latex

debug = True

### DOMAIN ###
domain = [-10, 10, 500]
x = np.linspace(start=domain[0], stop=domain[1], num=domain[2])
y = x
X, Y = np.meshgrid(x, y)

### FUNCTION ###
# hybrid binary fork grating

# Laguerre-Gaussian function
k, w_0, z_R = sympy.symbols(r'k, w_0, z_R')

def _w(z):
    return w_0*sympy.sqrt(1+(z/z_R)**2)
w = _w(Symbol('z'))
if debug: print(w)
def _R(z):
    return (z**2 + z_R**2)/z
R = _R(Symbol('z'))
if debug: print(R)
def _G(r, phi, z):
        return (w_0/w)*sympy.exp(-r**2/w**2)*sympy.exp(-sympy.I*k*z - (sympy.I*k*r**2/(2*R)))
G = _G(Symbol('r'), Symbol('φ'), Symbol('z'))
if debug: print(latex(G))

k = 2*sympy.pi*12345.67901235  # cm^-1
w_0 = 10e-5
z_R = (w_0**2)*k/2

sympy.plotting.plot3d(G.subs([(z_R, z_R), (w_0, w_0), (k, k)]))

phase = np.exp((X + Y*1j)*2*np.pi/(X**2 + Y**2))

amplitude = phase
intensity = amplitude*np.conj(amplitude)

cv2.imshow(winname='intensity', mat=intensity.real)
cv2.waitKey()
