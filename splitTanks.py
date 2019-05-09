import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelFile
import sys
import xlsxwriter

filepath = "output_Data.xlsx"
originalSheet = "output"

df = pd.read_excel(filepath, sheet_name = originalSheet)

Rows = df['Tank'].count()

tankNames = []

for i in range(1,Rows):
    tankName0 = df.iloc[i-1]['Tank']
    tankName1 = df.iloc[i]['Tank']
    if not (tankName0 == tankName1):
        tankNames.append(tankName0)

numOfTanks = len(tankNames)
tankDf = []

for i in range(numOfTanks):
    tankDf.append(pd.DataFrame(columns=['Tank','Weight sample g','Age_days','Days Apart','Weight Difference','Daily Growth','Average Temp']))


i = 0
condition = True
while (condition):
    for j in range(1,Rows):
        tankName0 = df.iloc[j-1]['Tank']
        tankName1 = df.iloc[j]['Tank']
        if (tankName0 == tankName1):
            tankDf[i].loc[-1] = df.loc[j-1]
            tankDf[i].index = tankDf[i].index + 1
            tankDf[i] = tankDf[i].sort_index()
        else:
            tankDf[i].loc[-1] = df.loc[j-1]
            tankDf[i].index = tankDf[i].index + 1
            tankDf[i] = tankDf[i].sort_index()
            i += 1
        if (i == numOfTanks):
            condition = False
            break


 # for i in range(numOfTanks):
#     print(tankDf[i])

writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
for i in range(numOfTanks):
    tankDf[i].to_excel(writer, sheet_name = 't'+str(i))

writer.save()
