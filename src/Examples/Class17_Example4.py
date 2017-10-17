# ------------------------------------------------------
# Example of how to read the data file into a Pandas
# DataFrame, aggregate the data to a longer time step,
# use groupby to aggregate across days, and then
# plot the data.
# ------------------------------------------------------
import pandas
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas data frame object
df = pandas.read_csv('datalog_richards_hall.csv', header=1, sep=',',
                     index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# First aggregate the incremental flow volume to a
# total volume for each hourly time step
hourlyTotVol = df['IncrementalVolume'].resample(rule='1H', base=0).sum()

# Calculate an average volume for each hour
# of the day by aggregating across days using
# the groupby function
hourlyAvgVol = hourlyTotVol.groupby(hourlyTotVol.index.hour).mean()
# Also calculate the standard deviation for each hour
hourlyStDevVol = hourlyTotVol.groupby(hourlyTotVol.index.hour).std()

# Generate a plot of the data with some indication of the variability in
# the hourly average values (e.g., add error bars with +- one Std. Dev.)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

plt.errorbar(x=hourlyAvgVol.index, y=hourlyAvgVol,
             yerr=hourlyStDevVol, capsize=3,
             capthick=0.5, fmt='--',
             label='Average Hourly Volumes', marker='o')

# Set the limits on the x-axis and the tick
# mark locations
ax.set_xlim(-0.5, 23.5)
xmarks = range(0, 23 + 1, 1)
plt.xticks(xmarks)

# Set the x and y-axis labels and title
ax.set_ylabel('Average Hourly Volume (gal)')
ax.set_xlabel('Hour of the Day')
ax.grid(False)
plt.title('Average Hourly Volume Estimates')

# Make sure the plot displays
plt.show()

print 'Done!'

