import pandas as pd

tag = str(int(tags['datetime'].iloc[get_selection]))

measurement = pd.read_csv(filepath_or_buffer="./data/measurement_" + tag + ".csv", sep=',', index_col=0)
coin_effi_line = pd.DataFrame(
    data={'position': measurement['position'],
          'efficient': 100 * measurement['coincidence counts'].div(
              np.sqrt(measurement['A channel counts'].mul(measurement['B channel counts'])))
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
fitting = pd.DataFrame(
    data={'x': fitting_position, 'y': v_line(fitting_position, coeff[0], coeff[1], coeff[2], coeff[3], coeff[4])})

min_idx = fitting['y'].idxmin()

visibility = 1 - (fitting['y'][min_idx]) / (coeff[1] + coeff[0] * fitting['x'][min_idx])

display.config(text="Visibility of this data is %.2f" % (visibility * 100) + "%")

fitting.plot(kind='line', x='x', y='y', ax=ax, color='r', legend=False)

measurement.plot(kind='scatter', x='position', y='coincidence counts', ax=ax, s=5)

ax.axis('on')
ax.set_ylabel("coincidence counts")
ax.set_xlabel("position (mm)")
ax.set_ylim(ymin=0)