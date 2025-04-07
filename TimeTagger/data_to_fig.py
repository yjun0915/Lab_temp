import numpy as np
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit

Channel_name = ['Channel A', 'Channel B', 'Coincidence']
resolution = 20
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
bin_width = 0.1
n = 2
_n = 20
font = {'family': 'serif',
        'color':  'k',
        'weight': 'normal',
        'size': 16,
        }


def gaussian(x, a, mu, sigma):
    return a * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))


# 파일 경로
file_path = "CoincidenceExampleData_16.txt"
fig = plt.figure(num=1, figsize=(16, 9))
fig1 = plt.figure(num=2, figsize=(14, 7))

# 데이터 읽기
with open(file_path, "r") as file:
    content = file.read()

with open(file_path, "r") as file:
    info = file.readlines()

# Counter data 추출
counter_match = re.search(r"Counter data:\s*array\((\[\[.*?]])\)", content, re.DOTALL)
if counter_match:
    counter_data = np.array(eval(counter_match.group(1)))
else:
    raise ValueError("Counter data not found in file.")

# Correlation data 추출
corr_match = re.search(r"Correlation data:\s*array\((\[.*?])\)", content, re.DOTALL)
if corr_match:
    correlation_data = np.array(eval(corr_match.group(1)))
else:
    raise ValueError("Correlation data not found in file.")

# X 데이터 생성
xdata = (np.arange(len(correlation_data)) - int(len(correlation_data)/2))/10 # NumPy 배열로 변환

# 초기 추정값 (A, mu, sigma)
p0 = [max(correlation_data), np.argmax(correlation_data), 10]  # A는 최대값, mu는 최댓값 위치

# 곡선 피팅 수행
coeff, var_matrix = curve_fit(f=gaussian, xdata=xdata, ydata=correlation_data, p0=p0)

# Counter Data Plot
ax1 = fig.add_subplot(2, 5, (1, 4))
for i, row in enumerate(counter_data):
    ax1.plot((np.arange(len(row))-len(row))/(bin_width*np.shape(counter_data)[1]), row, 'o-')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Count')
ax1.set_title('Counter Data')
ax1.legend((Channel_name[0], Channel_name[1], Channel_name[2]), loc=7)
ax1.grid(True)
fig.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.3)

# Correlation Data Plot
ax2 = fig.add_subplot(2, 5, (6, 9))

ax2.plot(xdata, correlation_data, marker='o', linestyle='-', color='r', label="Data")

fitted_y = gaussian(xdata, *coeff)
ax2.plot(xdata, fitted_y, linestyle="--", color="blue", label="Gaussian Fit")
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
ax3.axis('off')

ax4 = fig.add_subplot(2, 5, 10)
coeff_info = f'%s = %s \n%s = %s'%(r'$\mu$', '{:.3f}'.format(coeff[0]), r'$\sigma$', '{:.3f}'.format(coeff[2]))
ax4.text(x=0.05, y=1.001, s=coeff_info, transform=ax4.transAxes, fontsize=10, horizontalalignment='left',
         verticalalignment='top', bbox=props)
ax4.axis('off')


_ax1 = fig1.add_subplot(111)
for i, row in enumerate(counter_data):
    _ax1.plot((np.arange(len(row))-len(row))/(bin_width*np.shape(counter_data)[1]), row, 'o-', )
_ax1.set_xlabel('Time (s)')
_ax1.set_xlim(xmax=0)
_ax1.set_ylabel('Count')
_ax1.set_title('Counter Data')
_ax1.legend((Channel_name[0], Channel_name[1], Channel_name[2]), loc=7)
for i, row in enumerate(counter_data):
    ave = np.average(row[-_n:-1])
    _ax1.hlines(y=ave, xmin=-len(row[-_n:-1])/(bin_width*np.shape(counter_data)[1]), xmax=1, colors='k')
    _ax1.text(x=0.1, y=float(ave-100), s="← "+"{:.3f}".format(ave), fontdict=font)
_ax1.grid(True)
fig1.subplots_adjust(left=0.1, bottom=0.1, right=0.8, top=0.9, wspace=0.3, hspace=0.3)

plt.show()
fig.savefig(fname='result fig.png')

print("Fitted coefficients (A, mu, sigma):", coeff)

print("Coincidence Efficiency:", (2*np.average(counter_data[2][-_n:-1]))/(np.average(counter_data[0][-_n:-1]) + np.average(counter_data[1][-_n:-1]))*100)
