# -------------------------------------------------------------------------
# Summary: This script calculates and displays hourly average water use for
# toilets and other water uses based on disaggregated data.
# Written by: Jeff Horsburgh
# Last modified: 3-28-2017
#
# This script assumes that the script to disaggregate the toilet flows has
# already been run.
#
# This code does the following:
# 1. Read the processed csv data files into a Pandas data frames
# 2. Aggregates the data to an hourly scale
# 3. Plots the data with a line plot using Matplotlib
# -------------------------------------------------------------------------
# Import the Pandas and Matplotlib packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set up some variables so they are easy to change
# ------------------------------------------------
womensFileName = 'processed_datalog_Valley_View_Tower_2017-3-7_13-9-5.csv'
mensFileName = 'processed_datalog_Mountain_View_Tower_2017-3-3_15-33-30.csv'
numWomen = 242.0   # Number of residents in Valley View Tower
numMen = 312       # Number of residents in Mountain View Tower

# Read the CSV files into Pandas data frame objects
# Divide all of the values in the data frame by 60
# to convert from gal/min to gal/s
# -------------------------------------------------
wdf = pd.read_csv(womensFileName, header=0, sep=',', index_col=0, parse_dates=True,
                  infer_datetime_format=True, low_memory=False) / 60
mdf = pd.read_csv(mensFileName, header=0, sep=',', index_col=0, parse_dates=True,
                  infer_datetime_format=True, low_memory=False) / 60

# First aggregate the incremental flow volumes to a total volume for each hourly time step
# Normalize by the number of residents in each building
# Output units are gal/person for each hour
# ------------------------------------------------------------------------------------------
w_hourlyToiletVol = wdf['ToiletEventFlow'].resample(rule='1H', base=0).sum() / numWomen
m_hourlyToiletVol = mdf['ToiletEventFlow'].resample(rule='1H', base=0).sum() / numMen
w_hourlyOtherVol = wdf['OtherFlow'].resample(rule='1H', base=0).sum() / numWomen
m_hourlyOtherVol = mdf['OtherFlow'].resample(rule='1H', base=0).sum() / numMen
w_hourlyTotalVol = wdf['TotalFlow'].resample(rule='1H', base=0).sum() / numWomen
m_hourlyTotalVol = mdf['TotalFlow'].resample(rule='1H', base=0).sum() / numMen

# Calculate an average volume for each hour of the day by aggregating
# Units of result are gal/person/hour
# -------------------------------------------------------------------
w_hourlyAvgToiletVol = w_hourlyToiletVol.groupby(w_hourlyToiletVol.index.hour).mean()
m_hourlyAvgToiletVol = m_hourlyToiletVol.groupby(m_hourlyToiletVol.index.hour).mean()
w_hourlyAvgOtherVol = w_hourlyOtherVol.groupby(w_hourlyOtherVol.index.hour).mean()
m_hourlyAvgOtherVol = m_hourlyOtherVol.groupby(m_hourlyOtherVol.index.hour).mean()
w_hourlyAvgTotalVol = w_hourlyTotalVol.groupby(w_hourlyTotalVol.index.hour).mean()
m_hourlyAvgTotalVol = m_hourlyTotalVol.groupby(m_hourlyTotalVol.index.hour).mean()

# Create a line plot of the hourly average flows
# ----------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
w_hourlyAvgToiletVol.plot(color='blue', linestyle='solid', marker='o',
                          label='Men\'s Toilet')
m_hourlyAvgToiletVol.plot(color='red', linestyle='solid', marker='o',
                          label='Women\'s Toilet')
w_hourlyAvgOtherVol.plot(color='blue', linestyle='solid', marker='s',
                         label='Men\'s Other')
m_hourlyAvgOtherVol.plot(color='red', linestyle='solid', marker='s',
                         label='Women\'s Other')
#w_hourlyAvgTotalVol.plot(color='green', linestyle='solid', marker='s',
#                         label='Men\'s Total')
#m_hourlyAvgTotalVol.plot(color='purple', linestyle='solid', marker='s',
#                         label='Women\'s Total')
ax.set_ylabel(' Average Volume (gal/person)')
ax.set_xlabel('Hour of Day')
ax.grid(True)
ax.set_title('Hourly Average Water Use Volume Per Resident')

# Add a legend with some customizations
legend = ax.legend(loc='upper right', shadow=True)

