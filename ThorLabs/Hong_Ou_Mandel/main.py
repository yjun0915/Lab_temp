import asyncio
import threading
import matplotlib
import os
import execution
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import curve_fit
matplotlib.use('TkAgg')

# initial value
_start_point = 0.0189
_end_point = 0.0208
_data_num = 97
_binwidth = 1500.0
_n_value = 2
_delay = [50, 0]

# Global valiables
fig, ax = plt.subplots()
t_efficient = ax.twinx()
t_position = ax.twinx()
g_selection = 0

# Event functions
def v_line(x, a, b, c, d, h):
    output_list = []
    for pos in x:
        output_list.append(min(a*pos + b, abs(c*pos + d) + h))
    return output_list


async def executeClick():
    global tags, start_point, end_point, data_num, binwidth, n_value, description_write
    inputs = np.asarray([
        float(start_point.get()),
        float(end_point.get()),
        float(data_num.get()),
        float(binwidth.get()),
        float(n_value.get()),
        float(Adelay.get()),
        float(Bdelay.get())
    ])
    desc = description_write.get()
    exp = execution.Experiment(inputs, desc)
    await exp.execute()
    listbox.insert(tk.END, pd.read_csv("./data/datetime.csv")["datetime"].iloc[-1])
    tags = pd.read_csv(filepath_or_buffer="./data/datetime.csv", sep=',', index_col=0)
    make_figure(get_selection=-1)
    del exp


def handle_execute_click():
    threading.Thread(target=lambda: asyncio.run(executeClick())).start()


def onSelect(event):
    _selection = listbox.curselection()
    if _selection:
        global g_selection, tags
        index = _selection[0]
        g_selection = index
        description.config(text=str(tags.loc[index]["description"]))
        make_figure(get_selection=g_selection)


def deleteClick():
    global tags
    os.remove("./data/measurement_"+str(int(tags.loc[g_selection]['datetime']))+".csv")
    os.remove("./data/position_log_"+str(int(tags.loc[g_selection]['datetime']))+".csv")
    tags.drop(index=g_selection, inplace=True)
    tags.reset_index(drop=True, inplace=True)
    tags.to_csv(path_or_buf="./data/datetime.csv")
    listbox.delete(g_selection)
    window.update()


def exitClick():
    window.destroy()
    window.quit()
    exit()


def state_count():
    global s_count, g_selection
    s_count = not s_count
    make_figure(get_selection=g_selection)


def state_efficient():
    global s_efficient, g_selection
    s_efficient = not s_efficient
    make_figure(get_selection=g_selection)


def state_fitting():
    global s_fitting, g_selection
    s_fitting = not s_fitting
    make_figure(get_selection=g_selection)


# Main figure function
def make_figure(get_selection):
    global canvas
    global fig, ax, t_efficient, t_position
    global s_count, s_efficient, s_fitting

    ax.cla()
    ax.axis('off')
    t_efficient.cla()
    t_efficient.axis('off')
    t_position.cla()
    t_position.axis('off')

    tag = str(int(tags['datetime'].iloc[get_selection]))

    measurement = pd.read_csv(filepath_or_buffer="./data/measurement_"+tag+".csv", sep=',', index_col=0)
    coin_effi_line = pd.DataFrame(
        data={'position':measurement['position'],
              'efficient':100*measurement['coincidence counts'].div(np.sqrt(measurement['A channel counts'].mul(measurement['B channel counts'])))
              })

    ax.set_xlim(xmin=measurement['position'].min(), xmax=measurement['position'].max())
    ax.set_xticks(
        ticks=np.concatenate([measurement['position'][
                              int(measurement['position'].shape[0] / 2):0:-int(measurement['position'].shape[0] / 5)],
                              measurement['position'][
                              int(measurement['position'].shape[0] / 2):-1:int(measurement['position'].shape[0] / 5)]],
                             0),
        labels=(1e3) * np.round(
            np.concatenate([measurement['position'][int(measurement['position'].shape[0] / 2):0:-int(
                measurement['position'].shape[0] / 5)], measurement['position'][
                                                        int(measurement['position'].shape[0] / 2):-1:int(
                                                            measurement['position'].shape[0] / 5)]], 0), 4)

    )

    p0 = [0, measurement['coincidence counts'].max(), 1, 0, measurement['coincidence counts'].min()]
    coeff, var_matrix = curve_fit(f=v_line, xdata=measurement['position'], ydata=measurement['coincidence counts'], p0=p0)
    coeff[0] = 0

    fitting_position = np.linspace(start=measurement['position'].min(), stop=measurement['position'].max(), num=1000)
    fitting = pd.DataFrame(data={'x':fitting_position, 'y':v_line(fitting_position, coeff[0], coeff[1], coeff[2], coeff[3], coeff[4])})

    min_idx = fitting['y'].idxmin()

    visibility = 1 - (fitting['y'][min_idx])/(coeff[1] + coeff[0]*fitting['x'][min_idx])

    display.config(text="Visibility of this data is %.2f"%(visibility*100)+"%")

    if s_efficient:
        coin_effi_line.plot(kind='scatter', x='position', y='efficient', ax=t_efficient)
        t_efficient.axis('on')
        t_efficient.set_xlim(xmin=measurement['position'].min(), xmax=measurement['position'].max())

    if s_fitting:
        fitting.plot(kind='line', x='x', y='y', ax=ax, color='r', legend=False)

    if s_count:
        measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax, s=5)

        ax.axis('on')
        ax.set_ylabel("coincidence counts")
        ax.set_xlabel("position (mm)")
        ax.set_ylim(ymin=0)

    canvas.draw()

