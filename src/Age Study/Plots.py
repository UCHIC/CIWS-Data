import pandas
import datetime


dataPath = '/Users/nikki/Dev/CIWS-Data/src/Age Study/'
inputFileName = 'datalog_Snow_Hall_2017-6-6_12-52-2.csv'
df_SnowHall = pandas.read_csv(dataPath + inputFileName,
                              header=1, sep=',', index_col=0, parse_dates=True,
                              infer_datetime_format=True, low_memory=False, lineterminator='\n')

outputFileName = dataPath + 'processed_' + inputFileName

date = df_SnowHall.index + datetime.timedelta(hours=1)
flowRate = df_SnowHall['FlowRate'] * 5
incrementalVolume = df_SnowHall['IncrementalVolume'] * 5
totalizedVolume = df_SnowHall['TotalizedVolume'] * 5

processed = pandas.DataFrame(
    {'Date': date,
     'FlowRate': flowRate,
     'IncrementalVolume': incrementalVolume,
     'TotalizedVolume': totalizedVolume,
     })
processed.set_index('Date', inplace=True)
processed.to_csv(outputFileName, sep=',', header=True)

# processedSnowHall = {'Date': date,
#                      'FlowRate': flowRate,
#                      'IncrementalVolume': incrementalVolume,
#                      'TotalizedVolume': totalizedVolume}
# df = pandas.DataFrame(processedSnowHall, columns=['Date', 'FlowRate', 'IncrementalVolume', 'TotalizedVolume'])
# df.set_index('Date', inplace=True)
# df.to_csv(outputFileName, sep=',')

print(processed.columns)