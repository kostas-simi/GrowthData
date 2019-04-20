import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelFile
import sys

filepath = sys.argv[1]
originalSheet = sys.argv[2]

df = pd.read_excel(filepath, sheet_name = originalSheet)
Rows = df['Tank'].count()
print(Rows)


for i in range(Rows):
    if (df['Daily Growth'][i] > 5 or df['Daily Growth'][i] < -5):
        df = df.drop([i])


Rows2 = df['Tank'].count()
print(Rows2)

# --- might work ---

# df2 = pd.DataFrame(index=Rows2)
# for i in range(1,Rows2):
#     if (df['Tank'][i] == df['Tank'][i-1] and df['Daily Growth'][i] == df['Daily Growth'][i-1]):
#         df2[i] = df[i]


df.to_excel('NoBad_'+filepath, sheet_name = 'output')
