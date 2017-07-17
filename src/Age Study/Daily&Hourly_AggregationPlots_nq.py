import pandas
import matplotlib.pyplot as plt
import datetime

# Read the data files
dataPath = '/Users/nikki/Dev/CIWS-Data/src/Age Study/'
df_SnowHall = pandas.read_csv(dataPath + 'processed_datalog_Snow_Hall_2017-6-6_12-52-2.csv',
                     header=1, sep=',', index_col=0, parse_dates=True,
                    infer_datetime_format=True, low_memory=False,)

df_SnowHall['FlowRate'] = df_SnowHall['FlowRate'] * 5
df_SnowHall['IncrementalVolume'] = df_SnowHall['IncrementalVolume'] * 5
df_SnowHall['TotalizedVolume'] = df_SnowHall['TotalizedVolume'] * 5

df_SnowHall2 = pandas.read_csv(dataPath + 'datalog_Snow_Hall_2017-6-28_18-27-40.csv',
                     header=1, sep=',', index_col=0, parse_dates=True,
                    infer_datetime_format=True, low_memory=False,)

df_SnowHall3 = pandas.read_csv(dataPath + 'datalog_Snow_Hall_2017-7-11_12-40-23.csv',
                     header=1, sep=',', index_col=0, parse_dates=True,
                    infer_datetime_format=True, low_memory=False,)

df_BlueSquareB = pandas.read_csv(dataPath + 'datalog_Blue_Square_B_2017-6-6_12-52-17.csv',
                                 header=1, sep=',', index_col=0, parse_dates=True,
                                 infer_datetime_format=True, low_memory=False)

df_BlueSquareB2 = pandas.read_csv(dataPath + 'datalog_Blue_Square_B_2017-6-28_18-30-56.csv',
                                 header=1, sep=',', index_col=0, parse_dates=True,
                                 infer_datetime_format=True, low_memory=False)

df_BlueSquareB3 = pandas.read_csv(dataPath + 'datalog_Blue_Square_B_2017-7-5_15-44-43.csv',
                                 header=1, sep=',', index_col=0, parse_dates=True,
                                 infer_datetime_format=True, low_memory=False)

df_BlueSquareB4 = pandas.read_csv(dataPath + 'datalog_Blue_Square_B_2017-7-11_12-38-40.csv',
                                 header=1, sep=',', index_col=0, parse_dates=True,
                                 infer_datetime_format=True, low_memory=False)

df_BlueSquareC = pandas.read_csv(dataPath + 'datalog_Blue_Square_C_2017-6-6_12-55-9.csv',
                                 header=1, sep=',', index_col=0, parse_dates=True,
                                 infer_datetime_format=True, low_memory=False)

df_BlueSquareC2 = pandas.read_csv(dataPath + 'datalog_Blue_Square_C_2017-6-28_18-29-50.csv',
                                 header=1, sep=',', index_col=0, parse_dates=True,
                                 infer_datetime_format=True, low_memory=False)

df_BlueSquareC3 = pandas.read_csv(dataPath + 'datalog_Blue_Square_C_2017-7-11_12-39-40.csv',
                                 header=1, sep=',', index_col=0, parse_dates=True,
                                 infer_datetime_format=True, low_memory=False)

#If data was collected between March 12th 2017 and November 5th 2017 account for daylight savings time
df_SnowHall.index = df_SnowHall.index + datetime.timedelta(hours=1)
df_BlueSquareB.index = df_BlueSquareB.index + datetime.timedelta(hours=1)
df_BlueSquareC.index = df_BlueSquareC.index + datetime.timedelta(hours=1)

#Date Range
beginDate = '2017-06-07 00:00:00'
endDate = '2017-07-17 07:59:59'

#Number of Residents per Building
SnowResidents = 68
BSBresidents = 35
BSCresidents = 37

#Subset each building to the date range
df_subSnow = df_SnowHall[beginDate:endDate]
df_subBSB = df_BlueSquareB[beginDate:endDate]
df_subBSC = df_BlueSquareC[beginDate:endDate]

#add a new colum to the data frame to represent Cumulative Volume by multiplying the FlowRate by time
df_subSnow['CumVol'] = df_SnowHall.FlowRate.cumsum() * 1.0 / 60.0
df_subBSB['CumVol'] = df_BlueSquareB.FlowRate.cumsum() * 1.0 / 60.0
df_subBSC['CumVol'] = df_BlueSquareC.FlowRate.cumsum() * 1.0 / 60.0

# Print the total volume per building
print 'The total volume based upon 1 second flow data for Snow Hall is ' + \
      str(df_subSnow['CumVol'].iloc[-1]) + ' gallons.'
print 'The total volume based upon 1 second flow data for Blue Square B is ' + \
      str(df_subBSB['CumVol'].iloc[-1]) + ' gallons.'
print 'The total volume based upon 1 second flow data for Blue Square C is ' + \
      str(df_subBSC['CumVol'].iloc[-1]) + ' gallons.'

# Standardize and print total volume of water used in each building per resident
print 'The total volume based upon 1 second flow data per resident for Snow Hall is ' + \
          str(df_subSnow['CumVol'].iloc[-1] / SnowResidents) + ' gallons per resident.'
print 'The total volume based upon 1 second flow data per resident for Blue Square B is ' + \
       str(df_subBSB['CumVol'].iloc[-1] / BSBresidents) + ' gallons per resident.'
print 'The total volume based upon 1 second flow data per resident for Blue Square C is ' + \
      str(df_subBSC['CumVol'].iloc[-1] / BSCresidents) + ' gallons per resident.'

