import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

image = cv2.imread('IMG_0109.jpg', cv2.IMREAD_COLOR)

if image is None:
    raise FileNotFoundError("이미지를 찾을 수 없습니다. 경로를 확인하세요.")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

canny_image = cv2.Canny(image=gray_image, threshold1=120, threshold2=200, apertureSize=3, L2gradient=True, )
canny_image_2 = cv2.Canny(image=gray_image, threshold1=120, threshold2=200, apertureSize=5, L2gradient=True, )

lines = cv2.HoughLinesP(image=canny_image, rho=10, theta=np.pi/180, threshold=160, minLineLength=0, maxLineGap=0)
'''
cv2.HoughLinesP(image, rho, theta, threshold, lines=None, minLineLength=None, maxLineGap=None) -> lines
- image: 입력 에지 영상
- rho: 축적 배열에서 rho 값의 간격. (e.g.) 1.0 : 1픽셀 간격.
- theta: 축적 배열에서 theta 값의 간격. (e.g.) np.pi / 180 : 1° 간격.
- threshold: 축적 배열에서 직선으로 판단할 임계값
- lines: 선분의 시작과 끝 좌표(x1, y1, x2, y2) 정보를 담고 있는 numpy.ndarray.
- minLineLength: 검출할 선분의 최소 길이
- maxLineGap: 직선으로 간주할 최대 에지 점 간격
'''
hough_image = cv2.cvtColor(canny_image, cv2.COLOR_GRAY2BGR)
# for i in range(np.shape(hough_image)[0]):
#     for j in range(np.shape(hough_image)[1]):
#         hough_image[i][j] = np.add(hough_image[i][j], [canny_image_2[i][j], canny_image_2[i][j], 0])

line_filter = 1/20

dot_map = np.zeros(shape=(np.shape(hough_image)[0], np.shape(hough_image)[1]))

if lines is not None:
    print(f"Total number of Lines are {np.shape(lines)[0]}. ")
    for i in range(lines.shape[0]):
            pt1 = (lines[i][0][0], lines[i][0][1]) #시작점 좌표
            pt2 = (lines[i][0][2], lines[i][0][3]) #끝점 좌표
            if math.dist(pt1, pt2) < line_filter:
                cv2.line(hough_image, pt1, pt2, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.line(dot_map, pt1, pt2, 1, 2, cv2.LINE_AA)

dft = cv2.dft(src=np.float32(dot_map), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

magnitude_spectrum1 = 0.02*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

plt.plot(magnitude_spectrum1[int(np.shape(magnitude_spectrum1)[0]/4)][:])
plt.show()

cv2.imshow(winname="spec", mat=magnitude_spectrum1)
cv2.imshow(winname="fig_0", mat=dot_map)
cv2.imshow(winname="fig_00", mat=hough_image)
cv2.waitKey()