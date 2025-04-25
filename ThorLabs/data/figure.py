import pandas as pd
import matplotlib.pyplot as plt

tags = pd.read_csv(filepath_or_buffer="./datetime.csv", sep=',')

selection = int(input(tags["datetime"]))
tag = tags.loc[selection]["datetime"].astype(str)
print(tag)

measurement = pd.read_csv(filepath_or_buffer="./measurement_"+tag+".csv", sep=',')
position_log = pd.read_csv(filepath_or_buffer="./position_log_"+tag+".csv", sep=',')

fig, ax = plt.subplots(2)
measurement.plot(kind='line', x='position', y='coincidence counts', ax=ax[0])
position_log.plot(kind='line', y='position', ax=ax[1])

plt.show()