# Resample the data subset to hourly by summing the incremental volumes
SnowHourlyTotals = df_subSnow['IncrementalVolume'].resample(rule='1H', base=0).sum()
BSBHourlyTotals = df_subBSB['IncrementalVolume'].resample(rule='1H', base=0).sum()
BSCHourlyTotals = df_subBSC['IncrementalVolume'].resample(rule='1H', base=0).sum()

#Resample the data subset to daily
SnowDailyTotals = df_subSnow['IncrementalVolume'].resample(rule='1D', base=0).sum()
BSBDailyTotals = df_subBSB['IncrementalVolume'].resample(rule='1D', base=0).sum()
BSCDailyTotals = df_subBSC['IncrementalVolume'].resample(rule='1D', base=0).sum()

# Aggregate the hourly data subset by averaging across hours
SnowHourlyAverages = SnowHourlyTotals.groupby(SnowHourlyTotals.index.hour).mean()
BSBHourlyAverages = BSBHourlyTotals.groupby(BSBHourlyTotals.index.hour).mean()
BSCHourlyAverages = BSCHourlyTotals.groupby(BSCHourlyTotals.index.hour).mean()

# Normalize the Hourly data per resident
SnowHourlyTotalsPerResidentAverages = SnowHourlyAverages / SnowResidents
BSBHourlyTotalsPerResidentAverages = BSBHourlyAverages / BSBresidents
BSCHourlyTotalsPerResidentAverages = BSCHourlyAverages / BSCresidents

# Normalize the Daily data per resident
SnowDailyTotalsPerResidentAverages = SnowDailyTotals / SnowResidents
BSBDailyTotalsPerResidentAverages = BSBDailyTotals / BSBresidents
BSCDailyTotalsPerResidentAverages = BSCDailyTotals / BSCresidents

fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
SnowHourlyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                                             marker='o', use_index=True, label= 'Snow Hall Hourly Averages')
ax1.set_ylabel('Volume (gal)')
ax1.set_xlabel('Hour of Day')
ax1.grid(True)
ax1.set_title('Hourly Average Volume Per Resident')
legend = ax1.legend(loc='best', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.95')
fig.set_tight_layout(True)

ax2 = fig.add_subplot(2, 2, 2)
BSBHourlyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='red', linestyle='solid',
                                             marker='o', use_index=True, label= 'Blue Square B Hourly Averages')
ax2.set_ylabel('Volume (gal)')
ax2.set_xlabel('Hour of Day')
ax2.grid(True)
ax2.set_title('Hourly Average Volume Per Resident')
legend = ax2.legend(loc='best', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.95')
fig.set_tight_layout(True)

ax3 = fig.add_subplot(2, 2, 3)
BSCHourlyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='green', linestyle='solid',
                                             marker='o', use_index=True, label= 'Blue Square C Hourly Averages')
ax3.set_ylabel('Volume (gal)')
ax3.set_xlabel('Hour of Day')
ax3.grid(True)
ax3.set_title('Hourly Average Volume Per Resident')
legend = ax3.legend(loc='best', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.95')
fig.set_tight_layout(True)

ax4 = fig.add_subplot(2, 2, 4)
SnowHourlyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                                             marker='o', use_index=True, label= 'Snow Hall Hourly Averages')
BSCHourlyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='green', linestyle='solid',
                                             marker='o', use_index=True, label= 'Blue Square C Hourly Averages')
BSBHourlyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='red', linestyle='solid',
                                             marker='o', use_index=True, label= 'Blue Square B Hourly Averages')
ax4.set_ylabel('Volume (gal)')
ax4.set_xlabel('Hour of Day')
ax4.grid(True)
ax4.set_title('Hourly Average Volume Per Resident')
legend = ax4.legend(loc='best', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.95')
fig.set_tight_layout(True)

plt.show()

fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
SnowDailyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                                             marker='o', use_index=True, label= 'Snow Hall Daily Averages')
ax1.set_ylabel('Volume (gal)')
ax1.set_xlabel('Day')
ax1.grid(True)
ax1.set_title('Daily Average Volume Per Resident')
legend = ax1.legend(loc='best', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.95')
fig.set_tight_layout(True)

ax2 = fig.add_subplot(2, 2, 2)
BSBDailyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='red', linestyle='solid',
                                             marker='o', use_index=True, label= 'Blue Square B Daily Averages')
ax2.set_ylabel('Volume (gal)')
ax2.set_xlabel('Day')
ax2.grid(True)
ax2.set_title('Daily Average Volume Per Resident')
legend = ax2.legend(loc='best', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.95')
fig.set_tight_layout(True)

ax3 = fig.add_subplot(2, 2, 3)
BSCDailyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='green', linestyle='solid',
                                             marker='o', use_index=True, label= 'Blue Square C Daily Averages')
ax3.set_ylabel('Volume (gal)')
ax3.set_xlabel('Day')
ax3.grid(True)
ax3.set_title('Daily Average Volume Per Resident')
legend = ax3.legend(loc='best', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.95')
fig.set_tight_layout(True)

ax4 = fig.add_subplot(2, 2, 4)
SnowDailyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                                             marker='o', use_index=True, label= 'Snow Hall Daily Averages')
BSBDailyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='red', linestyle='solid',
                                             marker='o', use_index=True, label= 'Blue Square B Daily Averages')
BSCDailyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='green', linestyle='solid',
                                             marker='o', use_index=True, label= 'Blue Square C Daily Averages')
ax4.set_ylabel('Volume (gal)')
ax4.set_xlabel('Day')
ax4.grid(True)
ax4.set_title('Daily Average Volume Per Resident')
legend = ax4.legend(loc='best', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.95')
fig.set_tight_layout(True)

plt.show()
