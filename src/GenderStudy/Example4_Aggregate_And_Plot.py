# ------------------------------------------------------
# Example of how to read the data file into a Pandas
# data frame, aggregate the data to a longer time step -
# e.g., aggregate to hourly instead of every second, then
# plot the data using a line plot.
# ------------------------------------------------------
import pandas
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas data frame object
# -------------------------------------------------
# Check your file name to make sure it is the same as mine
df = pandas.read_csv('datalog_Valley_View_Tower_2017-3-7_13-9-5.csv',
                     header=1, sep=',', index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# Aggregate the total flow volume to an hourly time step so I can plot hourly data
# --------------------------------------------------------------------------------
hourlyVol = df.resample(rule='1H', how='sum', base=0)

# Plot the hourly data
hourlyVol.plot(y='IncrementalVolume', kind='line', use_index=True,
               linestyle='solid', ylim=[-0.5, 600], style='o',
               label='Hourly total volume (gal)')

ax = plt.gca()
ax.set_ylabel('Total Volume (gallons)')
ax.set_xlabel('Date/Time')
ax.grid(True)

# Add a legend with some customizations
legend = ax.legend(loc='upper right', shadow=True)

# Make sure the plot displays
plt.show()
plt.close()

print 'Done!'

