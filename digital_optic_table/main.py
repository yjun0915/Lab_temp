import numpy as np
import cv2

import pump

canvas = np.zeros(shape=(720, 1280))

laser = pump.Pump(image=canvas, x=15, y=15, width=20, height=7, magnitude=10)
canvas = laser.draw()

cv2.imshow(winname="fig_00", mat=canvas)
cv2.waitKey()