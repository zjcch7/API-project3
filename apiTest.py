from alpha_vantage.timeseries import TimeSeries
import requests
import pygal
from lxml import etree



print("Stock Data Visualizer")
print("----------------------")
while(True):
    try:
        print(" ")
        stock_symbol = input("Enter stock symbol: ")
        print(" ")
        print("Chart Types")
        print("-------------")
        print("1: Line")
        print("2: Bar")
        print(" ")
        chart_type = input("Enter chart type (1, 2): ")
        print(" ")
        print("Select Time Series of the chart you want to Generate")
        print("------------------------------------------------------")
        print("1: Intraday")
        print("2: Daily")
        print("3: Weekly")
        print("4: Monthly")
        print(" ")
        time_series = input("Enter time series function (1-4): ")
        if time_series == "1":
            interval = input("Enter time interval (1min, 5min, 15min, 30min, or 60min): ")
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey=Y7P82MTGYSOW6CEX"
        elif time_series == "2":
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&symbol={symbol}&apikey=Y7P82MTGYSOW6CEX"
        elif time_series == "3":
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey=Y7P82MTGYSOW6CEX"
        elif time_series == "4":
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey=Y7P82MTGYSOW6CEX"

        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        get_url = requests.get(url)
        get_url.raise_for_status()

        json_data = get_url.json()
        json_key = list(json_data.keys())[1]
        data = json_data[json_key]

        data_dict = {}
        if time_series == "intraday":
            for intraday_time, values in data.items():
                date = intraday_time[:10]
                if start_date <= date <= end_date:
                    data_dict[intraday_time] = values
        else:
            for date, values in data.items():
                if start_date <= date <= end_date:
                    data_dict[date] = values

        sorted_data = sorted(filtered_data.items(), reverse=False)

        if chart_type == "1":
            chart = pygal.Line(x_label_rotation=20, show_minor_x_labels=True)
        elif chart_type == "2":
            chart = pygal.Bar(x_label_rotation=20, show_minor_x_labels=True)


        chart.title = f"{symbol} Stock: {start_date} to {end_date}"
        chart.x_labels = [date for date, value in sorted_data]
        chart.add("Open", [float(value["1. open"]) for date, value in sorted_data])
        chart.add("High", [float(value["2. high"])for date, value in sorted_data])
        chart.add("Low", [float(value["3. low"]) for date, value in sorted_data])
        chart.add("Close", [float(value["4. close"]) for date, value in sorted_data])
        chart.render_in_browser()
       
    except:
        another_stock = input("Do you want to look at another stock? (y/n): ")
        if (another_stock != "y"):
            break
