import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import sys

filepath = sys.argv[1]
originalSheet = sys.argv[2]

OriginalDf = pd.read_excel(filepath, sheet_name = originalSheet)

df = OriginalDf.sort_values(by=['Tank','Date'])

Rows = df['Tank'].count()
# I mark the days where the fish are weighted
df['IsWeighted'] = 0 * Rows

for row in range(Rows):
    if (pd.notna(df['Weight sample g'][df.index[row]])):
        df['IsWeighted'][df.index[row]] = 1
# I calculate the sum of the temp detween the weight days
df['SumTemp'] = 0.0 * Rows
sum = 0.0
for row in range(1,Rows):
    sum += df['Temp'][df.index[row]]
    if(df['IsWeighted'][df.index[row]] != 0 ):
        df['SumTemp'][df.index[row]] = sum
        sum = 0.0


# keeping the cols I need
df1 = df[['Tank','Weight sample g','Age_days','Temp','SumTemp']]

# Popping the null weights
df1 = df1[df1['Weight sample g'].notnull()]



totalRows = df1['Tank'].count()

# print(totalRows)
# Setting new column 'Days Apart'
df1['Days Apart'] = 0 * totalRows
# Sorting the data by tank name and number of days in tank
df1 = df1.sort_values(by=['Tank','Age_days'])
# Adding the gap that separates the days
for i in range(1,totalRows):
    if(df1['Tank'][df1.index[i-1]] == df1['Tank'][df1.index[i]]):
        diff = df1['Age_days'][df1.index[i]] - df1['Age_days'][df1.index[i-1]]
    else:
        diff = 0
    df1['Days Apart'][df1.index[i]] = diff
# Setting new column "Weight Difference"
df1['Weight Difference'] = 0.0 * totalRows
# Adding the weight difference between days.
for i in range(1,totalRows):
    if(df1['Days Apart'][df1.index[i]] > 0):
        diff = df1['Weight sample g'][df1.index[i]] - df1['Weight sample g'][df1.index[i-1]]
    else:
        diff = 0.0
    df1['Weight Difference'][df1.index[i]] = diff
# Setting new column 'Daily Growth'
df1['Daily Growth'] = 0.0 * totalRows
# Adding the Average Daily Growth
for i in range(1,totalRows):
    if(df1['Days Apart'][df1.index[i]] > 0):
        growth = (df1['Weight Difference'][df1.index[i]]) / (df1['Days Apart'][df1.index[i]])
    else:
        growth = 0.0
    df1['Daily Growth'][df1.index[i]] = growth
# Setting new column 'Average Temp'
df1['Average Temp'] = 0.0 * totalRows
# Adding Average temp
for i in range(1,totalRows):
    if(df1['Days Apart'][df1.index[i]] > 0):
        avTemp = (df1['SumTemp'][df1.index[i]]) / (df1['Days Apart'][df1.index[i]])
    else:
        avTemp = 0.0
    df1['Average Temp'][df1.index[i]] = avTemp


FinalDf = df1[['Tank','Weight sample g','Age_days','Days Apart','Weight Difference','Daily Growth','Average Temp']]
# print(FinalDf)


FinalDf.to_excel('output_'+filepath, sheet_name = 'output')
