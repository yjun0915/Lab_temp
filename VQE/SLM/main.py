import cv2
import numpy as np
import sympy
from sympy.printing.latex import latex

### DOMAIN ###
domain = [-10, 10, 500]
x = np.linspace(start=domain[0], stop=domain[1], num=domain[2])
y = x
X, Y = np.meshgrid(x, y)

### FUNCTION ###
# hybrid binary fork grating

# Laguerre-Gaussian function
r = sympy.symbols(names='r', type='real')
phi = sympy.symbols(names='φ', type='real')
z = sympy.symbols(names='z', type='real')
L = sympy.Function('L')(r, phi, z)
G = sympy.Function('G')(r, phi, z)


LG = sympy.Function(r'LG^{l}_{p}')(r, phi, z)

phase = np.exp((X + Y*1j)*2*np.pi/(X**2 + Y**2))

amplitude = phase
intensity = amplitude*np.conj(amplitude)

cv2.imshow(winname='intensity', mat=intensity.real)
cv2.waitKey()
