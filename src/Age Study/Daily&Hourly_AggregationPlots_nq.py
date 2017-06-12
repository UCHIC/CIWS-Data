import pandas
import matplotlib.pyplot as plt

# Read the data files for Mountain View and Valley View towers
dataPath = '/Users/nikki/Dev/CIWS-Data/src/Age Study/'
df_SnowHall = pandas.read_csv(dataPath + 'datalog_Snow_Hall_2017-6-6_12-52-2.csv',
                     header=1, sep=',', index_col=0, parse_dates=True,
                    infer_datetime_format=True, low_memory=False)

# Set the begin date and the end date for the analysis
beginDate = '2017-06-06 12:52:2'
endDate = '2017-06-12 7:48:00'

# Input the number of residents for each building
people = 68

# Get a subset of the data between the begin date and end date
df_subSnowHall = df_SnowHall[beginDate:endDate]

# Create a new column within the data frames by summing flow rates and multiplying by time
df_subSnowHall['CumVol'] = df_subSnowHall.FlowRate.cumsum() * 1.0 / 60.0

# Print the total volume per building
print 'The total volume based upon 1 second flow data for Snow Hall is: ' + \
      str(df_subSnowHall['CumVol'].iloc[-1]) + 'gallons'

# Standardize and print total volume of water used in each building per resident
print 'The total volume based upon 1 second flow data flow for Mountain View Tower per resident is: ' + \
      str(df_subSnowHall['CumVol'].iloc[-1]/people) + 'gallons'

# Resample the data subset to hourly by summing the incremental volumes
hourlyTotals = df_subSnowHall['IncrementalVolume'].resample(rule='1H', base=0).sum()

# Resample the data subset to daily by summing the incremental volumes
dailyTotals = df_subSnowHall['IncrementalVolume'].resample(rule='1D', base=0).sum()

# Aggregate the hourly data subset by averaging across hours
hourlyAverages = hourlyTotals.groupby(hourlyTotals.index.hour).mean()

# Normalize the data for each hour per resident
hourlyTotalsPerResidentAverages = hourlyAverages / people

# Normalize the data for each day per resident
dailyTotalsPerResidentAverages = dailyTotals / people

# Generate a plot of the hourly average flow data with one line for men and one for women
fig = plt.figure()
#ax is a subplot inside of plt.figure()
ax = fig.add_subplot(1, 1, 1)
hourlyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                                marker='o', use_index=True, label='SnowHall Average')
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


# Generate a plot of the daily total flow data with one line for men and one for women
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
dailyTotalsPerResidentAverages.plot(y='IncrementalVolume', kind='line', color='purple', linestyle='solid',
                             marker='s', use_index=True, label='Women\'s Total')
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



