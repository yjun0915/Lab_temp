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

### CONSTANTS ###
_k = 2*sympy.pi*12345.67901235  # cm^-1
_w_0 = 10e-5
_z_R = (_w_0**2)*_k/2
_l = 2
_p = 6

### FUNCTION ###
sym_r, sym_phi, sym_z = sympy.symbols('r φ z', real=True)
sym_w_0, sym_k, sym_z_R = sympy.symbols('w_0 k z_R')
sym_l, sym_p = sympy.symbols('l p', integer=True)
func_w = sympy.Function('w')(sym_z)
func_R = sympy.Function('R')(sym_z)
func_zeta = sympy.Function('ζ')(sym_r, sym_z)
# hybrid binary fork grating

# Laguerre-Gaussian function
def _w(w_0, z, z_R):
    return w_0*sympy.sqrt(1+(z/z_R)**2)
def _R(z, z_R):
    return (z**2 + z_R**2)/z
def _zeta(r, w):
    return (2*r**2)/(w**2)
def _G(w_0, w, r, k, phi, z, R):
        return (w_0/w)*sympy.exp(-r**2/w**2)*sympy.exp(-sympy.I*k*z - (sympy.I*k*r**2/(2*R)))
def _L(l, p, zeta):
    i = sympy.symbols('i')
    return sympy.summation(((-1)**i)*sympy.binomial(p+sympy.Abs(l), p-i)*(zeta**i)/sympy.factorial(i), (i, 0, p))

w = _w(sym_w_0, sym_z, sym_z_R)
if debug: print(latex(w))
R = _R(sym_z, sym_z_R)
if debug: print(latex(R))
zeta = _zeta(sym_r, w)
if debug: print(latex(zeta))
G = _G(sym_w_0, func_w, sym_r, sym_k, sym_phi, sym_z, func_R)
if debug: print(latex(G))
L = _L(sym_l, sym_p, func_zeta)
if debug: print(latex(L))

L = L.subs({func_zeta:zeta}).subs({sym_l:_l, sym_p:_p, sym_w_0:_w_0, sym_z_R:_z_R})
G = G.subs({func_w:w, func_R:R}).subs({sym_w_0:_w_0, sym_k:_k, sym_z_R:_z_R})

sympy.plotting.plot3d(sympy.Abs((L*G*sympy.exp(-1*sympy.I*_l*sym_phi))), (sym_r, -1e-3, 1e-3), (sym_z, -1e-3, 1e-3))

# phase = np.exp((X + Y*1j)*2*np.pi/(X**2 + Y**2))
#
# amplitude = phase
# intensity = amplitude*np.conj(amplitude)
#
# cv2.imshow(winname='intensity', mat=intensity.real)
# cv2.waitKey()
