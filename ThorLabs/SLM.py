import cv2
import numpy as np

arr = np.zeros(shape=(100, 100))

x = np.linspace(start=-10, stop=10, num=100)
y = x

X, Y = np.meshgrid(x, y)

cv2.imshow()
