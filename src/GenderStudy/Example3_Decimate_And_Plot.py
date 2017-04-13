# ------------------------------------------------------
# Example of how to read the CSV data file into a Pandas
# data frame, artificially decimate the data to different
# time steps (5 and 10 seconds instead of 1 second),and
# then create a subset of the data that can be plotted
# with a multi-line plot using matplotlib.
# Created by:  Jeff Horsburgh
# Last updated: 4-13-2017
# ------------------------------------------------------
import pandas
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas data frame object
# -------------------------------------------------
dataPath = '/users/jeff/Documents/Working/Data/CampusWaterUse/'
df = pandas.read_csv(dataPath + 'datalog_Valley_View_Tower_2017-3-7_13-9-5.csv',
                     header=1, sep=',', index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# Subsample the full resolution data to a lower resolution to simulate
# a different sampling frequency
# --------------------------------------------------------------------
# Create a two new data frames, one with 5 second data and one with 10 second data
# Easiest way is to just get every nth observation from the original data frame
df_5s = df[::5]
df_10s = df[::10]

# Subset the data frames to get a reasonable time period to visualize
beginDate = '2017-03-08 00:00'
endDate = '2017-03-09 00:00'
df_1s_sub = df[beginDate:endDate]
df_5s_sub = df_5s[beginDate:endDate]
df_10s_sub = df_10s[beginDate:endDate]

# Generate a plot of the data subsets
fig, ax = plt.subplots(1, 1)

# Add each of the data series to the plot
df_1s_sub.plot(y='FlowRate', ax=ax, kind='line', use_index=True,
               linestyle='solid', ylim=[-0.5, 90], style='o', label='1 s Data')

df_5s_sub.plot(y='FlowRate', ax=ax, kind='line', use_index=True,
               linestyle='solid', ylim=[-0.5, 90], style='o', label='5 s Data')

df_10s_sub.plot(y='FlowRate', ax=ax, kind='line', use_index=True,
                linestyle='solid', ylim=[-0.5, 90], style='o', label='10 s Data')

# Set the x and y-axis labels
ax.set_ylabel('Flow (gpm)')
ax.set_xlabel('Date/Time')
ax.grid(True)

# Add a legend with some customizations
legend = ax.legend(loc='upper right', shadow=True)

plt.title('Begin date = ' + beginDate + '  End date = ' + endDate)

# Make sure the plot displays
plt.show()
plt.close()

print 'Done!'


