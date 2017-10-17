# ------------------------------------------------------
# Example of how to read the data file into a Pandas
# DataFrame and then get some simple characteristics
# of the DataFrame.
# ------------------------------------------------------
# Import the Pandas package - must be installed before you can use it
import pandas

# Read the CSV file into a Pandas data frame object
# -------------------------------------------------
# Check your file name to make sure it is the same as mine
df = pandas.read_csv('datalog_richards_hall.csv', header=1, sep=',',
                     index_col=0, parse_dates=True,
                     infer_datetime_format=True, low_memory=False)

# Get the number of values in the data frame and the minimum and max date
# The "str" function converts other items to a text string
# String concatenation is done with the "+" operator
print 'There are ' + str(len(df)) + ' data points in the data frame.'
print 'The begin date is ' + str(df.index.min())
print 'The end date is ' + str(df.index.max())

# Print the column headers and first few rows of the data frame
print ('\nColumn headers and first few rows of data:\n')
print(df.head(5))

# Print a statistical summary for each column of the data frame
print ('\nStatistical summary for each column:\n')
print(df.describe())

# Print a list of the column names in the data frame
print ('\nList of column names in the data frame:\n')
print(df.columns)

# Print a list of data types for each of the columns in the data frame
print ('\nData types for each column:\n')
print(df.dtypes)

print 'Done!'

