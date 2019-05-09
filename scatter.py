import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelFile
import sys
import numpy as np
import seaborn as sns

filepath = sys.argv[1]
originalSheet = 'output'


df = pd.read_excel(filepath, sheet_name = originalSheet)

# groups = df.groupby('Tank')
#
# plt.figure()
#
# ax = plt.gca()
#
#
# plt.scatter(x=df['Age_days'],y=df['Daily Growth'], c = groups)
# plt.show()




sns.lmplot('Age_days', 'Daily Growth', data=df, hue='Tank', fit_reg=False)

plt.show()
