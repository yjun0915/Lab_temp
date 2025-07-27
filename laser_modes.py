import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.hermite import Hermite
from numpy.polynomial.laguerre import Laguerre
from matplotlib.colors import hsv_to_rgb

H0 = Hermite(coef=(0, 1, 0), domain=(-3, 3))
H1 = Hermite(coef=(0, 1), domain=(-3, 3))

L0 = Laguerre(coef=(1, 0), domain=(-3, 3))
L1 = Laguerre(coef=(0, 1), domain=(-3, 3))
print(L1)

x = np.linspace(-3, 3, 500)
y = x

X, Y = np.meshgrid(x, y)

R = np.sqrt(X**2 + Y**2)
A = np.arctan2(X, Y)

l, p = 1, 4

Z = H0(1.4*X)*H1(1.4*Y)*np.exp(-(X**2 + Y**2))
L = L1(2 * R**2) * np.exp(-R**2) * np.exp(1j * l * A)

intensity = np.abs(L)
phase = np.angle(L)

intensity_norm = intensity / np.max(intensity)
phase_norm = (phase + np.pi) / (2 * np.pi)

H = phase_norm               # Hue: phase
S = np.ones_like(H)          # Saturation: 고정
V = intensity_norm           # Value: intensity
HSV = np.stack((H, S, V), axis=-1)
RGB = hsv_to_rgb(HSV)

plt.imshow(RGB)
plt.colorbar()
plt.title("Physicist's Hermite Polynomial H₂(x)")
plt.xlabel("x")
plt.ylabel("H(x)")
plt.grid(True)
plt.show()
