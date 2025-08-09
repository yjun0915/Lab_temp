from LightPipes import *
from tqdm import trange

import matplotlib.pyplot as plt
import numpy as np

import cv2


wavelength = 405 * nm
size = 55 * mm
N = 700
waist = 1.9 * mm

f1 = 15 * mm

seg = 0.1e-3
len = 2*f1

F = Begin(size=size, labda=wavelength, N=N)
F = GaussBeam(Fin=F, w0=waist)
F = Lens(Fin=F, f = f1)

movie = [np.zeros_like(a=F.field) for _ in range(int(len/seg))]
n = np.shape(movie)[0]

for idx in trange(n):
    F = Forvard(Fin=F, z=seg*m)
    frame = Intensity(F)
    movie[idx] = frame
    cv2.imshow('Grayscale Video', frame)
    key = cv2.waitKey(20)

    if key == 27:
        break

for i in range(n):
    frame = movie[i]
    cv2.imshow('Grayscale Video', frame)
    key = cv2.waitKey(2)

    if key == 27:
        break

cv2.destroyAllWindows()