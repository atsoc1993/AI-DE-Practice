import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_squared_error
from statsmodels.tools.eval_measures import rmse
from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings

warnings.filterwarnings("ignore")

algo_trade_data = pd.read_csv(
    'algo_data.csv',
    index_col='Day',
    parse_dates=True
)

algo_trade_data = algo_trade_data[~algo_trade_data.index.duplicated(keep='last')]
algo_trade_data = algo_trade_data.sort_index()
algo_trade_data = algo_trade_data.asfreq('D')
algo_trade_data['#OpenP'] = algo_trade_data['#OpenP'].ffill().bfill()

print(algo_trade_data.head())

result = seasonal_decompose(
    algo_trade_data['#OpenP'],
    model='multiplicative',
    period=7
)
result.plot()
plt.show()

stepwise_fit = auto_arima(
    algo_trade_data['#OpenP'], start_p=1, start_q=1,
    max_p=3, max_q=3, m=30,
    start_P=0, seasonal=True,
    d=None, D=1, trace=True,
    error_action='ignore',
    suppress_warnings=True,
    stepwise=True
)

print(stepwise_fit.summary())
print("Chosen order:", stepwise_fit.order)
print("Chosen seasonal order:", stepwise_fit.seasonal_order)

train = algo_trade_data.iloc[:len(algo_trade_data) - 12]
test = algo_trade_data.iloc[len(algo_trade_data) - 12:]

order = stepwise_fit.order
seasonal_order = stepwise_fit.seasonal_order

model = SARIMAX(
    train['#OpenP'],
    order=order,
    seasonal_order=seasonal_order
)
result = model.fit()
print(result.summary())

pred_res = result.get_prediction(start=test.index[0], end=test.index[-1])
predictions = pred_res.predicted_mean
predictions.name = "Predictions"

ax = test['#OpenP'].plot(legend=True, label='#OpenP')
predictions.plot(ax=ax, legend=True)
plt.show()

print("RMSE:", rmse(test["#OpenP"], predictions))
print("MSE:", mean_squared_error(test["#OpenP"], predictions))

full_model = SARIMAX(
    algo_trade_data['#OpenP'],
    order=order,
    seasonal_order=seasonal_order
)
full_result = full_model.fit()

days_ahead = 30
forecast_res = full_result.get_forecast(steps=days_ahead)
forecast = forecast_res.predicted_mean
forecast.name = "Forecast"

ax = algo_trade_data['#OpenP'].plot(figsize=(12, 5), legend=True, label='Historical')
forecast.plot(ax=ax, legend=True, label='Forecast')
plt.show()
