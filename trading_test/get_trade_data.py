import requests
from datetime import datetime
from time import time as t
import json
import os

start_year = 2025
end_year = 2019

jan = 1
june = 6
dec = 12

file_name = 'algo_data.csv'

if not os.path.exists(file_name):
    with open(file_name, 'w') as f:
        pass

        f.write('Day,#OpenP')
        for i in range(start_year, end_year, -1):
            start_time_1 = datetime(year=start_year, month=jan, day=1, hour=0).isoformat()
            end_time_1 = datetime(year=start_year, month=june, day=1, hour=0).isoformat()
            url_1 = f'https://api.exchange.coinbase.com/products/ALGO-USD/candles?granularity=86400&start={start_time_1}&end={end_time_1}'

            start_time_2 = datetime(year=start_year, month=june, day=1, hour=0).isoformat()
            end_time_2 = datetime(year=start_year, month=dec, day=1, hour=0).isoformat()
            url_2 = f'https://api.exchange.coinbase.com/products/ALGO-USD/candles?granularity=86400&start={start_time_2}&end={end_time_2}'

            response_1: list[list] = requests.get(url_1).json()
            response_2: list[list] = requests.get(url_2).json()
            response = response_2 + response_1
            for r in response:
                open_price = r[3]
                time = datetime.fromtimestamp(r[0]).date()
                f.write(f'\n{time},{open_price}')

            start_year -= 1
