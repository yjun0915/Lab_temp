import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 불러오기
data = pd.read_csv('SPCM_AQRH_12_FC.csv')

font = {'family': 'serif',
        'color':  'k',
        'weight': 'normal',
        'size': 16,
        }

# x와 y 열을 추출
x = data['x']
y = data['y']

# 그래프 그리기
plt.figure(figsize=(8, 5))
plt.scatter(x, y, marker='.', s=1, color='green')
plt.scatter(809.8720078262731, 60.63886469303951, color='r')
plt.text(819.8720078262731, 61.63886469303951, '(809.872, 60.638)', fontdict=font)
plt.title('SPCM-AQRH Typical Detection Efficiency')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Photon Detection Efficiency (PDE)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
