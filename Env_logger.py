import pandas as pd
import matplotlib.pyplot as plt

# 데이터 불러오기
df = pd.read_csv('env_data.csv', parse_dates=['Timestamp'])

# 이중 y축
fig, ax1 = plt.subplots(figsize=(10, 5))

# 온도용 y축
color = 'tab:red'
ax1.set_xlabel('Time')
ax1.set_ylabel('Temperature', color=color)
ax1.plot(df['Timestamp'], df['Temperature'], color=color, label='Temp')
ax1.tick_params(axis='y', labelcolor=color)

# 습도용 y축
ax2 = ax1.twinx()  # 오른쪽 y축
color = 'tab:blue'
ax2.set_ylabel('Humidity', color=color)
ax2.plot(df['Timestamp'], df['Humidity'], color=color, label='Humidity')
ax2.tick_params(axis='y', labelcolor=color)

plt.title("Temperature and Humidity Over Time")
fig.autofmt_xdate()
plt.tight_layout()
plt.show()
