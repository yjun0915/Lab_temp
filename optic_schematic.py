import cv2
import numpy as np


def main():
    canvas = np.zeros(shape=(720, 1280, 3))
    laser = pump_laser(img=canvas, wavelength=633, pos=(10, 80), size=(150, 30))
    laser.pt1, laser.pt2 = laser.calc_path()

    mirror1 = mirror(img=canvas, pos=(200, 80), size=(5, 30), rotation=0)

    cv2.line(img=canvas, pt1=laser.pt1, pt2=laser.pt2, thickness=2, color=(0, 0, 255))

    cv2.imshow('lines', canvas)
    cv2.waitKey(0)

class pump_laser():
    def __init__(self, img, wavelength, pos, size):
        end_pos = tuple(sum(elem) for elem in zip(pos, size))
        cv2.rectangle(img=img, pt1=pos, pt2=end_pos, color=(255, 255, 255))

        self.wavelength = wavelength
        self.pos = tuple(sum(elem) for elem in zip(pos, (size[0], int(size[1]/2))))
        print(self.pos)

    def calc_path(self):
        pt1, pt2 = self.pos, (1280, self.pos[1])
        return pt1, pt2

class mirror():
    def __init__(self, img, pos, size, rotation):
        r = 1 + int(np.sqrt(size[0]**2 + size[1]**2))
        sub_canvas = np.zeros(shape=(r, r, 3))
        end_pos = tuple(sum(elem) for elem in zip(pos, size))
        body = cv2.rectangle(img=sub_canvas, pt1=pos, pt2=end_pos, color=(255, 255, 255))
        M = rotate_image(img=body, angle=rotation)
        cv2.bitwise_or(src1=img, src2=M)

def rotate_image(img, angle, scale=1):
    if img.ndim > 2:
        height, width, channel = img.shape
    else:
        height, width = img.shape

    matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, scale)
    result = cv2.warpAffine(img, matrix, (width, height))

    return result

if __name__ == "__main__":
    main()
