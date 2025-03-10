import cv2
import numpy as np

def main():
    canvas = np.zeros(shape=(720, 1280, 3))
    laser = pump_laser(wavelength=633, pos=(0, 0))
    cv2.line(img=canvas, pt1=laser.calc_path(), pt2=(100, 100), thickness=2, color=(0, 0, 255))

    cv2.imshow('lines', canvas)
    cv2.waitKey(0)

class pump_laser():
    def __init__(self, wavelength, pos):
        self.wavelength = wavelength
        self.pos = pos

    def calc_path(self):
        return self.pos

if __name__ == "__main__":
    main()
