import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('TkAgg')

# Global valiables
fig, ax = plt.subplots(3)


# Event functions
def v_line(x, a, b, c, d, h):
    output_list = []
    for pos in x:
        output_list.append(min(a*pos + b, abs(c*pos + d) + h))
    return output_list


def onSelect(event):
    _selection = listbox.curselection()
    if _selection:
        index = _selection[0]
        value = str(listbox.get(index))
        make_figure(get_selection=value)


def exitClick():
    window.destroy()
    window.quit()
    exit()


def state_count():
    global s_count
    s_count = not s_count
    print(s_count)


def state_efficient():
    global s_efficient
    s_efficient = not s_efficient
    print(s_efficient)


def state_position():
    global s_position
    s_position = not s_position
    print(s_position)


# Main figure function
def make_figure(get_selection):
    global canvas
    global fig, ax

    ax[0].cla()
    ax[1].cla()
    ax[2].cla()

    tag = get_selection

    measurement = pd.read_csv(filepath_or_buffer="./measurement_"+tag+".csv", sep=',', index_col=0)
    position_log = pd.read_csv(filepath_or_buffer="./position_log_"+tag+".csv", sep=',', index_col=0)
    new_row = measurement['coincidence counts'].div(np.sqrt(measurement['A channel counts'].mul(measurement['B channel counts'])))

    measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax[0], s=5)
    new_row.plot(kind='line', ax=ax[1])
    position_log.plot(kind='line', y='position', ax=ax[2], lw=0.5)
    position_log.reset_index().plot(kind='scatter', x='index', y='position', ax=ax[2], s=0.1)

    p0 = [0, measurement['coincidence counts'].mean(), 1, 0, measurement['coincidence counts'].min()]
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

    display.config(text="Visibility of this data is %.2f"%(visibility*100)+"%")

    ax[0].set_ylim(ymin=0)
    canvas.draw()
    canvas.get_tk_widget().pack()

width = 900
height = 600
fig_width = 600
wgt_width = width - fig_width

tags = pd.read_csv(filepath_or_buffer="./datetime.csv", sep=',', index_col=0)

window = tk.Tk()
window.geometry("%dx%d"%(width, height))
window.wm_attributes("-topmost", 1)

figure_frame = tk.Frame(master=window, width=fig_width, height=height)
figure_frame.pack(side=tk.LEFT)
widget_frame = tk.Frame(master=window, width=wgt_width, height=height)
widget_frame.pack(side=tk.RIGHT)

scroll_frame = tk.Frame(master=widget_frame)
scrollbar = tk.Scrollbar(master=scroll_frame)
scrollbar.pack(side=tk.RIGHT, fill="y")
listbox = tk.Listbox(master=scroll_frame, yscrollcommand=scrollbar.set)
for tag in tags['datetime']:
    listbox.insert(tk.END, tag)
listbox.pack(side=tk.TOP, fill=tk.BOTH)
listbox.bind('<<ListboxSelect>>', onSelect)
scrollbar.config(command=listbox.yview)
scroll_frame.pack()

state_field = tk.Frame(master=widget_frame, width=wgt_width, height=60)
state_field.pack()
s_count = True
s_efficient = False
s_position = False
check_count = tk.Button(master=state_field, text='counts', command=state_count)
check_efficient = tk.Button(master=state_field, text='efficiency', command=state_efficient)
check_position = tk.Button(master=state_field, text='position', command=state_position)
check_count.grid(row=0, column=0)
check_efficient.grid(row=0, column=1)
check_position.grid(row=0, column=2)

display = tk.Label(master=widget_frame, height=1, width=wgt_width, text='', borderwidth=5, relief='ridge')
display.pack(side=tk.TOP, fill=tk.BOTH)

exit_button = tk.Button(master=widget_frame, text="EXIT", command=exitClick)
exit_button.pack(side=tk.TOP, fill=tk.BOTH)

canvas = FigureCanvasTkAgg(figure=fig, master=figure_frame)

make_figure(get_selection=str(tags.loc[0]['datetime']))

window.mainloop()
