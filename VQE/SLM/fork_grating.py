import numpy as np
import matplotlib.pyplot as plt


def fork_grating(x, y, l, a, period=5):
    phi = np.arctan2(y, x)
    grating = (2 * np.pi / period) * x
    for idx in range(len(l)):
        grating = a[idx]*np.exp(1j*l[idx] * phi)*np.exp(1j*grating)
    return grating


n = 1000
range_lim = 10
x = np.linspace(-range_lim, range_lim, n)
y = np.linspace(-range_lim, range_lim, n)
X, Y = np.meshgrid(x, y)

l = [-2, -1, 1, 2]
a = [0.1, 3, 2, 2.1]
period = 5e-1

Z = fork_grating(X, Y, l=l, a=a, period=period)

plt.figure(figsize=(6, 6))
plt.imshow(np.real(Z/4), cmap='gray', extent=[-range_lim, range_lim, -range_lim, range_lim])
plt.title(f"Fork Grating with ℓ = {l}")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar(label="Phase (radians)")
plt.tight_layout()
plt.show()
