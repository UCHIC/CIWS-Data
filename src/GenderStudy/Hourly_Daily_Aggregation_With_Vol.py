import pandas
import numpy as np
import matplotlib.pyplot as plt

dataPath = 'C:\Dev\\'

# Read the data files for Mountain View and Valley View towers
df_mountainView = pandas.read_csv(dataPath + 'datalog_Mountain_View_Tower_2017-3-3_15-33-30.csv',
                                  header=1, sep=',', index_col=0, parse_dates=True,
                                  infer_datetime_format=True, low_memory=False)

df_valleyView = pandas.read_csv(dataPath + 'datalog_Valley_View_Tower_2017-3-7_13-9-5.csv',
                                header=1, sep=',', index_col=0, parse_dates=True,
                                infer_datetime_format=True, low_memory=False)

# Set the begin date and the end date for the analysis
beginDate = '2017-03-13 00:00:00'
endDate = '2017-03-26 23:59:59'

# Input the number of residents for each building
mountainViewResidents = 312
valleyViewResidents = 242

# Get a subset of the data between the begin date and end date
df_subMountainView = df_mountainView[beginDate:endDate]
df_subValleyView = df_valleyView[beginDate:endDate]

# Create a new column within the data frames by summing flow rates and multiplying by time
df_subMountainView['CumVol'] = df_subMountainView.FlowRate.cumsum() * 1.0 / 60.0
df_subValleyView['CumVol'] = df_subValleyView.FlowRate.cumsum() * 1.0 / 60.0

mountainViewVolume = df_subMountainView['CumVol'].iloc[-1]
valleyViewVolume = df_subValleyView['CumVol'].iloc[-1]

# Print the total volume per building
print 'The total volume based upon 1 second flow data for Mountain View Tower is: ' + \
       str(mountainViewVolume) + 'gallons'
print 'The total volume based upon 1 second flow data for Valley View Tower is: ' + \
       str(valleyViewVolume) + 'gallons'

# Standardize and print total volume of water used in each building per resident
print 'The total volume based upon 1 second flow data flow for Mountain View Tower per resident is: ' + \
       str(mountainViewVolume / mountainViewResidents) + 'gallons'
print 'The total volume based upon 1 second flow data flow for Mountain View Tower per resident is: ' + \
       str(valleyViewVolume / valleyViewResidents) + 'gallons'

# Determine and print the percentage of total usage by each building
print 'The percentage of water used by Mountain View Tower during the two week period is: ' + \
       str(mountainViewVolume / (mountainViewVolume + valleyViewVolume) * 100) + '%'
print 'The percentage of water used by Valley View Tower during the two week period is: ' + \
       str(valleyViewVolume / (mountainViewVolume + valleyViewVolume) * 100) + '%'


# Resample the data subset to hourly by summing the incremental volumes
hourlyTotVolMountain = df_subMountainView['IncrementalVolume'].resample(rule='1H', base=0).sum()
hourlyTotVolValley = df_subValleyView['IncrementalVolume'].resample(rule='1H', base=0).sum()

#Aggregate the hourly data subset by averaging across hours
hourlyAvgVolMountain = hourlyTotVolMountain.groupby(hourlyTotVolMountain.index.hour).mean()
hourlyAvgVolValley = hourlyTotVolValley.groupby(hourlyTotVolValley.index.hour).mean()

# Normalize the data for each hour per resident
hourlyAvgVolMountainPerRes = hourlyAvgVolMountain / mountainViewResidents
hourlyAvgVolValleyPerRes = hourlyAvgVolValley / valleyViewResidents

#Create a dataframe that outputs the hourly usages per resident
displayOfHourlyVolumes = pandas.concat([hourlyAvgVolMountainPerRes, hourlyAvgVolValleyPerRes], axis=1,)

#Set column labels in what I consider to be a slightly sketchy manner
print "     Mountain Volume     Valley Volume "

#Print the dataframe
print displayOfHourlyVolumes

# Generate a plot of the hourly average flow data with one line for men and one for women
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
hourlyAvgVolMountainPerRes.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                                marker='o', use_index=True, label='Men\'s Average')
hourlyAvgVolValleyPerRes.plot(y='IncrementalVolume', kind='line', color='purple', linestyle='solid',
                              marker='s', use_index=True, label='Women\'s Average')
ax.set_ylabel('Volume (gal)')
ax.set_xlabel('Hour of Day')
ax.grid(True)
ax.set_title('Hourly Average Flow Volume Per Resident')

# Add a legend with some customizations
legend = ax.legend(loc='upper left', shadow=True)

# Create a frame around the legend.
frame = legend.get_frame()
frame.set_facecolor('0.95')

# Make sure the plot displays
fig.set_tight_layout(True)
plt.show()

#Create a new column within the hourly aggregated data that contains the total volume up to that hour
hourlyAvgVolMountainPerRes = hourlyAvgVolMountainPerRes.cumsum()
hourlyAvgVolValleyPerRes = hourlyAvgVolValleyPerRes.cumsum()

#Generate a plot that shows the aggregated hourly volumes summed up over the 24 hour time period
cumHourlyVolumeMountain = hourlyAvgVolMountainPerRes.cumsum()
cumHourlyVolumeValley = hourlyAvgVolValleyPerRes.cumsum()
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

cumHourlyVolumeMountain.plot(kind='line', title='Cumulative Volume Over 24 Hours',
                             legend='True', linestyle='solid', ylim=[-0.5, 200], label='Men\'s Sum',
                             color='blue')
cumHourlyVolumeValley.plot(kind='line', title='Cumulative Volume Over 24 Hours',
                           legend='True', linestyle='solid', ylim=[-0.5, 200], label='Women\'s Sum',
                           color='purple')

# Set the x and y-axis labels
ax.set_xlabel('Time')
ax.set_ylabel('Cumulative Volume')
ax.grid(True)

#Make sure the plot displays
plt.show()
plt.close()
print 'Done!'



"""

# Resample the data subset to daily by summing the incremental volumes
dailyTotVolMountain = df_subMountainView['IncrementalVolume'].resample(rule='1D', base=0).sum()
dailyTotVolValley = df_subValleyView['IncrementalVolume'].resample(rule='1D', base=0).sum()

#Normalize the data for each day per resident
dailyTotVolMountainPerRes = dailyTotVolMountain / mountainViewResidents
dailyTotVolValleyPerRes = dailyTotVolValley / valleyViewResidents

# Generate a plot of the daily total flow data with one line for men and one for women
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
dailyTotVolMountainPerRes.plot(y='IncrementalVolume', kind='line', color='blue', linestyle='solid',
                               marker='o', use_index=True, label='Men\'s Total')
dailyTotVolValleyPerRes.plot(y='IncrementalVolume', kind='line', color='purple', linestyle='solid',
                             marker='s', use_index=True, label='Women\'s Total')
ax.set_ylabel('Volume (gal)')
ax.set_xlabel('Day')
ax.grid(True)
ax.set_title('Daily Total Flow Volume Per Resident')

# Add a legend with some customizations
legend = ax.legend(loc='upper left', shadow=True)

# Create a frame around the legend.
frame = legend.get_frame()
frame.set_facecolor('0.95')

# Make sure the plot displays
fig.set_tight_layout(True)
plt.show()"""







