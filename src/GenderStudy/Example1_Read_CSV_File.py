# ------------------------------------------------------
# Example of how to read the CSV data file into a Pandas
# data frame and then get some simple characteristics
# of the data frame.
# Created by:  Jeff Horsburgh
# Last updated: 4-13-2017
# ------------------------------------------------------
# Import the Pandas package - must be installed before you can use it
import pandas

# Read the CSV file into a Pandas data frame object
# -------------------------------------------------
dataPath = '/users/jeff/Documents/Working/Data/CampusWaterUse/'
df = pandas.read_csv(dataPath + 'datalog_Valley_View_Tower_2017-3-7_13-9-5.csv',
                     header=1, sep=',', index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# Get the number of values in the data frame and the minimum and max date
# The "str" function converts other items to a text string
# String concatenation is done with the "+" operator
print 'There are ' + str(len(df)) + ' data points in the data frame.'
print 'The begin date is ' + str(df.index.min())
print 'The end date is ' + str(df.index.max())

print(df.head())  # Print the column headers and first few rows of the data frame
print(df.describe())  # Print a statistical summary for each column of the data frame
print(df.columns)  # Print a list of the column names in the data frame
print(df.dtypes)  # Print a list of data types for each of the columns in the data frame

print 'Done!'

I added a new line that is going to cause this script to crash

