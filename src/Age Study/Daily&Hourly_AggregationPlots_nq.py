import pandas
import matplotlib.pyplot as plt

# Read the data files for Mountain View and Valley View towers
dataPath = '/Users/nikki/Dev/CIWS-Data/src/Age Study/'
df_SnowHall = pandas.read_csv(dataPath + 'datalog_Snow_Hall_2017-6-6_12-52-2.csv',
                     header=1, sep=',', index_col=0, parse_dates=True,
                    infer_datetime_format=True, low_memory=False)
def hourly(df, residenceHall, residents, BeginDate, EndDate):
    beginDate = BeginDate
    endDate = EndDate
    # Number of residents per building
    people = residents
    # Get a subset of the data between the begin date and end date
    df_sub = df[beginDate:endDate]
    # Create a new column within the data frames by summing flow rates and multiplying by time
    df_sub['CumVol'] = df.FlowRate.cumsum() * 1.0 / 60.0
    # Print the total volume per building
    print 'The total volume based upon 1 second flow data for ' + str(residenceHall) + ' is: ' + \
      str(df_sub['CumVol'].iloc[-1]) + ' gallons'
    # Standardize and print total volume of water used in each building per resident
    print 'The total volume based upon 1 second flow data  for ' + residenceHall + ' is: ' + \
          str(df_sub['CumVol'].iloc[-1] / people) + ' gallons per resident'
    # Resample the data subset to hourly by summing the incremental volumes
    hourlyTotals = df_sub['IncrementalVolume'].resample(rule='1H', base=0).sum()
    # Aggregate the hourly data subset by averaging across hours
    hourlyAverages = hourlyTotals.groupby(hourlyTotals.index.hour).mean()
    # Normalize the data for each hour per resident
    hourlyTotalsPerResidentAverages = hourlyAverages / people
    # Generate a plot of the hourly average flow data with one line for men and one for women
    fig = plt.figure()
    # ax is a subplot inside of plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    hourlyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                                         marker='o', use_index=True, label= residenceHall + 'Average')
    ax.set_ylabel('Volume (gal)')
    ax.set_xlabel('Hour of Day')
    ax.grid(True)
    ax.set_title('Hourly Average Volume Per Resident')
    # Add a legend with some customizations
    legend = ax.legend(loc='upper left', shadow=True)
    # Create a frame around the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.95')
    # Make sure the plot displays
    fig.set_tight_layout(True)
    plt.show()

    return;

def daily(df, residenceHall, residents, BeginDate, EndDate):
    beginDate = BeginDate
    endDate = EndDate
    # Number of residents per building
    people = residents
    # Get a subset of the data between the begin date and end date
    df_sub = df[beginDate:endDate]
    # Create a new column within the data frames by summing flow rates and multiplying by time
    df_sub['CumVol'] = df.FlowRate.cumsum() * 1.0 / 60.0
    # Resample the data subset to daily by summing the incremental volumes
    dailyTotals = df_sub['IncrementalVolume'].resample(rule='1D', base=0).sum()
    # Normalize the data for each day per resident
    dailyTotalsPerResidentAverages = dailyTotals / people
    # Generate a plot of the daily total flow data with one line for men and one for women
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    dailyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='purple', linestyle='solid',
                                        marker='s', use_index=True, label=residenceHall + ' Total')
    ax.set_ylabel('Volume (gal)')
    ax.set_xlabel('Day')
    ax.grid(True)
    ax.set_title('Daily Total Volume Per Resident')
    # Add a legend with some customizations
    legend = ax.legend(loc='upper left', shadow=True)
    # Create a frame around the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.95')
    # Make sure the plot displays
    fig.set_tight_layout(True)
    plt.show()
    return;

hourly(df_SnowHall, 'SnowHall', 68, '2017-06-07 0:00:00', '2017-06-12 7:48:00')
daily(df_SnowHall, 'SnowHall', 68, '2017-06-07 0:00:00', '2017-06-12 7:48:00')
