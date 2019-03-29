import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelFile
import sys

filepath = sys.argv[1]
originalSheet = sys.argv[2]

df = pd.read_excel(filepath, sheet_name = originalSheet)

Rows = df['Tank'].count()

plt.figure()

ax = plt.gca()


df = df[df['Daily Growth'] > 20 and df['Daily Growth'] < 10]


df.to_excel('NoBad_'+filepath, sheet_name = 'output')
