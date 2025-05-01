import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('TkAgg')

def v_line(x, a, b, c, d, h):
    output_list = []
    for pos in x:
        output_list.append(min(a*pos + b, abs(c*pos + d) + h))
    return output_list

def onSelect(event):
    selection = listbox.curselection()
    if selection:
        index = selection[0]
        value = listbox.get(index)
        print(f"선택된 항목: {value}")

tags = pd.read_csv(filepath_or_buffer="./datetime.csv", sep=',', index_col=0)

window = tk.Tk()
listbox = tk.Listbox(master=window)
listbox.pack(side=tk.RIGHT, fill=tk.BOTH)
for v in tags['datetime']:
    listbox.insert(tk.END, v)
listbox.bind('<<ListboxSelect>>', onSelect)

selection = 36
tag = tags.loc[selection]["datetime"].astype(str)

measurement = pd.read_csv(filepath_or_buffer="./measurement_"+tag+".csv", sep=',', index_col=0)
position_log = pd.read_csv(filepath_or_buffer="./position_log_"+tag+".csv", sep=',', index_col=0)
new_row = measurement['coincidence counts'].div(np.sqrt(measurement['A channel counts'].mul(measurement['B channel counts'])))

fig, ax = plt.subplots(3)
measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax[0], s=5)
new_row.plot(kind='line', ax=ax[1])
position_log.plot(kind='line', y='position', ax=ax[2], lw=0.5)
position_log.reset_index().plot(kind='scatter', x='index', y='position', ax=ax[2], s=0.1)

p0 = [0, 100, 0, 0, 0]
coeff, var_matrix = curve_fit(f=v_line, xdata=measurement['position'], ydata=measurement['coincidence counts'], p0=p0)

fitting = pd.DataFrame(data={'x':measurement['position'], 'y':v_line(measurement['position'], coeff[0], coeff[1], coeff[2], coeff[3], coeff[4])})
fitting.plot(kind='line', x='x', y='y', ax=ax[0], color='r', legend=False)

min_idx = measurement['coincidence counts'].idxmin()

visibility = 1 - (measurement['coincidence counts'][min_idx]/(measurement['position'][min_idx]*coeff[0] + coeff[1]))

visibility_spot = pd.DataFrame(data={
    'position':[measurement['position'][min_idx], measurement['position'][min_idx]],
    'coincidence counts':[measurement['coincidence counts'][min_idx], (measurement['position'][min_idx]*coeff[0] + coeff[1])]
})
visibility_spot.plot(kind='scatter', x='position', y='coincidence counts', ax=ax[0], s=3, color='r')

print("Visibility of this data is %.2f"%(visibility*100)+"%")

canvas = FigureCanvasTkAgg(figure=fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack()
window.mainloop()
