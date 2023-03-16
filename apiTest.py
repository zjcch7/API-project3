from alpha_vantage.timeseries import TimeSeries
import requests
import pygal
import lxml
from pprint import pprint
while(True):
    try:
    
        ts = TimeSeries(key='Y7P82MTGYSOW6CEX', output_format='pandas')

        data_daily, meta_data = ts.get_daily_adjusted(symbol=input('Please Enter The Symbol: '), outputsize='full')

        start_date = datetime.datetime(input('Enter Start Date (MUST BE YYYY, MM, DD): '))
        end_date = datetime.datetime(input('Enter End Date (MUST BE YYYY, MM, DD)'))

        date_filter = data_daily[(data_daily.index > start_date) & (data_daily.index <= end_date)]
        date_filter = date_filter.sort_index(ascending=True)


        pprint(data.head(2))

    except:
        while(True):
            another_stock = input("Do you want to look at another stock? (y/n): ")
            if (another_stock != "y"):
            break
