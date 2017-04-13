# ------------------------------------------------------
# Example of how to read the data file into a Pandas
# data frame, artificially decimate the data to different
# time steps (5 and 10 seconds instead of 1 second),and
# then create cumulative data to compare the total volume
# estimated using the different time steps. Finally,
# create a cumulative volume line plot with all 4 lines -
# one for each sampling interval
# ------------------------------------------------------
import pandas
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas data frame object
# -------------------------------------------------
# Check your file name to make sure it is the same as mine
df = pandas.read_csv('datalog_Valley_View_Tower_2017-3-2_16-23-21.csv',
                     header=1, sep=',', index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# Subsample the full resolution data to a lower resolution to simulate
# a different sampling frequency
# --------------------------------------------------------------------
# Create a three new data frames, one with 5 second data, one with 10 second data, and one with 30 s data
# Easiest way is to just get every nth observation from the original data frame
df_5s = df[::5]
df_10s = df[::10]
df_30s = df[::30]

print 'Length of 1 second data is ' + str(len(df))
print 'Length of 5 second data is ' + str(len(df_5s))
print 'Length of 10 second data is ' + str(len(df_10s))
print 'Length of 30 second data is ' + str(len(df_30s))

# Estimate the cumulative volume at each time step for each sampling resolution
# ---------------------------------------------------------------------------------
# Define a new cumulative sum column called "CumVol" in each data frame estimated
# by summing the "FlowRate" column multiplied by the time interval
df['CumVol'] = df.FlowRate.cumsum() * 1.0 / 60.0
df_5s['CumVol'] = df_5s.FlowRate.cumsum() * 5.0 / 60.0
df_10s['CumVol'] = df_10s.FlowRate.cumsum() * 10.0 / 60.0
df_30s['CumVol'] = df_30s.FlowRate.cumsum() * 30.0 / 60.0

print 'Total volume estimated from original datalogger program = ' + str(df['TotalizedVolume'].iloc[-1])
print 'Total volume estimated from 1 second flow data = ' + str(df['CumVol'].iloc[-1])
print 'Total volume estimated from 5 second flow data = ' + str(df_5s['CumVol'].iloc[-1])
print 'Total volume estimated from 10 second flow data = ' + str(df_10s['CumVol'].iloc[-1])
print 'Total volume estimated from 30 second flow data = ' + str(df_30s['CumVol'].iloc[-1])


# Plot the estimated cumulative volume data
# -----------------------------------------
# Generate a single plot to which I can add all of the data subsets
fig, ax = plt.subplots(1, 1)

# Add each of the cumulative series to the plot
df.plot(y='CumVol', ax=ax, kind='line', use_index=True,
        linestyle='solid', ylim=[-0.5, 4000], label='1 s Data')

df_5s.plot(y='CumVol', ax=ax, kind='line', use_index=True,
           linestyle='solid', ylim=[-0.5, 4000], label='5 s Data')

df_10s.plot(y='CumVol', ax=ax, kind='line', use_index=True,
            linestyle='solid', ylim=[-0.5, 4000], label='10 s Data')

df_30s.plot(y='CumVol', ax=ax, kind='line', use_index=True,
            linestyle='solid', ylim=[-0.5, 4000], label='30 s Data')

# Set the x and y-axis labels
ax.set_ylabel('Cumulative Volume (gallons)')
ax.set_xlabel('Date/Time')
ax.grid(True)

# Add a legend with some customizations
legend = ax.legend(loc='upper left', shadow=True)

# Make sure the plot displays
plt.show()
plt.close()

print 'Done!'


