import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(filepath_or_buffer='log.csv', sep=',', index_col=0)
data.plot()
plt.show()