# Create a frame around the legend.
frame = legend.get_frame()
frame.set_facecolor('0.95')

# Make sure the plot displays
fig.set_tight_layout(True)
plt.show()
plt.close()

# Create a stacked bar plot of the hourly average flows
# Example at: https://chrisalbon.com/python/matplotlib_stacked_bar_plot.html
# --------------------------------------------------------------------------
# First for the women:
# Create the general blog and the "subplots" (i.e., the bars)
f, ax1 = plt.subplots(1, figsize=(10, 5))

# Set the bar width
bar_width = 0.75

# Create a list of x-axis positions of the left bar-boundaries
bar_l = [i + 1 for i in range(len(w_hourlyAvgToiletVol))]

# Create a list of the positions of the x-axis ticks (center of the bars as bar labels)
tick_pos = [i + (bar_width / 2) for i in bar_l]

# Create a bar plot in position bar_l for the toilet flush data
ax1.bar(bar_l, w_hourlyAvgToiletVol, width=bar_width, label='Toilet', alpha=0.5, color='green')

# Create a bar plot in position bar_l for the "other" flow data stacked on top of the toilet flush data
ax1.bar(bar_l, w_hourlyAvgOtherVol, width=bar_width, bottom=w_hourlyAvgToiletVol, label='Other', alpha=0.5, color='blue')

# Set the names of the x-axis ticks
plt.xticks(tick_pos, [str(i + 1) for i in range(len(w_hourlyAvgToiletVol))])

# Set the axis labels, plot title, and legend location
ax1.set_ylabel('Average Volume (gal/person)')
ax1.set_xlabel('Hour of Day')
plt.title('Hourly Average Water Use Volume Per Resident')
plt.legend(loc='upper left')

# Set a buffer around the edge of the plot
plt.xlim([min(tick_pos) - bar_width, max(tick_pos) + bar_width])

plt.show()


# Create a heat map plot of the hourly data
# ------------------------------------------
x = np.arange(13, 27, 1)
y = np.arange(0, 24, 1)
x, y = np.meshgrid(x, y)

# z = w_hourlyToiletVol.values
numRows = 24
numColumns = 14
# Toilet Use: Women's total goes up to about 0.75, men's total goes up to about 0.6
#z = np.reshape(w_hourlyToiletVol.values, (numRows, numColumns), order='F')
#z = np.reshape(m_hourlyToiletVol.values, (numRows, numColumns), order='F')
# Other Use: Women's total goes up to about 1.1, men's total goes up to just over 1.1
#z = np.reshape(w_hourlyOtherVol.values, (numRows, numColumns), order='F')
#z = np.reshape(m_hourlyOtherVol.values, (numRows, numColumns), order='F')
# Total Use: Women's total goes up to 1.6, men's total goes up to just over 1.2
z = np.reshape(w_hourlyTotalVol.values, (numRows, numColumns), order='F')
#z = np.reshape(m_hourlyTotalVol.values, (numRows, numColumns), order='F')

fig, ax = plt.subplots()
im = ax.pcolormesh(x, y, z, vmin=z.min(), vmax=z.max())
# im = ax.pcolormesh(x, y, z, vmin=0.0, vmax=1.1)
# plt.axis([x.min(), x.max(), y.min(), y.max()])
fig.colorbar(im).set_label('Water Use (gal/person)')

ax.set_xlabel('Day')
ax.set_ylabel('Hour of Day')
ax.axis('tight')
plt.title('Heatmap of Hourly Water Use')
plt.show()

# # Create a heat map plot of the 1 s data
# # TODO:  Currently not normalized per person
# # ----------------------------------------
# x = np.arange(13, 26, 1)
# y = np.arange(0, 86400, 1)
# x, y = np.meshgrid(x, y)
#
# # z = w_hourlyToiletVol.values
# numRows = 86400
# numColumns = 13
# z = np.reshape(wdf.TotalFlow.values[:-86339], (numRows, numColumns), order='F')
#
# fig, ax = plt.subplots()
# im = ax.pcolormesh(x, y, z)
# fig.colorbar(im).set_label('Water Use (gal)')
#
# ax.set_xlabel('Day')
# ax.set_ylabel('Second of Day')
# ax.axis('tight')
# plt.title('Heatmap of Water Use')
# plt.show()


print "Done!"

