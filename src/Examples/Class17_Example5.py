# ------------------------------------------------------
# Example of how to read the data file into a Pandas
# data frame, artificially decimate the data to different
# time steps (e.g., 5 and 10 seconds instead of 1 second),
# and then plot with a multi-line plot using matplotlib.
# ------------------------------------------------------
import pandas
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas data frame object
# -------------------------------------------------
# Check your file name to make sure it is the same as mine
# Read the CSV file into a Pandas data frame object
df = pandas.read_csv('datalog_richards_hall.csv', header=1, sep=',',
                     index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# Subset the data frame to get a smaller amount of data to plot
beginDate = '2017-03-03 15:15:00'
endDate = '2017-03-03 16:15:00'
df_1s = df[beginDate:endDate].copy()

# Subsample the full resolution data to a lower resolution
# Create new data frames, one for each simulated sampling frequency
# Easiest way is to just get every nth observation from the original data frame
df_5s = df_1s[0::5].copy()
df_10s = df_1s[0::10].copy()
df_30s = df_1s[0::30].copy()

# Generate a plot of the data subsets
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Add each of the data series to the plot
df_1s.plot(y='FlowRate', ax=ax, kind='line', use_index=True,
           style='-', ylim=[-0.5, 90], marker='o', label='1 s Data')

df_5s.plot(y='FlowRate', ax=ax, kind='line', use_index=True,
           style='-', ylim=[-0.5, 90], marker='^', label='5 s Data')

df_10s.plot(y='FlowRate', ax=ax, kind='line', use_index=True,
            style='-', ylim=[-0.5, 90], marker='*', label='10 s Data')

df_30s.plot(y='FlowRate', ax=ax, kind='line', use_index=True,
            style='-', ylim=[-0.5, 90], marker='s', label='30 s Data')

# Set the x and y-axis labels
ax.set_ylabel('Flow (gpm)')
ax.set_xlabel('Date/Time')
ax.grid(True)

# Add a legend with some customizations
legend = ax.legend(loc='upper right', shadow=True)

plt.title('Comparison of Sampling Intervals')

# Make sure the plot displays
plt.show()

print 'Done!'


