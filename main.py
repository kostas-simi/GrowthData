import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelFile
import sys
import numpy as np
import seaborn as sns

filepath = sys.argv[1]
originalSheet = sys.argv[2]

OriginalDf = pd.read_excel(filepath, sheet_name = originalSheet)

df = OriginalDf.sort_values(by=['Tank','Date'])

Rows = df['Tank'].count()
# I mark the days where the fish are weighted
df = df.assign(IsWeighted=0)

for row in range(Rows):
    if (pd.notna(df['Weight sample g'][df.index[row]])):
        df.iloc[row, df.columns.get_loc('IsWeighted')] = 1

# I calculate the sum of the temp detween the weight days
df = df.assign(SumTemp=0)
sum = 0.0
for row in range(1,Rows):
    sum += df['Temp'][df.index[row]]
    if(df['IsWeighted'][df.index[row]] != 0 ):
        df.iloc[row, df.columns.get_loc('SumTemp')] = sum
        sum = 0.0

# keeping the cols I need
df1 = df[['Tank','Weight sample g','Age_days','Temp','SumTemp','Date','Daily feed per fish']]

# Popping the lines with null weights
df1 = df1[df1['Weight sample g'].notnull()]

totalRows = df1['Tank'].count()
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
    df1.iloc[i,df1.columns.get_loc('Days Apart')] = diff

# Setting new column "Weight Difference"
df1['Weight Difference'] = 0.0 * totalRows
# Adding the weight difference between days.
for i in range(1,totalRows):
    if(df1['Days Apart'][df1.index[i]] > 0):
        diff = df1['Weight sample g'][df1.index[i]] - df1['Weight sample g'][df1.index[i-1]]
    else:
        diff = 0.0
    df1.iloc[i,df1.columns.get_loc('Weight Difference')] = diff

# Setting new column 'Daily Growth'
df1['Daily Growth'] = 0.0 * totalRows
# Adding the Average Daily Growth
for i in range(1,totalRows):
    if(df1['Days Apart'][df1.index[i]] > 0):
        growth = (df1['Weight Difference'][df1.index[i]]) / (df1['Days Apart'][df1.index[i]])
    else:
        growth = 0.0
    df1.iloc[i , df1.columns.get_loc('Daily Growth')] = growth

# Setting new column 'Average Temp'
df1['Average Temp'] = 0.0 * totalRows
# Adding Average temp
for i in range(1,totalRows):
    if(df1['Days Apart'][df1.index[i]] > 0):
        avTemp = (df1['SumTemp'][df1.index[i]]) / (df1['Days Apart'][df1.index[i]])
    else:
        avTemp = 0.0
    df1.iloc[i , df1.columns.get_loc('Average Temp')] = avTemp
# Setting new column 'fromDate'
df1['fromDate'] = 0 * totalRows
# Setting new column 'toDate'
df1['toDate'] = df1['Date'].apply(lambda x: x.date().isoformat())
Rows = totalRows


# I seperate each tank so I can study its growth rate
# the tanks will be joined later.
tankNames = df1['Tank'].unique().tolist()
numOfTanks = len(tankNames) - 1

tankDf = []

# I create each tank's dataframe and add it to a list
for i in range(numOfTanks):
    tankDf.append(pd.DataFrame(columns=['Tank','Weight sample g','Age_days','Days Apart','Weight Difference','Daily Growth','Average Temp','fromDate','toDate','Daily feed per fish']))
    wanted = (df1['Tank'] == tankNames[i])
    tankDf[i] = df1[wanted]




# function to sort out bad data-------------
def badData(datafr):
    Rows = datafr['Tank'].count()

    # eliminating the data outliers
    lessThan = (datafr['Daily Growth'] < 5)
    moreThan = (datafr['Daily Growth'] > -5)
    datafr = datafr[lessThan & moreThan ]

    Rows2 = datafr['Tank'].count()

    datafr = datafr.sort_values(by=['Age_days'])

    datafr = datafr.assign(steadyGrowth=0)
    datafr.iloc[0, datafr.columns.get_loc('steadyGrowth')] = 1
# rounding the growth rate to group those with a similar growth rate
    datafr1 = datafr.round({'Daily Growth':1})

    for i in range(Rows2):
        for j in range(i+1,Rows2):
            if (datafr1.iloc[i]['Daily Growth'] == datafr1.iloc[j]['Daily Growth']):
                    datafr.iloc[i, datafr.columns.get_loc('steadyGrowth')] = 1
                    datafr.iloc[j, datafr.columns.get_loc('steadyGrowth')] = 1

    finalDf = datafr.loc[datafr['steadyGrowth'] == 1]
    return finalDf
# end of function-------------

for i in range(numOfTanks):

    tankRows = tankDf[i]['Tank'].count()
    tankDf[i] = tankDf[i].assign(fromWeight=0)
    tankDf[i]['toWeight'] = tankDf[i]['Weight sample g']
    tankDf[i] = tankDf[i].sort_values(by=['toDate'])
    # assigning values to column 'fromDate'
    for j in range(1,tankRows):
        tankDf[i].iloc[j , tankDf[i].columns.get_loc('fromDate')] = tankDf[i].iloc[j-1]['toDate']
        # assigning values to 'fromWeight'
        tankDf[i].iloc[j , tankDf[i].columns.get_loc('fromWeight')] = tankDf[i].iloc[j-1]['toWeight']

FinalDf = pd.DataFrame(columns=['Tank','fromWeight','toWeight','Age_days','Days Apart','Weight Difference','Daily Growth','Average Temp','steadyGrowth','fromDate','toDate','Daily feed per fish'])
# calling the badData function for each of the tank dataframes and joinning them into one.
for i in range(numOfTanks):
    final = badData(tankDf[i])
    FinalDf = FinalDf.append(final,sort=True)

FinalDf = FinalDf.sort_values(by=['Tank','toDate'])
FinalDf = FinalDf[['Tank','fromDate','toDate','Days Apart','Age_days','fromWeight','toWeight','Weight Difference','Daily Growth','Average Temp','Daily feed per fish']]


FinalDf.to_excel('Output_'+filepath, sheet_name = 'output')
print(FinalDf)
# plotting the data and giving a different colour for each tank
sns.lmplot('Age_days', 'Daily Growth', data=FinalDf, hue='Tank', fit_reg=False)

plt.show()
