# ------------------------------------------------------
# Example of how to read the data file into a Pandas
# DataFrame, aggregate the data to a longer time step -
# e.g., aggregate to hourly instead of every second, then
# plot the data using a line plot.
# ------------------------------------------------------
import pandas
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas data frame object
df = pandas.read_csv('datalog_richards_hall.csv', header=1, sep=',',
                     index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# Aggregate the DataFrame to an hourly time step so
# we can plot hourly data - put the result in a new
# DataFrame
hourlydf = df.resample(rule='1H', base=0).sum()

# Plot the hourly data
hourlydf.plot(y='IncrementalVolume', kind='line', use_index=True,
              style='-', ylim=[-0.5, 600], marker='o',
              label='Hourly total volume (gal)')

# Get the current axis of the plot and
# set the x and y-axis labels
ax = plt.gca()
ax.set_ylabel('Total Volume (gallons)')
ax.set_xlabel('Date/Time')
ax.grid(True)

# Add a legend with some customizations
legend = ax.legend(loc='upper right', shadow=True)

# Make sure the plot displays
plt.show()

print 'Done!'
