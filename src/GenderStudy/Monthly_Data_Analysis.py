import pandas
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

dataPath = 'C:\Dev\\'
fileName = 'dorm_data.csv'
df_monthlyData = pandas.read_csv(dataPath + fileName, parse_dates=True, index_col=0 )
january = df_monthlyData.January
february = df_monthlyData.February
march = df_monthlyData.March
april = df_monthlyData.April

fig = plt.figure()

ax1 = fig.add_subplot(2,2,1)
january.plot(kind='bar')

ax2 = fig.add_subplot(2,2,2)
february.plot(kind='bar')

ax3 = fig.add_subplot(2,2,3)
march.plot(kind='bar')

ax4 = fig.add_subplot(2,2,4)
april.plot(kind='bar')

plt.show()