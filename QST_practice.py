import pandas as pd

S = pd.read_csv(filepath_or_buffer='./QST_example_2qubit.csv', sep=',', index_col=0)
info = S.describe()

normalizer = 1/(info.loc['mean']*6).sum()

S = normalizer*S
info = S.describe()
print(info)
