from LightPipes import *
import matplotlib.pyplot as plt


wavelength = 500 * nm
size = 15 * mm
N = 200
w0 = 3 * mm
i = 0
LG = True


F = Begin(size, wavelength, N)
F = GaussBeam(F, w0, LG=LG, n=0, m=0)
I = Intensity(0, F)
F=PhaseSpiral(F,m=1)
phase=Phase(F,unwrap=True)

plt.imshow(phase, cmap='jet',vmin=0., vmax=7)
plt.colorbar()

plt.show()
