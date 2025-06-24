import pandas as pd

df = pd.DataFrame(data={
    'H':[40230, 150, 19970, 20533, 21988, 18910],
    'V':[220, 39094, 18542, 20050, 18003, 21054],
    'D':[20556, 19706, 333, 39918, 20475, 19975],
    'A':[20010, 18629, 38011, 440, 18931, 19544],
    'R':[19900, 19649, 17623, 21855, 38717, 401],
    'L':[20761, 19330, 21207, 18804, 483, 39382]
})
df.index = ['H', 'V', 'D', 'A', 'R', 'L']

df.to_csv(path_or_buf='./QST_example_2qubit.csv', sep=',')

S = pd.read_csv(filepath_or_buffer='./QST_example_2qubit.csv', sep=',')

print(S)