import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(filepath_or_buffer="./QST_data_97.csv", index_col=0)

basis = ["HH", "HV", "VV", "VH", "DD", "DA", "AA", "AD"]

heights = [data["Coincidence counts"][row].item() for row in basis]

print(heights)

plt.bar([0, 1, 2, 3, 4, 5, 6, 7], heights)
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7], basis)

plt.show()
