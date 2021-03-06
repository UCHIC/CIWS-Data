# ------------------------------------------------------
# This code does the following:
# 1. Read the CSV data file into a Pandas data frame
# 2. Subset the data to get a smaller time period for analysis
# 3. Plot the data with a line plot using Matplotlib
# 4. Separate the data into toilet flows and other flows
# Created by:  Jeff Horsburgh
# Last updated: 1-21-2018
# ------------------------------------------------------
# Import the Pandas and Matplotlib packages
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Set up some variables so they are easy to change
# ------------------------------------------------
# The script runs one building at a time, so set the file name to the data file
# for one building and set the correct number of residents for that building
dataPath = ''
# inputFileName = 'datalog_Mountain_View_Tower_2017-3-3_15-33-30.csv'
inputFileName = 'datalog_Valley_View_Tower_2017-3-7_13-9-5.csv'
outputFileName = dataPath + 'processed_' + inputFileName
# Number of residents for Mountain View Tower = 312
# Number of residents for Valley View Tower = 242
# numResidents = 312.0
numResidents = 242.0

# Read the CSV file into a Pandas data frame object
# -------------------------------------------------
df = pd.read_csv(dataPath + inputFileName, header=1, sep=',', index_col=0, parse_dates=True,
                 infer_datetime_format=True, low_memory=False)

# Get a subset of data in a new data frame to analyze
# -----------------------------------------------------
# Full date range (two week period of flows)
beginDate = '2017-03-13 00:00:00'
endDate = '2017-03-26 23:59:59'

# Test date range
# beginDate = '2017-03-13 15:00:00'
# endDate = '2017-03-14 15:00:00'
# beginDate = '2017-03-13 09:27:00'
# endDate = '2017-03-13 10:00:00'

flows = df[beginDate:endDate]['FlowRate']

# Now identify the toilet events
# ------------------------------
# Create the toilet event flows series
toiletEventBeginFlag = []
toiletEventEndFlag = []
toiletEventFlows = []
otherFlows = []
totalFlows = []
eventDates = []
# Initialize a counter for toilet events
toiletEventCounter = 0.0

# Loop through all of the data values in the flows series
x = 0
while x < (len(flows) - 60):  # End 60 values (one minute) short of the end of the flow series to not go out of bounds
    # Check to see if the next value (x + 1) is greater than the current value (x) AND that the difference between
    # the (x + 2) value and the current value (x) is greater than 5 gpm. If so, a likely event is detected.
    if (flows[x + 1] > flows[x]) and (flows[x + 2] - flows[x]) > 5:
        # Check to make sure the following event criteria are met:
        # * Flow peaks at greater than 20 gpm within the first 3 values of the event (peak high enough)
        # * Flow stays above 1.5 gpm until at least the 5th value of the event (event long enough)
        # * The number of flows above 20 gpm in the 20 values following the start of the event must
        #   be less than 12 (event not too long)
        if (flows[x:(x + 4)].max() > 20) and \
           (flows[(x + 2):(x + 6)].min() > 1.5) and \
           (flows[(x + 2):(x + 20)] > 20).sum() < 12:

            # An event has been detected. Add the current value to the output
            toiletEventCounter += 1.0
            toiletEventBeginFlag.append(0)
            toiletEventEndFlag.append(float('nan'))
            toiletEventFlows.append(0.0)
            otherFlows.append(flows[x])
            totalFlows.append(flows[x])
            eventDates.append(flows.index[x])

            # Loop through the next several values to find the end of the event
            endOfEvent = False
            y = 0
            while not endOfEvent:
                try:
                    # Check to make sure the following conditions are true for being within an event:
                    # * The current flow is greater than the flow before the event (x) by at least 10 gpm
                    # OR the following two conditions are true:
                    # * The current flow (x + y + 1) is greater than the flow before the event (x) AND
                    # * The difference between the current flow (x + y + 1) and the mean of the 5 values
                    #   following it is less than 0.125 gpm
                    if (flows[x + y + 1] > flows[x] + 10) \
                            or ((flows[x + y + 1] > flows[x])
                                and (abs(flows[x + y + 1] - flows[(x + y + 2):(x + y + 6)].mean()) > 0.125)):

                        # Check to make sure there is not a second peak after 5 seconds by checking to see if the
                        # flow has dropped below 10 gpm and that the flows are increasing again
                        # if y >= 8 and flows[x + y + 2] < 10 and (flows[x + y + 2] > flows[x + y + 1]):
                        if y >= 4 and flows[x + y + 1] < 10 and (flows[x + y + 2] > flows[x + y + 1] + 0.5):
                            # The flows are going up again, so we are most likely in a double flush event
                            # Need to add an additional flush event to the event begin flags

                            # Check to make sure a new event didn't just start in the previous time step
                            if 0 not in toiletEventBeginFlag[-4:]:
                                # This is likely the start of a new, overlapping event
                                toiletEventCounter += 1.0
                                toiletEventBeginFlag.append(0)
                                toiletEventEndFlag.append(float('nan'))
                            else:
                                # This is a value within the event and not a new event
                                toiletEventBeginFlag.append(float('nan'))
                                toiletEventEndFlag.append(float('nan'))

                        else:
                            # This is a value within the event
                            toiletEventBeginFlag.append(float('nan'))
                            toiletEventEndFlag.append(float('nan'))

                        # Add the event flows to the output
                        toiletEventFlows.append(flows[x + y + 1] - flows[x])
                        otherFlows.append(flows[x])
                        totalFlows.append(flows[x + y + 1])
                        eventDates.append(flows.index[x + y + 1])
                        y += 1

                    else:
                        # The event is over
                        endOfEvent = True
                        toiletEventBeginFlag.append(float('nan'))
                        toiletEventEndFlag.append(0)
                        toiletEventFlows.append(0.0)
                        otherFlows.append(flows[x + y + 1])
                        totalFlows.append(flows[x + y + 1])
                        eventDates.append(flows.index[x + y + 1])

                        # Set the x index so the next flow value processed is the first value after the event
                        # But, check first to make sure that an event flow was actually added
                        if y > 0:  # It was an actual event
                            x += y + 1
                        else:      # The criteria for event detection were true, but no flows were added
                            x += 1
                except:
                    print "Error finding the end of the event for " + str(flows.index[x])
        else:  # The peak and persistence checks are false, so just go to the next data value
            toiletEventBeginFlag.append(float('nan'))
            toiletEventEndFlag.append(float('nan'))
            toiletEventFlows.append(0.0)
            otherFlows.append(flows[x])
            totalFlows.append(flows[x])
            eventDates.append(flows.index[x])
            x += 1
    else:  # The event detection check is false, so just go to the next data value
        toiletEventBeginFlag.append(float('nan'))
        toiletEventEndFlag.append(float('nan'))
        toiletEventFlows.append(0.0)
        otherFlows.append(flows[x])
        totalFlows.append(flows[x])
        eventDates.append(flows.index[x])
        x += 1

