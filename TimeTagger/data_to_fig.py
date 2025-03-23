import numpy as np
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit

Channel_name = ['Channel A', 'Channel B', 'Coincidence']
resolution = 20
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
count_delay = 0.1


def gaussian(x, A, mu, sigma):
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))


# 파일 경로
file_path = "CoincidenceExampleData.txt"
fig = plt.figure(num=1, figsize=(16, 9))

# 데이터 읽기
with open(file_path, "r") as file:
    content = file.read()

with open(file_path, "r") as file:
    info = file.readlines()

# Counter data 추출
counter_match = re.search(r"Counter data:\s*array\((\[\[.*?\]\])\)", content, re.DOTALL)
if counter_match:
    counter_data = np.array(eval(counter_match.group(1)))
else:
    raise ValueError("Counter data not found in file.")

# Correlation data 추출
corr_match = re.search(r"Correlation data:\s*array\((\[.*?\])\)", content, re.DOTALL)
if corr_match:
    correlation_data = np.array(eval(corr_match.group(1)))
else:
    raise ValueError("Correlation data not found in file.")

# X 데이터 생성
xdata = np.arange(len(correlation_data))  # NumPy 배열로 변환

# 초기 추정값 (A, mu, sigma)
p0 = [max(correlation_data), np.argmax(correlation_data), 10]  # A는 최대값, mu는 최댓값 위치

# 곡선 피팅 수행
coeff, var_matrix = curve_fit(gaussian, xdata, correlation_data, p0=p0)

# Counter Data Plot
ax1 = fig.add_subplot(2, 5, (1, 4))
for i, row in enumerate(counter_data):
    ax1.plot(row, marker='o', linestyle='-', label=Channel_name[i])
plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], labels=(-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, "0.0"))
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Count')
ax1.set_title('Counter Data')
ax1.legend()
ax1.grid(True)

# Correlation Data Plot
ax2 = fig.add_subplot(2, 5, (6, 9))

ax2.plot(xdata, correlation_data, marker='o', linestyle='-', color='r', label="Data")

# 가우시안 피팅된 곡선 추가
gauss_xdata = np.array([idx/resolution for idx in range(len(correlation_data)*resolution)])
fitted_y = gaussian(gauss_xdata, *coeff)
ax2.plot(gauss_xdata, fitted_y, linestyle="--", color="blue", label="Gaussian Fit")
plt.xticks(ticks=[5, 15, 25, 35, 45], labels=(-2, -1, "0.0", "+1.0", "+2.0"))
ax2.set_xlabel('Time (ns)')
ax2.set_ylabel('Correlation')
ax2.set_title('Correlation Data with Gaussian Fit')
ax2.legend()
ax2.grid(True)

ax3 = fig.add_subplot(255)
info_str = info[0]
for idx in range(1, 10):
    info_str = info_str + '\n' + info[idx]
ax3.text(x=0.05, y=1.001, s=info_str, transform=ax3.transAxes, fontsize=10, horizontalalignment='left',
         verticalalignment='top', bbox=props)
plt.axis('off')

ax4 = fig.add_subplot(2, 5, 10)
coeff_info = f'$\mu$ = {coeff[0]} \n $\sigma$ = {coeff[2]}'
ax4.text(x=0.05, y=1.001, s=coeff_info, transform=ax4.transAxes, fontsize=10, horizontalalignment='left',
         verticalalignment='top', bbox=props)
plt.axis('off')

plt.show()
fig.savefig(fname='result fig.png')

# 피팅된 파라미터 출력
print("Fitted coefficients (A, mu, sigma):", coeff)

print((2*counter_data[2][-1]/(counter_data[0][-1] + counter_data[1][-1]))*100)
