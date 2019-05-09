import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelFile
import sys
import numpy as np


# filepath = sys.argv[1]
# originalSheet = sys.argv[2]

def func(df):
    # filepath = "test.xlsx"
    # df = pd.read_excel(filepath, sheet_name = sheet)
    Rows = df['Tank'].count()
    # print(Rows)

    # eliminating the data outliers
    for i in range(Rows):
        if (df['Daily Growth'][i] > 5 or df['Daily Growth'][i] < -5):
            df = df.drop([i])



    Rows2 = df['Tank'].count()
    # print(Rows2)

    df = df.sort_values(by=['Age_days'])

    df = df.assign(steadyGrowth=0)

    df = df.round({'Daily Growth':1})

    for i in range(Rows2):
        for j in range(i+1,Rows2):
            if (df.iloc[i]['Daily Growth'] == df.iloc[j]['Daily Growth']):
                    df.iloc[i, df.columns.get_loc('steadyGrowth')] = 1
                    df.iloc[j, df.columns.get_loc('steadyGrowth')] = 1

    finalDf = df.loc[df['steadyGrowth'] == 1]
    return finalDf

finalDf = pd.DataFrame(columns=['Tank','Weight sample g','Age_days','Days Apart','Weight Difference','Daily Growth','Average Temp','steadyGrowth'])

file = pd.ExcelFile("test.xlsx")
filepath = 'test.xlsx'
names = file.sheet_names
for i in range(len(names)):
    df = file.parse(names[i])
    final = func(df)
    finalDf = finalDf.append(final,sort=True)

# print(finalDf)
finalDf.to_excel('NoBad_'+filepath, sheet_name = 'output')
