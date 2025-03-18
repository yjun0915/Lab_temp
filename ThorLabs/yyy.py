import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('ND_visibility_97.csv', sep=',', header=None)
data = np.array(df)
data[0] = data[1]

data = data*1000

I_max_idx = data.argmax()
I_min_idx = data.argmin()

I_max = data[I_max_idx]
I_min = data[I_min_idx]

v = (I_max-I_min)/(I_max+I_min)
print(f"visibility = {v}")
print(f"data max = {data.max()}")
print(f"data min = {data.min()}")

plt.plot(data, 'k')
plt.scatter(x=I_max_idx, y=I_max, marker="^", color='r', s=100)
plt.scatter(x=I_min_idx, y=I_min, marker="v", color='b', s=100)
plt.ylabel("Power (mW)")
plt.xlabel("Index")
plt.show()
