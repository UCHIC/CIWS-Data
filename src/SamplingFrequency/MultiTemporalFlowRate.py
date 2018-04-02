# ------------------------------------------------------------------
# Multi-Temporal Sampling Frequency -- Flow Rates/Cumulative Volume
# ------------------------------------------------------------------
# Written by:   Travis Whitfield
# Date:         Jan. 23, 2018
# Project:      Cyberinfrastructure for Intelligent
#               Water Supply (CIWS)
# Study:        Sampling Frequency Study
# Description:  This Program stores a .csv file into a data
#               frame object, and creates copies of the dataframe
#               simulating different (1s, 2s, 5s, 10s, 30s)
#               frequencies and plots the different frequencies
#               for two different end use events. Creates a plot
#               for 3 longer (day, week, month) timestamps
#               and plots the different frequencies for the
#               longer time periods. Exports the values in
#               an array to a .csv file for post processing in Excel
# --------------------------------------------------------------------
import pandas
import matplotlib.pyplot as plt

# File path to the data file:
dataFilePath = "/Users/Travis/Desktop/Source Code/WaterLab/"
# File name of the data file:
dataFileName = "datalog_Blue_Square_C_2017-6-28_18-29-50.csv"

# Read the .csv file into a pandas data frame:
df = pandas.read_csv(dataFilePath + dataFileName, header=1, sep=',',
                     index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# File path to the data file:
dataFilePath1 = "/Users/Travis/Desktop/Source Code/WaterLab/"
# File name of the data file:
dataFileName1 = "datalog_Mountain_View_Tower_2018-1-25_20-22-45.csv"

# Read the .csv file into a pandas data frame:
df1 = pandas.read_csv(dataFilePath1 + dataFileName1, header=1, sep=',',
                      index_col=0, parse_dates=True,
                      infer_datetime_format=True, low_memory=False)

# The data in the file was scaled wrong, scale the following values in the df:
df1['FlowRate'] = df1['FlowRate'] * (2/5)
df1['IncrementalVolume'] = df['FlowRate'] / 60

# Generate a figure with dimensions (w: 10.0" , h: 4.0")
fig = plt.figure(figsize=(10.0, 4.0))

# --------------------------------------------------------------------
# EVENT #1:
# --------------------------------------------------------------------

# The time frame of the event:
beginDate1 = "01/26/2018 05:49:55"
endDate1 = "01/26/2018 05:50:28"

# Create copies of the data frame, sub sample data
# frame into 2, 5, 10, 30s frequencies.
e1_df_1s = df1[beginDate1:endDate1].copy()
e1_df_2s = e1_df_1s[0::2].copy()
e1_df_5s = e1_df_1s[0::5].copy()
e1_df_10s = e1_df_1s[0::10].copy()
e1_df_30s = e1_df_1s[0::30].copy()

# Subplots the first graph into the first row, left position
ax1 = fig.add_subplot(1, 2, 1)

# Adjust the plot lines for each sub sample frequency
e1_df_1s.plot(y='FlowRate', ax=ax1, kind='Line', use_index=True,
                style='-', ylim=[-0.01, 34], marker='.', markersize=4.0, label='1s Data',
                linewidth=1.5, color='blue')

e1_df_2s.plot(y='FlowRate', ax=ax1, kind='Line', use_index=True,
                style='-', ylim=[-0.01, 34], marker='.', markersize=4.0, label='2s Data',
                linewidth=1.0, color='red')

e1_df_5s.plot(y='FlowRate', ax=ax1, kind='Line', use_index=True,
                style='-', ylim=[-0.01, 34], marker='.', markersize=4.0, label='5s Data',
                linewidth=1.0, color='black')

e1_df_10s.plot(y='FlowRate', ax=ax1, kind='Line', use_index=True,
               style='-', ylim=[-0.01, 34], marker='.', markersize=4.0, label='10s Data',
               linewidth=1.0, color='green')

e1_df_30s.plot(y='FlowRate', ax=ax1, kind='Line', use_index=True,
               style='-', ylim=[-0.01, 34], marker='.', markersize=4.0, label='30s Data',
               linewidth=1.0, color='orange')

# Calculates the cumulative volume change during the event for each separate frequency
e1_df_1s['CumVol'] = e1_df_1s.FlowRate.cumsum() * 1.0 / 60.0
e1_df_2s['CumVol'] = e1_df_2s.FlowRate.cumsum() * 2.0 / 60.0
e1_df_5s['CumVol'] = e1_df_5s.FlowRate.cumsum() * 5.0 / 60.0
e1_df_10s['CumVol'] = e1_df_10s.FlowRate.cumsum() * 10.0 / 60.0
e1_df_30s['CumVol'] = e1_df_30s.FlowRate.cumsum() * 30.0 / 60.0

# Print out the cumulative volume calculations made above to the console
print("---------------------------------------------------------------------")
print("Total volumes over Event #1:")
print("---------------------------------------------------------------------")
print('Total volume estimated from 1 second flow data = ' + str(e1_df_1s['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 2 second flow data = ' + str(e1_df_2s['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 5 second flow data = ' + str(e1_df_5s['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 10 second flow data = ' + str(e1_df_10s['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 30 second flow data = ' + str(e1_df_30s['CumVol'].iloc[-1]))


# --------------------------------------------------------------------
# EVENT #2:
# --------------------------------------------------------------------

# The time frame of the event
beginDate2 = "2017-07-01 03:02:30"
endDate2 = "2017-07-01 03:07:00"

# Create copies of the data frame, sub sample data
# frame into 2, 5, 10, 30s frequencies
e2_df_1s = df[beginDate2:endDate2].copy()
e2_df_2s = e2_df_1s[0::2].copy()
e2_df_5s = e2_df_1s[0::5].copy()
e2_df_10s = e2_df_1s[0::10].copy()
e2_df_30s = e2_df_1s[0::30].copy()

# Subplots the second graph into the first row, right position
# (nrows, ncols, index, **kwargs)
ax2 = fig.add_subplot(1, 2, 2)

# Adjust the plot lines for each sub sample frequency
e2_df_1s.plot(y='FlowRate', ax=ax2, kind='Line', use_index=True,
                style='-', ylim=[-0.01, 2], marker='.', markersize=4.0, label='1s Data',
                linewidth=0.8, color='blue')

e2_df_2s.plot(y='FlowRate', ax=ax2, kind='Line', use_index=True,
                style='-', ylim=[-0.01, 2], marker='.', markersize=4.0, label='2s Data',
                linewidth=0.8, color='red')

e2_df_5s.plot(y='FlowRate', ax=ax2, kind='Line', use_index=True,
                style='-', ylim=[-0.01, 2], marker='.', markersize=4.0, label='5s Data',
                linewidth=0.8, color='black')

e2_df_10s.plot(y='FlowRate', ax=ax2, kind='Line', use_index=True,
               style='-', ylim=[-0.01, 2], marker='.', markersize=4.0, label='10s Data',
               linewidth=0.8, color='green')

e2_df_30s.plot(y='FlowRate', ax=ax2, kind='Line', use_index=True,
               style='-', ylim=[-0.01, 2], marker='.', markersize=4.0, label='30s Data',
               linewidth=0.8, color='orange')

# Calculates the cumulative volume change during the event for each separate frequency
e2_df_1s['CumVol'] = e2_df_1s.FlowRate.cumsum() * 1.0 / 60.0
e2_df_2s['CumVol'] = e2_df_2s.FlowRate.cumsum() * 2.0 / 60.0
e2_df_5s['CumVol'] = e2_df_5s.FlowRate.cumsum() * 5.0 / 60.0
e2_df_10s['CumVol'] = e2_df_10s.FlowRate.cumsum() * 10.0 / 60.0
e2_df_30s['CumVol'] = e2_df_30s.FlowRate.cumsum() * 30.0 / 60.0

# Print out the cumulative volume calculations made above to the console
print("---------------------------------------------------------------------")
print("Total volumes over Event #2:")
print("---------------------------------------------------------------------")
print('Total volume estimated from 1 second flow data = ' + str(e2_df_1s['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 2 second flow data = ' + str(e2_df_2s['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 5 second flow data = ' + str(e2_df_5s['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 10 second flow data = ' + str(e2_df_10s['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 30 second flow data = ' + str(e2_df_30s['CumVol'].iloc[-1]))

# --------------------------------------------------------------------
# Daily:
# --------------------------------------------------------------------
# Begin and end dates for one day of data
beginDate_day = "2018-01-26 11:11:12"
endDate_day = "2018-01-27 12:59:17"

# Create copies simulating the different sampling frequencies over the daily time period
df_1s_day = df1[beginDate_day:endDate_day].copy()
df_2s_day = df_1s_day[0::2].copy()
df_5s_day = df_1s_day[0::5].copy()
df_10s_day = df_1s_day[0::10].copy()
df_30s_day = df_1s_day[0::30].copy()

# Calculate the Cumulative Volume over the daily time period for each frequency
df_1s_day['CumVol'] = df_1s_day.FlowRate.cumsum() * 1.0 / 60.0
df_2s_day['CumVol'] = df_2s_day.FlowRate.cumsum() * 2.0 / 60.0
df_5s_day['CumVol'] = df_5s_day.FlowRate.cumsum() * 5.0 / 60.0
df_10s_day['CumVol'] = df_10s_day.FlowRate.cumsum() * 10.0 / 60.0
df_30s_day['CumVol'] = df_30s_day.FlowRate.cumsum() * 30.0 / 60.0

# Print out the cumulative volume calculations made above to the console
print("---------------------------------------------------------------------")
print("Total volumes over one day:")
print("---------------------------------------------------------------------")
print('Total volume estimated from 1 second flow data = ' + str(df_1s_day['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 2 second flow data = ' + str(df_2s_day['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 5 second flow data = ' + str(df_5s_day['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 10 second flow data = ' + str(df_10s_day['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 30 second flow data = ' + str(df_30s_day['CumVol'].iloc[-1]))

# --------------------------------------------------------------------
# Weekly:
# --------------------------------------------------------------------
# Begin and end dates for one week of data
beginDate_week = "2018-01-26 11:11:12"
endDate_week = "2018-02-02 13:43:43"

# Create copies simulating the different sampling frequencies over the weekly time period
df_1s_week = df1[beginDate_week:endDate_week].copy()
df_2s_week = df_1s_week[0::2].copy()
df_5s_week = df_1s_week[0::5].copy()
df_10s_week = df_1s_week[0::10].copy()
df_30s_week = df_1s_week[0::30].copy()

# Calculate the Cumulative Volume over the weekly time period for each frequency
df_1s_week['CumVol'] = df_1s_week.FlowRate.cumsum() * 1.0 / 60.0
df_2s_week['CumVol'] = df_2s_week.FlowRate.cumsum() * 2.0 / 60.0
df_5s_week['CumVol'] = df_5s_week.FlowRate.cumsum() * 5.0 / 60.0
df_10s_week['CumVol'] = df_10s_week.FlowRate.cumsum() * 10.0 / 60.0
df_30s_week['CumVol'] = df_30s_week.FlowRate.cumsum() * 30.0 / 60.0

# Print out the cumulative volume calculations made above to the console
print("---------------------------------------------------------------------")
print("Total volumes over one week:")
print("---------------------------------------------------------------------")
print('Total volume estimated from 1 second flow data = ' + str(df_1s_week['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 2 second flow data = ' + str(df_2s_week['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 5 second flow data = ' + str(df_5s_week['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 10 second flow data = ' + str(df_10s_week['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 30 second flow data = ' + str(df_30s_week['CumVol'].iloc[-1]))

# --------------------------------------------------------------------
# Monthly:
# --------------------------------------------------------------------
# Begin and end dates for one month of data
beginDate_month = "2018-01-26 11:11:12"
endDate_month = "2018-02-26 09:22:47"

# Create copies simulating the different sampling frequencies over the monthly time period
df_1s_month = df1[beginDate_month:endDate_month].copy()
df_2s_month = df_1s_month[0::2].copy()
df_5s_month = df_1s_month[0::5].copy()
df_10s_month = df_1s_month[0::10].copy()
df_30s_month = df_1s_month[0::30].copy()

# Calculate the Cumulative Volume over the monthly time period for each frequency
df_1s_month['CumVol'] = df_1s_month.FlowRate.cumsum() * 1.0 / 60.0
df_2s_month['CumVol'] = df_2s_month.FlowRate.cumsum() * 2.0 / 60.0
df_5s_month['CumVol'] = df_5s_month.FlowRate.cumsum() * 5.0 / 60.0
df_10s_month['CumVol'] = df_10s_month.FlowRate.cumsum() * 10.0 / 60.0
df_30s_month['CumVol'] = df_30s_month.FlowRate.cumsum() * 30.0 / 60.0

# Print out the cumulative volume calculations made above to the console
print("---------------------------------------------------------------------")
print("Total volumes over one month:")
print("---------------------------------------------------------------------")
print('Total volume estimated from 1 second flow data = ' + str(df_1s_month['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 2 second flow data = ' + str(df_2s_month['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 5 second flow data = ' + str(df_5s_month['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 10 second flow data = ' + str(df_10s_month['CumVol'].iloc[-1]))
print()
print('Total volume estimated from 30 second flow data = ' + str(df_30s_month['CumVol'].iloc[-1]))
# ---------------------------------------------------------------------------------
# Creating the low frequency plot:
# ---------------------------------------------------------------------------------
# Create a second figure for the longer time period plot
fig2 = plt.figure(figsize=(9.0, 4.0))
ax3 = fig2.add_subplot(1, 1, 1)

# Adjust the plot lines for each sub sample frequency
df_1s_month.plot(y='CumVol', ax=ax3, kind='line', use_index=True,
                 style='-', ylim=[-0.5, 200000], label='1s Data', linewidth=0.5)

df_2s_month.plot(y='CumVol', ax=ax3, kind='line', use_index=True,
                 style='-', ylim=[-0.5, 200000], label='2s Data', linewidth=0.5)

df_5s_month.plot(y='CumVol', ax=ax3, kind='line', use_index=True,
                 style='-', ylim=[-0.5, 200000], label='5s Data', linewidth=0.5)

df_10s_month.plot(y='CumVol', ax=ax3, kind='line', use_index=True,
                  style='-', ylim=[-0.5, 200000], label='10s Data', linewidth=0.5)

df_30s_month.plot(y='CumVol', ax=ax3, kind='line', use_index=True,
                  style='-', ylim=[-0.5, 200000], label='30s Data', linewidth=0.5)

# Title for the longer time period plot
ax3.set_title('Totalized Volume of Different Frequencies', fontsize=14)

# y-axis label for the 2nd figure
ax3.set_ylabel('Cumulative Volume (gallons)', fontsize=10)

# x-axis label for the 2nd figure
ax3.set_xlabel('Date', fontsize=10)

# Show the grid lines on the plot
ax3.grid(True)

# Take off the vertical grid lines on the plot
ax3.xaxis.grid(False)

# Add a legend with some customizations
legend = ax3.legend(loc='upper left', shadow=True)

# ---------------------------------------------------------------------------------
# Creating the tables:
# ---------------------------------------------------------------------------------
# Store the cumulative volume calculations in separate arrays
df_Table = pandas.DataFrame({'Event 1': [str(e1_df_1s['CumVol'].iloc[-1]), str(e1_df_2s['CumVol'].iloc[-1]),
                                         str(e1_df_5s['CumVol'].iloc[-1]), str(e1_df_10s['CumVol'].iloc[-1]),
                                         str(e1_df_30s['CumVol'].iloc[-1])],

                             'Event 2': [str(e2_df_1s['CumVol'].iloc[-1]), str(e2_df_2s['CumVol'].iloc[-1]),
                                         str(e2_df_5s['CumVol'].iloc[-1]), str(e2_df_10s['CumVol'].iloc[-1]),
                                         str(e2_df_30s['CumVol'].iloc[-1])],

                             'Daily': [str(df_1s_day['CumVol'].iloc[-1]), str(df_2s_day['CumVol'].iloc[-1]),
                                       str(df_5s_day['CumVol'].iloc[-1]), str(df_10s_day['CumVol'].iloc[-1]),
                                       str(df_30s_day['CumVol'].iloc[-1])],

                             'Weekly': [str(df_1s_week['CumVol'].iloc[-1]), str(df_2s_week['CumVol'].iloc[-1]),
                                        str(df_5s_week['CumVol'].iloc[-1]), str(df_10s_week['CumVol'].iloc[-1]),
                                        str(df_30s_week['CumVol'].iloc[-1])],

                             'Monthly': [str(df_1s_month['CumVol'].iloc[-1]), str(df_2s_month['CumVol'].iloc[-1]),
                                         str(df_5s_month['CumVol'].iloc[-1]), str(df_10s_month['CumVol'].iloc[-1]),
                                         str(df_30s_month['CumVol'].iloc[-1])],
                             },
                            index=['1s', '2s', '5s', '10s', '30s'])

# Store the set of arrays in a single array
data = [df_Table]

# Export the arrays as a .csv file
pandas.concat(data).to_csv('CumVol.csv')

# Confirm the .csv file is being written to
print('Writing CumVol.csv')
print('...')
print('Done!')
# ---------------------------------------------------------------------------------

# Adjust the spacing in between the two event figures
plt.subplots_adjust(left=0.09, wspace=0.05, hspace=0.1)

# Sets the labels for the x/y axes of the first event:
ax1.set_xlabel('Time', fontsize=10)
ax1.set_ylabel('Flow (gpm)', fontsize=10)
ax1.yaxis.labelpad = 12

# Set the label for the second event
ax2.set_xlabel('Time', fontsize=10)
ax2.set_ylabel('Flow (gpm)', fontsize=10)

# Position the label and ticks on the right side of event #2 figure
ax2.yaxis.set_label_position("right")
ax2.yaxis.labelpad = 12
ax2.yaxis.tick_right()

# Set the axis grid to show on the plot:
ax1.grid(True)
ax2.grid(True)

# Create a legend on the plot and place it in the upper right corner:
legend1 = ax1.legend(loc='upper right', shadow=True)
legend2 = ax2.legend(loc='upper right', shadow=True)

# Add a title to the top of the data plot:
ax1.set_title('Comparison of Sampling Intervals \n of End Use Event #1', fontsize=13)
ax2.set_title('Comparison of Sampling Intervals \n of End Use Event #2', fontsize=13)

# Display the plot in the window:
plt.show()

# Confirm the Program ran and then terminated
print('done')



