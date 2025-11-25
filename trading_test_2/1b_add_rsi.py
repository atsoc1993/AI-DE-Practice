import pandas as pd
import numpy as np

df = pd.read_csv('./trading_test_2/algo_data_with_flag.csv')


def rsi(series, period):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

df['rsi_14'] = rsi(df['close'], 14)
df['rsi_60'] = rsi(df['close'], 60)
df['rsi_240'] = rsi(df['close'], 240)

df.to_csv('./trading_test_2/algo_data_with_rsi.csv', index=False)
