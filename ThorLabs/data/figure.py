import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('TkAgg')

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


def onSelect(event):
    _selection = listbox.curselection()
    if _selection:
        global g_selection
        index = _selection[0]
        g_selection = str(listbox.get(index))
        description.config(text=
                           f""
                           f"< description >------------------------\n"
                           f"|                                                  |\n"
                           f"|                     {str(tags.loc[index]["description"])}                     |\n"
                           f"|                                                  |\n"
                           f"-----------------------------------------")
        make_figure(get_selection=g_selection)


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


def state_position():
    global s_position, g_selection
    s_position = not s_position
    make_figure(get_selection=g_selection)


# Main figure function
def make_figure(get_selection):
    global canvas
    global fig, ax, t_efficient, t_position
    global s_count, s_efficient, s_position

    ax.cla()
    ax.axis('off')
    t_efficient.cla()
    t_efficient.axis('off')
    t_position.cla()
    t_position.axis('off')

    tag = get_selection

    measurement = pd.read_csv(filepath_or_buffer="./measurement_"+tag+".csv", sep=',', index_col=0)
    position_log = pd.read_csv(filepath_or_buffer="./position_log_"+tag+".csv", sep=',', index_col=0)
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
                                                            measurement['position'].shape[0] / 5)]], 0), 5)

    )

    p0 = [0, measurement['coincidence counts'].mean(), 1, 0, measurement['coincidence counts'].min()]
    coeff, var_matrix = curve_fit(f=v_line, xdata=measurement['position'], ydata=measurement['coincidence counts'], p0=p0)

    fitting_position = [
        measurement['position'][0],
        (coeff[4] - coeff[1] - abs(coeff[3]))/(coeff[0] + abs(coeff[2])),
        -abs(coeff[3])/abs(coeff[2]),
        (coeff[4] - coeff[1] + abs(coeff[3])) / (coeff[0] - abs(coeff[2])),
        measurement['position'].iloc[-1]
    ]
    fitting = pd.DataFrame(data={'x':fitting_position, 'y':v_line(fitting_position, coeff[0], coeff[1], coeff[2], coeff[3], coeff[4])})

    min_idx = measurement['coincidence counts'].idxmin()

    visibility = 1 - (measurement['coincidence counts'][min_idx]/(measurement['position'][min_idx]*coeff[0] + coeff[1]))
    acc = measurement['A channel counts'][min_idx]*measurement['B channel counts'][min_idx]*10*1e-12

    fit_visibility = 1 - (fitting['y'][2]-acc)/(coeff[1] + coeff[0]*fitting_position[2]-acc)

    display.config(text="Visibility of this data is %.2f"%(fit_visibility*100)+"%")

    if s_count:
        measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax, s=5)
        fitting.plot(kind='line', x='x', y='y', ax=ax, color='r', legend=False)
        ax.axis('on')
        ax.set_ylabel("coincidence counts")
        ax.set_xlabel("position (mm)")
        ax.set_ylim(ymin=0)

    if s_efficient:
        coin_effi_line.plot(kind='scatter', x='position', y='efficient', ax=t_efficient)
        t_efficient.axis('on')
        t_efficient.set_xlim(xmin=measurement['position'].min(), xmax=measurement['position'].max())

    if s_position:
        position_log.reset_index().plot(kind='scatter', x='index', y='position', ax=t_position, s=0.1)
        t_position.axis('on')
        t_position.spines.right.set_position(("axes", 1.1))
        t_position.set_ylabel('position')

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

description = tk.Label(master=widget_frame, height=5, width=wgt_width, text='')
description.pack(side=tk.TOP, fill=tk.BOTH)

exit_button = tk.Button(master=widget_frame, text="EXIT", command=exitClick)
exit_button.pack(side=tk.TOP, fill=tk.BOTH)

canvas = FigureCanvasTkAgg(figure=fig, master=figure_frame)

g_selection = str(int(tags.loc[0]['datetime']))
make_figure(get_selection=g_selection)

window.mainloop()
