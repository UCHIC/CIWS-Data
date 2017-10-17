# ------------------------------------------------------
# Example of how to read the data file into a Pandas
# DataFrame, subset the data to get a smaller time period and
# then plot the data with a line plot using Matplotlib.
# ------------------------------------------------------
# Import the Pandas and Matplotlib packages - must be installed first
import pandas
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas data frame object
df = pandas.read_csv('datalog_richards_hall.csv', header=1, sep=',',
                     index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# Get a subset of data in a new data frame to visualize
# Get one day of data
beginDate = '2017-03-04 00:00:00'
endDate = '2017-03-04 23:59:59'
df_sub = df[beginDate:endDate]

# Get the number of values in the subset data frame
print 'There are ' + str(len(df_sub)) + ' data points in your subset.'

# Generate a plot of the data subset
df_sub.plot(y='FlowRate', kind='line', use_index=True,
            style='-', ylim=[-0.5, 90], marker='o',
            label='Flow rate (gal/min)')

# Get the current axis of the plot and
# set the x and y-axis labels
ax = plt.gca()
ax.set_ylabel('Flow (gpm)')
ax.set_xlabel('Date/Time')
ax.grid(True)

# Add a legend with some customizations
legend = ax.legend(loc='upper right', shadow=True)

# Make sure the plot displays
plt.show()

print 'Done!'
