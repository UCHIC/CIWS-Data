import pandas
import matplotlib.pyplot as plt
import datetime

# Read the data files
dataPath = '/Users/nikki/Dev/CIWS-Data/src/Age Study/'
df_SnowHall = pandas.read_csv(dataPath + 'datalog_Snow_Hall_2017-6-6_12-52-2.csv',
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
def printVolume(df, residents, buildingName):
    df['CumVol'] = df.FlowRate.cumsum() * 1.0 / 60.0
    print 'The total volume based upon 1 second flow data for ' + buildingName + ' is ' + \
          str(df['CumVol'].iloc[-1]) + ' gallons.'
    print 'The total volume based upon 1 second flow data per resident for Snow ' + buildingName + ' is ' + \
          str(df['CumVol'].iloc[-1] / residents) + ' gallons per resident.'
    return;

def plotHourlyAndDailyForOne(df, residents, buildingName):
    HourlyTotals = df['IncrementalVolume'].resample(rule='1H', base=0).sum()
    HourlyAverages = HourlyTotals.groupby(HourlyTotals.index.hour).mean()
    HourlyTotalsPerResidentAverages = HourlyAverages / residents
    DailyTotals = df['IncrementalVolume'].resample(rule='1D', base=0).sum()
    DailyTotalsPerResidentAverages = DailyTotals / residents
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    HourlyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                                             marker='o', use_index=True, label=' ' + buildingName +' Hourly Averages')
    ax1.set_ylabel('Volume (gal)')
    ax1.set_xlabel('Hour of Day')
    ax1.grid(True)
    ax1.set_title('Hourly Average Volume Per Resident')
    legend = ax1.legend(loc='best', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.95')
    fig.set_tight_layout(True)

    ax2 = fig.add_subplot(2, 1, 2)
    DailyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='green', linestyle='solid',
                                            marker='o', use_index=True, label='Snow Hall Daily Averages')
    ax2.set_ylabel('Volume (gal)')
    ax2.set_xlabel('Day')
    ax2.grid(True)
    ax2.set_title('Daily Average Volume Per Resident')
    legend = ax2.legend(loc='best', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.95')
    fig.set_tight_layout(True)
    plt.show()
    return;

def HourlyAndDailyForThree(df1,residents1, name1, df2, residents2, name2, df3, residents3, name3):
    HourlyTotals1 = df1['IncrementalVolume'].resample(rule='1H', base=0).sum()
    HourlyAverages1 = HourlyTotals1.groupby(HourlyTotals1.index.hour).mean()
    HourlyTotalsPerResidentAverages1 = HourlyAverages1 / residents1
    DailyTotals1 = df1['IncrementalVolume'].resample(rule='1D', base=0).sum()
    DailyTotalsPerResidentAverages1 = DailyTotals1 / residents1
    HourlyTotals2 = df2['IncrementalVolume'].resample(rule='1H', base=0).sum()
    HourlyAverages2 = HourlyTotals2.groupby(HourlyTotals2.index.hour).mean()
    HourlyTotalsPerResidentAverages2 = HourlyAverages2 / residents2
    DailyTotals2 = df2['IncrementalVolume'].resample(rule='1D', base=0).sum()
    DailyTotalsPerResidentAverages2 = DailyTotals2 / residents2
    HourlyTotals3 = df3['IncrementalVolume'].resample(rule='1H', base=0).sum()
    HourlyAverages3 = HourlyTotals3.groupby(HourlyTotals3.index.hour).mean()
    HourlyTotalsPerResidentAverages3 = HourlyAverages3 / residents3
    DailyTotals3 = df3['IncrementalVolume'].resample(rule='1D', base=0).sum()
    DailyTotalsPerResidentAverages3 = DailyTotals3 / residents3
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    HourlyTotalsPerResidentAverages1.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                                             marker='o', use_index=True, label=name1 +' Hourly Averages')
    HourlyTotalsPerResidentAverages2.plot(y='IncrementalVolume', kind='line', color='green', linestyle='solid',
                                            marker='o', use_index=True, label=name2 +' Hourly Averages')
    HourlyTotalsPerResidentAverages3.plot(y='IncrementalVolume', kind='line', color='red', linestyle='solid',
                                            marker='o', use_index=True, label=name3 +' Hourly Averages')
    ax1.set_ylabel('Volume (gal)')
    ax1.set_xlabel('Hour of Day')
    ax1.grid(True)
    ax1.set_title('Hourly Average Volume Per Resident')
    legend = ax1.legend(loc='best', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.95')
    fig.set_tight_layout(True)

    plt.show()

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    DailyTotalsPerResidentAverages1.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                                            marker='o', use_index=True, label=name1 +' Daily Averages')
    DailyTotalsPerResidentAverages2.plot(y='IncrementalVolume', kind='line', color='green', linestyle='solid',
                                           marker='o', use_index=True, label=name2 +' Daily Averages')
    DailyTotalsPerResidentAverages3.plot(y='IncrementalVolume', kind='line', color='red', linestyle='solid',
                                           marker='o', use_index=True, label=name3 +' Daily Averages')
    ax1.set_ylabel('Volume (gal)')
    ax1.set_xlabel('Day')
    ax1.grid(True)
    ax1.set_title('Daily Average Volume Per Resident')
    legend = ax1.legend(loc='best', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.95')
    fig.set_tight_layout(True)

    plt.show()
    return;


printVolume(df_SnowHall, 68, 'Snow Hall')
plotHourlyAndDailyForOne(df_SnowHall, 68, 'Snow Hall')
HourlyAndDailyForThree(df_SnowHall, 68, 'Snow Hall', df_BlueSquareB, 35, 'Blue Square B', df_BlueSquareC, 37, 'Blue Square C')
HourlyAndDailyForThree(df_SnowHall, 68, 'Snow Hall 6/6', df_SnowHall2, 68, 'Snow Hall 6/28', df_SnowHall3, 68, 'Snow Hall 7/11')
HourlyAndDailyForThree(df_BlueSquareB, 35, 'Blue Square B 6/6', df_BlueSquareB3, 35, 'Blue Square B 7/5', df_BlueSquareB4, 35, 'Blue Square B 7/11')
HourlyAndDailyForThree(df_BlueSquareC, 37, 'Blue Square C 6/6', df_BlueSquareC2, 37, 'Blue Square C 6/28', df_BlueSquareC3, 37, 'Blue Square C 7/11')
