import pandas
import matplotlib.pyplot as plt

# Read the data files for Mountain View and Valley View towers
df_mountainView = pandas.read_csv('datalog_Mountain_View_Tower_2017-3-3_15-33-30.csv',
                                  header=1, sep=',', index_col=0, parse_dates=True,
                                  infer_datetime_format=True, low_memory=False)

df_valleyView = pandas.read_csv('datalog_Valley_View_Tower_2017-3-7_13-9-5.csv',
                                header=1, sep=',', index_col=0, parse_dates=True,
                                infer_datetime_format=True, low_memory=False)

# Set the begin date and the end date for the analysis
beginDate = '2017-03-13 00:00:00'
endDate = '2017-03-26 23:59:59'

# Get a subset of the data between the begin date and end date
df_subMountainView = df_mountainView[beginDate:endDate]
df_subValleyView = df_valleyView[beginDate:endDate]

# Resample the data subset to hourly by summing the incremental volumes
hourlyTotVolMountain = df_subMountainView['IncrementalVolume'].resample(rule='1H', base=0).sum()
hourlyTotVolValley = df_subValleyView['IncrementalVolume'].resample(rule='1H', base=0).sum()

# Resample the data subset to daily by summing the incremental volumes
dailyTotVolMountain = df_subMountainView['IncrementalVolume'].resample(rule='1D', base=0).sum()
dailyTotVolValley = df_subValleyView['IncrementalVolume'].resample(rule='1D', base=0).sum()

# Aggregate the hourly data subset by averaging across hours
hourlyAvgVolMountain = hourlyTotVolMountain.groupby(hourlyTotVolMountain.index.hour).mean()
hourlyAvgVolValley = hourlyTotVolValley.groupby(hourlyTotVolValley.index.hour).mean()

# Generate a plot of the hourly average flow data with one line for men and one for women
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
hourlyAvgVolMountain.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                          marker='o', use_index=True, label='Men\'s Average')
hourlyAvgVolValley.plot(y='IncrementalVolume', kind='line', color='purple', linestyle='solid',
                        marker='s', use_index=True, label='Women\'s Average')
ax.set_ylabel('Volume (gal)')
ax.set_xlabel('Hour of Day')
ax.grid(True)
ax.set_title('Hourly Average Flow Volume')

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
dailyTotVolMountain.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                         marker='o', use_index=True, label='Men\'s Total')
dailyTotVolValley.plot(y='IncrementalVolume', kind='line', color='purple', linestyle='solid',
                       marker='s', use_index=True, label='Women\'s Total')
ax.set_ylabel('Volume (gal)')
ax.set_xlabel('Day')
ax.grid(True)
ax.set_title('Daily Total Flow Volume')

# Add a legend with some customizations
legend = ax.legend(loc='upper left', shadow=True)

# Create a frame around the legend.
frame = legend.get_frame()
frame.set_facecolor('0.95')

# Make sure the plot displays
fig.set_tight_layout(True)
plt.show()

print 'Done!'