# Create a dataframe object from the processed flow rates, which are in gal/min
processedFlows = pd.DataFrame(
    {'TimeStamp': eventDates,
     'ToiletEventBeginFlag': toiletEventBeginFlag,
     'ToiletEventEndFlag': toiletEventEndFlag,
     'ToiletEventFlow': toiletEventFlows,
     'OtherFlow': otherFlows,
     'TotalFlow': totalFlows,
     })
processedFlows.set_index('TimeStamp', inplace=True)

'''
# Generate a plot of the data
# Uncomment this code if you want to run a shorter time window and generate a plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
processedFlows['TotalFlow'].plot(color='blue', linestyle='solid', marker='o', label='Total flow rate (gpm)')
processedFlows['ToiletEventFlow'].plot(color='cyan', linestyle='solid', marker='o', label='Toilet flow rate (gpm)')
processedFlows['OtherFlow'].plot(color='black', linestyle='solid', marker='o', label='Other flow rate (gpm)')
processedFlows['ToiletEventBeginFlag'].plot(color='green', linestyle='None', marker='o', label='Toilet Event Begin Markers')
processedFlows['ToiletEventEndFlag'].plot(color='red', linestyle='None', marker='x', label='Toilet Event End Markers')
ax.set_ylabel('Flow (gpm)')
ax.set_xlabel('Date/Time')
ax.grid(True)
ax.set_title('Total and Toilet Flows')

# Add a legend with some customizations
legend = ax.legend(loc='upper right', shadow=True)

# Create a frame around the legend.
frame = legend.get_frame()
frame.set_facecolor('0.95')

# Make sure the plot displays
fig.set_tight_layout(True)
plt.show()
plt.close()
'''

# Print some totals for the entire monitoring period
# --------------------------------------------------
print 'File analyzed: ' + inputFileName
print 'Number of residents: ' + str(numResidents)
print 'Sampling period analyzed: ' + str(beginDate) + ' through ' + str(endDate)
begin = datetime.strptime(beginDate, "%Y-%m-%d %H:%M:%S")
end = datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S")
delta = end - begin
numDays = round(delta.total_seconds() / 86400.0, 0)
print 'Total number of days analyzed: ' + str(numDays)

# Get the number of toilet flush events, number per resident, and the number per resident per day
print 'Total number of toilet flush events: ' + str(toiletEventCounter)
print 'Toilet flush events per resident: ' + str(round(toiletEventCounter / numResidents, 2))
print 'Toilet flush events per person per day: ' + str(round(toiletEventCounter / numResidents / numDays, 2))

# Calculate the total volume used by toilet flushes - use the trapezoidal rule. Since the
# data are evenly space at one second, I can just sum the gallons per minute flow values
# and then divide by 60 to convert seconds to minutes.
totalFlushVolume = processedFlows['ToiletEventFlow'].sum() / 60
print 'Total volume of toilet flushes (gal): ' + str(round(totalFlushVolume, 2))
print 'Total volume of toilet flushes per resident (gal): ' + str(round(totalFlushVolume / numResidents, 2))
print 'Total volume of toilet flushes per person per day (gal): ' + str(round(totalFlushVolume / numResidents / numDays, 2))

# Calculate the average volume used per toilet flush - this calculate is based on just
# taking the total volume used by the toilets ane dividing by the number of toilet events
avgFlushVolume = totalFlushVolume / toiletEventCounter
print 'Average volume per toilet flush (gal): ' + str(round(avgFlushVolume, 2))

# Calculate the total volume used by uses other than toilets
totalOtherVolume = processedFlows['OtherFlow'].sum() / 60
print 'Total volume of uses other than toilets (gal): ' + str(round(totalOtherVolume, 2))
print 'Total volume of uses other than toilets per resident (gal): ' + str(round(totalOtherVolume / numResidents, 2))
print 'Total volume of uses other than toilets per person per day (gal): ' + \
      str(round(totalOtherVolume / numResidents / numDays, 2))

# Calculate the total volume of water used
totalVolume = processedFlows['TotalFlow'].sum() / 60
print 'Total volume of water used (gal): ' + str(round(totalVolume, 2))
print 'Total volume of water used per resident (gal): ' + str(round(totalVolume / numResidents))
print 'Total volume of water used per person per day (gal): ' + str(round(totalVolume / numResidents / numDays, 2))

# Write out the data to a processed data file
# -------------------------------------------
processedFlows.to_csv(outputFileName, sep=',')

print 'Done!'
