import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('visibility_90.csv', sep=',', header=None)
data = np.array(df)
data[0] = 0.001

imax = data.max()
imin = data.min()

v = (imax-imin)/(imax+imin)
print(f"visibility = {v}")
plt.plot(data)
plt.show()
