import numpy as np
import cv2
from screeninfo import get_monitors
import pump

monitor = get_monitors()[0]

settings = {
    "resolution": [monitor.width, monitor.height],
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

print(f"Table pixels are {table_xy}")

for px in range(1, int(settings["size"][0]/0.025)):
    px = px*(settings["size"][0]/(int(settings["size"][0]/0.025)))
    for py in range(1, int(settings["size"][1]/0.025)):
        py = py*(settings["size"][1]/(int(settings["size"][1]/0.025)))
        cv2.circle(img=canvas, center=(table_xy[1] + int(py*scale), table_xy[0] + int(px*scale)), radius=1, color=(1, 1, 1), thickness=1)
laser = pump.Pump(image=canvas, offset=table_xy, x=1.9, y=0.1, width=0.06, height=0.04, rotation=9, magnitude=scale)
canvas = laser.draw()

cv2.imshow(winname="fig_00", mat=canvas.T)
cv2.waitKey()
