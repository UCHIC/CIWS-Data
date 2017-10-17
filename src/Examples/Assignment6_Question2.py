# ------------------------------------------------------
# Hydroinformatics 2017
# Assignment 6 solution to Question 2
# How does sampling frequency affect the estimate for
# the total volume of water used over a particular time
# period?
# This code does the following:
# 1. Subsets the full resolution data to a known time
#    period
# 2. Subsamples the full resolution to simulate different
#    sampling frequencies
# 3. Calculates a cumulative sum (running total volume)
#    for each sampling frequency
# 4. Plots the data and compares to manual meter readings
# ------------------------------------------------------
import pandas
import matplotlib.pyplot as plt

# Read the CSV file containing the high frequency data
# into a Pandas data frame object
df = pandas.read_csv('datalog_richards_hall.csv', header=1, sep=',',
                     index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# Read the manual meter readings into a Pandas data frame object
df_man = pandas.read_csv('manual_meter_readings_richards_hall.csv', header=0,
                         sep=',', index_col=0, parse_dates=True,
                         infer_datetime_format=True, low_memory=False)

# Subset the continuous data to get the right time period to analyze
# Use copy to make sure we get a new copy of the data and not
# a view of the original data frame
beginDate = '2017-03-03 15:13:00'
endDate = '2017-03-27 16:20:00'
df_1s = df[beginDate:endDate].copy()

# Subsample the full resolution data to a lower resolution
# to simulate a different sampling frequency.
# Create a three new data frames, one with 5 second data,
# one with 10 second data, and one with 30 s data
# Easiest way is to just get every nth observation from the
# original DataFrames
df_5s = df_1s[0::5].copy()
df_10s = df_1s[0::10].copy()
df_30s = df_1s[0::30].copy()

# Estimate the cumulative volume at each time step for each sampling resolution
# Define a new cumulative sum column called "CumVol" in each data frame estimated
# by summing the "FlowRate" column multiplied by the time interval
df_1s['CumVol'] = df_1s.FlowRate.cumsum() * 1.0 / 60.0
df_5s['CumVol'] = df_5s.FlowRate.cumsum() * 5.0 / 60.0
df_10s['CumVol'] = df_10s.FlowRate.cumsum() * 10.0 / 60.0
df_30s['CumVol'] = df_30s.FlowRate.cumsum() * 30.0 / 60.0

print 'Total volume estimated from 1 second flow data = ' + str(df_1s['CumVol'].iloc[-1])
print 'Total volume estimated from 5 second flow data = ' + str(df_5s['CumVol'].iloc[-1])
print 'Total volume estimated from 10 second flow data = ' + str(df_10s['CumVol'].iloc[-1])
print 'Total volume estimated from 30 second flow data = ' + str(df_30s['CumVol'].iloc[-1])
print 'Total volume estimated from manual meter readings = ' + str(df_man['Volume_Used_gal'].iloc[-2])

# Plot the estimated cumulative volume data
# Generate a single plot to which I can add all of the data subsets
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Add each of the cumulative series to the plot
df_1s.plot(y='CumVol', ax=ax, kind='line', use_index=True,
           style='-', ylim=[-0.5, 111000], label='1 s Data')

df_5s.plot(y='CumVol', ax=ax, kind='line', use_index=True,
           style='-', ylim=[-0.5, 111000], label='5 s Data')

df_10s.plot(y='CumVol', ax=ax, kind='line', use_index=True,
            style='-', ylim=[-0.5, 111000], label='10 s Data')

df_30s.plot(y='CumVol', ax=ax, kind='line', use_index=True,
            style='-', ylim=[-0.5, 111000], label='30 s Data')

df_man.plot(y='Volume_Used_gal', ax=ax, kind='line', use_index=True,
            style='o', ylim=[-0.5, 111000], label='Manual Meter Readings')

# Set the x and y-axis labels
ax.set_ylabel('Cumulative Volume (gallons)')
ax.set_xlabel('Date/Time')
ax.grid(True)

# Add a legend with some customizations
legend = ax.legend(loc='upper left', shadow=True)

fig.tight_layout()

# Make sure the plot displays
plt.show()

print 'Done!'


