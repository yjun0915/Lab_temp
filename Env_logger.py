import pandas as pd
import matplotlib.pyplot as plt

# 데이터 불러오기
df = pd.read_csv('env_data.csv', parse_dates=['Timestamp'])

# 이중 y축
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.grid(which='both', linestyle='dashed')
ax1.set_axisbelow(True)

# 온도용 y축
color = 'tab:red'
ax1.set_xlabel('Time')
ax1.set_ylabel('Temperature (℃)', color='k')
ax1.plot(df['Timestamp'], df['Temperature'], color='k', label='Temp', zorder=1)
ax1.tick_params(axis='y', labelcolor='k')

# 습도용 y축
# ax2 = ax1.twinx()  # 오른쪽 y축
# color = 'tab:blue'
# ax2.set_ylabel('Humidity (%)', color=color)
# ax2.plot(df['Timestamp'], df['Humidity'], color=color, label='Humidity', zorder=0)
# ax2.tick_params(axis='y', labelcolor=color)

plt.title("Temperature Over Time")
fig.autofmt_xdate()
plt.tight_layout()
plt.show()
