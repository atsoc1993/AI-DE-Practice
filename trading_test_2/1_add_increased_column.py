import pandas as pd

raw_data_file_name = './trading_test_2/algo_data.csv'
data_with_increase_decrease_flag = './trading_test_2/algo_data_with_flag.csv'

algo_trade_data = pd.read_csv(raw_data_file_name)

algo_trade_data['next_close'] = algo_trade_data['close'].shift(-1)
algo_trade_data['increased'] = (algo_trade_data['next_close'] > algo_trade_data['close']).astype('int8')
algo_trade_data.loc[algo_trade_data.index[-1], 'increased'] = ''   # last row has no next_close


algo_trade_data['prev3_avg'] = algo_trade_data['close'].rolling(window=3).mean().shift(1)

algo_trade_data['increaseThree'] = (
    algo_trade_data['close'] > algo_trade_data['prev3_avg']
).astype('int8')

mask_edge = algo_trade_data['prev3_avg'].isna()
algo_trade_data.loc[mask_edge, 'increaseThree'] = ''

algo_trade_data[['open', 'high', 'low', 'close', 'volume', 'increased', 'increaseThree']].to_csv(
    data_with_increase_decrease_flag,
    index=False
)
