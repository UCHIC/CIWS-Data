import pandas
import matplotlib.pyplot as plt

dataPath = '/Users/nikki/Dev/CIWS-Data/src/Age Study/'
df = pandas.read_csv(dataPath + 'datalog_Snow_Hall_2017-6-6_12-52-2.csv',
                     header=1, sep=',', index_col=0, parse_dates=True,
                    infer_datetime_format=True, low_memory=False)

print 'There are ' + str(len(df)) + ' data points in the data frame.'
print 'The beginning date is ' + str(df.index.min())
print 'The end date is ' + str(df.index.max())

# Generate a plot of the data subset
# Generate a plot of the data subset
df.plot(y='FlowRate', kind='line', use_index=True,
            linestyle='solid', ylim=[-0.5, 25], style='o',
            label='Flow rate (gal/min)')

MinuteVol = df.resample(rule='1H', how='sum', base=0)
MinuteVol.plot(y='IncrementalVolume', kind='line', use_index=True,
               linestyle='solid', ylim=[-0.5, 600], style='o',
               label='Hourly total volume (gal)')

# Get the current axis of the plot and set the x and y-axis labels
ax = plt.gca()
ax.set_ylabel('Flow (gpm)')
ax.set_xlabel('Date/Time')
ax.grid(True)

# Add a legend with some customizations
legend = ax.legend(loc='upper right', shadow=True)

# Make sure the plot displays
plt.show()
plt.close()

df['CumVol'] = df.FlowRate.cumsum() * 1.0 / 60.0
print str(df['CumVol'].iloc[-1])

print 'Done!'