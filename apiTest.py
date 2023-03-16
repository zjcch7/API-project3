from alpha_vantage.timeseries import TimeSeries
import requests
from pprint import pprint
ts = TimeSeries(key='Y7P82MTGYSOW6CEX', output_format='pandas')
data, meta_data = ts.get_intraday(symbol=input('Please Enter The Symbol: '),interval=input('Please Enter the interval: '), outputsize='full')
pprint(data.head(2))
