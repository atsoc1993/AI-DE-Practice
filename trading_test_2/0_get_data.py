import os
import requests
from datetime import datetime, timedelta
import calendar

raw_data_file_name = './trading_test_2/algo_data.csv'

if not os.path.exists(raw_data_file_name):
    with open(raw_data_file_name, 'w') as f:
        f.write('open,high,low,close,volume')

start_year = 2020
end_year = 2025

with open(raw_data_file_name, 'a') as f:
    for year in range(start_year, end_year + 1):
        print(f'Year: {year}')
        for month in range(1, 13):
            print(f'Month: {month}')
            days_in_month = calendar.monthrange(year, month)[1]
            for day in range(1, days_in_month + 1):
                print(f'Day: {day}')
                for hour in range(0, 24):
                    start_time = datetime(year=year, month=month, day=day, hour=hour)
                    end_time = start_time + timedelta(hours=1)

                    start_time_iso = start_time.isoformat()
                    end_time_iso = end_time.isoformat()

                    url_1 = f'https://api.exchange.coinbase.com/products/ALGO-USD/candles?granularity=60&start={start_time_iso}&end={end_time_iso}'

                    response = requests.get(url_1)
                    candles = response.json()

                    for r in candles:
                        try:
                            timestamp, low, high, open_, close, volume = r
                            f.write(f'\n{open_},{high},{low},{close},{volume}')
                        except:
                            import time
                            print(f'Error... sleeping')
                            time.sleep(100)
                            url_1 = f'https://api.exchange.coinbase.com/products/ALGO-USD/candles?granularity=60&start={start_time_iso}&end={end_time_iso}'

                            response = requests.get(url_1)
                            candles = response.json()
                            
                            for s in candles:
                                timestamp, low, high, open_, close, volume = s
                                f.write(f'\n{open_},{high},{low},{close},{volume}')
                            break
                            