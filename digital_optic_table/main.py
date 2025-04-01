from turtledemo.penrose import start

import numpy as np
import cv2

import pump

settings = {
    "resolution": [1280, 720],
    "size": [2, 0.8]
}

canvas = np.zeros(shape=(settings["resolution"][0], settings["resolution"][1]))

scale = 1
if settings["resolution"][0]/settings["resolution"][1] >= settings["size"][0]/settings["size"][1]:
    scale = settings["resolution"][1]/settings["size"][1]
elif settings["resolution"][0]/settings["resolution"][1] <= settings["size"][0]/settings["size"][1]:
    scale = settings["resolution"][0]/settings["size"][0]
print(f"scale: {scale}")
table_xy = [
    int((settings["resolution"][0]-(settings["size"][0]*scale))/2),
    int((settings["resolution"][1]-(settings["size"][1]*scale))/2),
    int((settings["resolution"][0]+(settings["size"][0]*scale))/2)-1,
    int((settings["resolution"][1]+(settings["size"][1]*scale))/2)-1
]
for idx in range(table_xy[0], table_xy[2]):
    canvas[idx][table_xy[1]] = 1
    canvas[idx][table_xy[3]] = 1
for idx in range(table_xy[1], table_xy[3]):
    canvas[table_xy[0]][idx] = 1
    canvas[table_xy[2]][idx] = 1

for px in range(1, int(settings["size"][0]/0.025)):
    px = px*(settings["size"][0]/(int(settings["size"][0]/0.025)))
    for py in range(1, int(settings["size"][1]/0.025)):
        py = py*(settings["size"][1]/(int(settings["size"][1]/0.025)))
        cv2.circle(img=canvas, center=(table_xy[1] + int(py*scale), table_xy[0] + int(px*scale)), radius=1, color=(1, 1, 1), thickness=1)
laser = pump.Pump(image=canvas, x=0.15, y=0.15, width=0.2, height=0.07, magnitude=scale)
canvas = laser.draw()

cv2.imshow(winname="fig_00", mat=canvas.T)
cv2.waitKey()