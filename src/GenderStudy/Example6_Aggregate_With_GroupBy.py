# ------------------------------------------------------
# Example of how to read the data file into a Pandas
# data frame, aggregate the data to a longer time step -
# e.g., aggregate to hourly average flows and then
# plot the data.
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

# First aggregate the incremental flow volume to a total volume for each hourly time step
# ---------------------------------------------------------------------------------------
hourlyTotVol = df['IncrementalVolume'].resample(rule='1H', base=0).sum()

# Calculate an average volume for each hour of the day by aggregating
# -------------------------------------------------------------------
hourlyAvgVol = hourlyTotVol.groupby(hourlyTotVol.index.hour).mean()

# Create a bar chart of the hourly flows
# --------------------------------------
hourlyAvgVol.plot(kind='bar', use_index=True)

ax = plt.gca()
ax.set_ylabel('Average Hourly Volume (gal)')
ax.set_xlabel('Hour of the Day')
ax.grid(True)

# Make sure the plot displays
plt.show()

print 'Done!'

