from alpha_vantage.timeseries import TimeSeries
import requests
import pygal
import lxml
                    
def do_another_stock():
    do_another_stock=True
    while(do_another_stock):
        another_stock = input("Would you like to analyze another stock?(y/n): ")
        if(another_stock=="y"):
            do_another_stock=main()
        if(another_stock!="y"):
            do_another_stock=False

def main():
    while True:
        try:
            print("Stock Data Visualizer")
            print("----------------------")
            print(" ")
            stock_symbol = input("Enter stock symbol: ")
            print(" ")
            print("Chart Types")
            print("-------------")
            print("1: Line")
            print("2: Bar")
            print(" ")
            while(True):
                try:
                    chart_type = int(input("Enter chart type (1, 2): "))
                    if(chart_type < 1 or chart_type > 2):
                        print('please enter 1 or 2')
                        continue
                except ValueError:
                        print("Please enter only Numerical values")
                else:
                        break
            print(" ")
            print("Select Time Series of the chart you want to Generate")
            print("------------------------------------------------------")
            print("1: Intraday")
            print("2: Daily")
            print("3: Weekly")
            print("4: Monthly")
            print(" ")
            while(True):
                try:
                    time_series = int(input("Enter time series function (1-4): "))
                    #checks if user input is between 1-4
                    if (time_series >4 or time_series <1):
                        print('Please enter a number 1-4')
                        continue
                #exception handles error if user input is not an integer.    
                except ValueError:
                        print('Please enter only numerical values')
                else:
                    break
            #reads user input and will adjust url. Also checks to see if user selects intraday.
            if time_series == 1:
                interval = input("Enter time interval (1min, 5min, 15min, 30min, or 60min): ")
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval={interval}&apikey=Y7P82MTGYSOW6CEX"
            elif time_series == 2:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&symbol={stock_symbol}&apikey=Y7P82MTGYSOW6CEX"
            elif time_series == 3:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={stock_symbol}&apikey=Y7P82MTGYSOW6CEX"
            elif time_series == 4:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={stock_symbol}&apikey=Y7P82MTGYSOW6CEX"    
            
            while(True):
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    #checks if end_date is less than start_date
                    if end_date < start_date:
                        print("end date cannot be before start date")
                        continue
                    elif end_date > start_date:
                        break               
            
            try:
                #using requests, an HTTP GET request is sent to the url that the user picks by selecting a specific time series 
                get_url = requests.get(url)
                #returns an HTTPError object if an error happens during the HTTP GET process
                get_url.raise_for_status()
            except HTTPError as e:
                print(f"Error retrieving data: {e}")
            

            #json is used to parse data from get_url that the user wants into the stock_data variable
            stock_data = get_url.json()
            #Checks the number of keys in the stock_data is less than 2. If there is, an error will happen.
            if len(stock_data.keys()) < 2:
                print("Invalid stock. Be sure to use all caps and correct stock symbol.")
                continue
            
            #The data stored in time series api has the stock symbol listed as the second key
            #stock_key varibale converts the keys to a list and grabs the second key and is assigned to it
            stock_key = list(stock_data.keys())[1]

            data = stock_data[stock_key]

            data_dict = {}
            #if statement that adds intraday data
            if time_series == "intraday":
                for intraday_time, values in data.items():
                    date = inraday_time[:10]
                    if start_date <= date <= end_date:
                        data_dict[intraday_time] = values
            #else statement that adds every other time_series function to the dictionary if used
            else:
                for date, values in data.items():
                    if start_date <= date <= end_date:
                        data_dict[date] = values
                        
            #sorts data_dict items found based off user inputs into tuple lists
            #using sorted, the list returns in ascending order that is assigned to sorted_data which will be used to create the pygal graph
            sorted_data = sorted(data_dict.items())

            #determines chart type based on user input
            if chart_type == 1:
                chart = pygal.Line(x_label_rotation=30, show_minor_x_labels=True)
            elif chart_type == 2:
                chart = pygal.Bar(x_label_rotation=30, show_minor_x_labels=True)

            chart.title = f"{stock_symbol} Stock: {start_date} to {end_date}"
            chart.x_labels = [date for date, value in sorted_data]
            chart.add("Open", [float(value["1. open"]) for date, value in sorted_data])
            chart.add("High", [float(value["2. high"])for date, value in sorted_data])
            chart.add("Low", [float(value["3. low"]) for date, value in sorted_data])
            chart.add("Close", [float(value["4. close"]) for date, value in sorted_data])
            chart.render_in_browser()
            break
        except Exception as e:
            print(e)

    do_another_stock()
main()

