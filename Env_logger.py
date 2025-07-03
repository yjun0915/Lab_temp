import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(filepath_or_buffer='./env_data.csv', sep=',')
fig, ax = plt.subplots()
data['Temperature (C)'].plot(ax=ax)
(data['Humidity (%)']*45/100).plot(ax=ax)

ax.set_ylim([0, 20])

plt.show()
