# ------------------------------------------------------
# Hydroinformatics 2017
# Assignment 6 solution to Question 1
# How are weekend (Saturday and Sunday) water demands
# different than weekday (Monday – Friday) demands?
# This code does the following:
# 1. Resamples the data to hourly by summing incremental
#    volumes
# 2. Bins the hourly data into weekday versus weekend data
# 3. Aggregates the data to average hourly and Std. Dev.
#    by using the groupby function
# 4. Plots the aggregated weekday versus weekend data for
#    comparison
# ------------------------------------------------------
import pandas
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas data frame object
df = pandas.read_csv('datalog_richards_hall.csv', header=1, sep=',',
                     index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# First aggregate the incremental flow volume to a
# total volume for each hourly time step for the whole period
hourlyTotVol = df['IncrementalVolume'].resample(rule='1H', base=0).sum()

# Now subset the hourly data by days of the week
# Create a new DataFrame for weekdays and one for weekends
weekday_dat = hourlyTotVol[hourlyTotVol.index.weekday < 5].copy()
weekend_dat = hourlyTotVol[hourlyTotVol.index.weekday >= 5].copy()

# Calculate an average volume for each hour of the day by aggregating
# across days using the groupby function - for both weekday and weekend
hourlyAvgWeekdayVol = weekday_dat.groupby(weekday_dat.index.hour).mean()
hourlyAvgWeekendVol = weekend_dat.groupby(weekend_dat.index.hour).mean()

# Also calculate the standard deviation for each hour
hourlyWeekdayStDevVol = weekday_dat.groupby(weekday_dat.index.hour).std()
hourlyWeekendStDevVol = weekend_dat.groupby(weekend_dat.index.hour).std()

# Set the default font size for the plot
font = {'family': 'normal',
        'weight': 'normal',
        'size': 16}
plt.rc('font', **font)

# Generate a single plot to which I can add all of the data subsets
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Create an errorbar plot (lines, point, and errorbars) of the hourly average volumes
plt.errorbar(x=hourlyAvgWeekdayVol.index, y=hourlyAvgWeekdayVol, yerr=hourlyWeekdayStDevVol,
             capsize=3, capthick=0.5, fmt='--', label='Average Hourly Weekday Volumes', marker='o')

plt.errorbar(x=hourlyAvgWeekendVol.index+0.1, y=hourlyAvgWeekendVol, yerr=hourlyWeekendStDevVol,
             capsize=3, capthick=0.5, fmt='--', label='Average Hourly Weekend Volumes', marker='s')

# Set the x-axis tic mark locations
ax.set_xlim(-0.5, 23.5)
xmarks = range(0, 23 + 1, 1)
plt.xticks(xmarks)

# Set the x and y-axis labels
ax.set_ylabel('Average Hourly Volume (gal)')
ax.set_xlabel('Hour of the Day')
ax.grid(False)

# Add a legend with some customizations
legend = ax.legend(loc='upper right', shadow=True)

fig.tight_layout()

# Make sure the plot displays
plt.show()

print 'Done!'