width = 900
height = 600
fig_width = 600
wgt_width = width - fig_width

tags = pd.read_csv(filepath_or_buffer="./data/datetime.csv", sep=',', index_col=0)

window = tk.Tk()
window.geometry("%dx%d"%(width, height))
window.wm_attributes("-topmost", 1)

figure_frame = tk.Frame(master=window, width=fig_width, height=height)
figure_frame.pack(side=tk.LEFT)
widget_frame = tk.Frame(master=window, width=wgt_width, height=height)
widget_frame.pack(side=tk.RIGHT)

# execute experiment
experiment_frame = tk.Frame(master=widget_frame, width=wgt_width, borderwidth=5, relief='ridge')
experiment_frame.pack(fill=tk.BOTH)
tk.Label(master=experiment_frame, text='[ Experiment execution ]').pack()

input_frame = tk.Frame(master=experiment_frame)
input_frame.pack()
tk.Label(master=input_frame, text='Start position').grid(row=0, column=0)
start_point = tk.Entry(master=input_frame)
start_point.grid(row=0, column=1)
start_point.insert(index=0, string=str(_start_point))
tk.Label(master=input_frame, text='End position').grid(row=1, column=0)
end_point = tk.Entry(master=input_frame)
end_point.grid(row=1, column=1)
end_point.insert(index=0, string=str(_end_point))
tk.Label(master=input_frame, text='Number of data').grid(row=2, column=0)
data_num = tk.Entry(master=input_frame)
data_num.grid(row=2, column=1)
data_num.insert(index=0, string=str(_data_num))
tk.Label(master=input_frame, text='Bin width').grid(row=3, column=0)
binwidth = tk.Entry(master=input_frame)
binwidth.grid(row=3, column=1)
binwidth.insert(index=0, string=str(_binwidth))
tk.Label(master=input_frame, text='Number of n').grid(row=4, column=0)
n_value = tk.Entry(master=input_frame)
n_value.grid(row=4, column=1)
n_value.insert(index=0, string=str(_n_value))
tk.Label(master=input_frame, text='Delay A').grid(row=5, column=0)
Adelay = tk.Entry(master=input_frame)
Adelay.grid(row=5, column=1)
Adelay.insert(index=0, string=str(_delay[0]))
tk.Label(master=input_frame, text='Delay B').grid(row=6, column=0)
Bdelay = tk.Entry(master=input_frame)
Bdelay.grid(row=6, column=1)
Bdelay.insert(index=0, string=str(_delay[1]))

tk.Label(master=input_frame, text='Description').grid(row=7, column=0)
description_write = tk.Entry(master=input_frame)
description_write.grid(row=7, column=1)

tk.Button(master=experiment_frame, text='Execute', command=handle_execute_click).pack()


# data selection
dataselection_frame = tk.Frame(master=widget_frame, width=wgt_width, borderwidth=5, relief='ridge')
dataselection_frame.pack(fill=tk.BOTH)
tk.Label(master=dataselection_frame, text="[ Data Selection ]").pack()

scroll_frame = tk.Frame(master=dataselection_frame)
scrollbar = tk.Scrollbar(master=scroll_frame)
scrollbar.pack(side=tk.RIGHT, fill="y")
listbox = tk.Listbox(master=scroll_frame, yscrollcommand=scrollbar.set)
for tag in tags['datetime']:
    listbox.insert(tk.END, tag)
listbox.pack(side=tk.TOP, fill=tk.BOTH)
listbox.bind('<<ListboxSelect>>', onSelect)
scrollbar.config(command=listbox.yview)
scroll_frame.pack()

state_field = tk.Frame(master=dataselection_frame, width=wgt_width, height=60)
state_field.pack()
s_count = True
s_efficient = False
s_fitting = True
check_count = tk.Button(master=state_field, text='counts', command=state_count)
check_efficient = tk.Button(master=state_field, text='efficiency', command=state_efficient)
check_fitting = tk.Button(master=state_field, text='fitting', command=state_fitting)
check_count.grid(row=0, column=0)
check_efficient.grid(row=0, column=1)
check_fitting.grid(row=0, column=2)

# information
inform_frame = tk.Frame(master=widget_frame, width=wgt_width, borderwidth=5, relief='ridge')
inform_frame.pack(fill=tk.BOTH)
tk.Label(master=inform_frame, text="[ Inform ]").pack()

display = tk.Label(master=inform_frame, height=1, width=wgt_width, text='')
display.pack(side=tk.TOP, fill=tk.BOTH)

description = tk.Label(master=inform_frame, height=3, width=wgt_width, text='')
description.pack(side=tk.TOP, fill=tk.BOTH)

# delete
tk.Button(master=widget_frame, text='Delete', command=deleteClick).pack(fill=tk.BOTH)

# exit
tk.Button(master=widget_frame, text="EXIT", command=exitClick).pack(side=tk.TOP, fill=tk.BOTH)

# figure
canvas = FigureCanvasTkAgg(figure=fig, master=figure_frame)
canvas.get_tk_widget().pack()

# main function
g_selection = 0
make_figure(get_selection=g_selection)

# maintain window
window.mainloop()
