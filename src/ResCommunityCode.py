import pandas
import matplotlib.pyplot as plt


# Read the data files for the Sturdent Residential Buildings
df_ = pandas.read_csv('/Users/amycarmellini/Develop/ciws-data/src/Dorm Data.csv',
                                  header=1, sep=',', index_col=0, parse_dates=True,
                                  infer_datetime_format=True, low_memory=False)




# Normalize the data for each month per resident
monthyDormPerRes = hourlyAvgVolMountain / mountainViewResidents
hourlyAvgVolValleyPerRes = hourlyAvgVolValley / valleyViewResidents