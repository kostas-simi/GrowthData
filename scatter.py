import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelFile
import sys

filepath = sys.argv[1]
originalSheet = sys.argv[2]

df = pd.read_excel(filepath, sheet_name = originalSheet)

plt.figure()

ax = plt.gca()

plt.scatter(x=df['Average Temp'],y=df['Daily Growth'])
plt.show()

# plt.scatter(x=df['Age_days'],y=df['Daily Growth'])
# plt.show()
#
# plt.scatter(x=df['Days Apart'],y=df['Weight Difference'])
#
# plt.show()
