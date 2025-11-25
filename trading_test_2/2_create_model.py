import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import time


print('Loading CSV . . .')
df = pd.read_csv('./trading_test_2/algo_data_with_rsi.csv')

features = [
    'open','high','low','close','volume',
    'increaseThree','rsi_60','rsi_240'
]

val_1, val_2 = df['increased'].value_counts().values
sum = val_1 + val_2
base_line = val_1 / sum if val_1 > val_2 else val_2 / sum
print(f'Base line accuracy is {base_line * 100}%')

print('Filling empty values . . .')
df['increased'] = df['increased'].fillna(df['increased'].mode()[0])
for col in features:
    df[col] = df[col].fillna(df[col].mode()[0])


print('Dropping NaNs and building data frame . . .')
data = df[features + ['increased']].dropna()


print('Converting X data to numpy . . .')
x_data = data[features].to_numpy()


print('Converting Y data to numpy . . .')
y_data = data['increased'].to_numpy()


print('Creating train/test split . . .')
x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data, random_state=1, test_size=0.1
)

model = LogisticRegression(random_state=1, max_iter=3_000_000)


print('Fitting model . . .')
model.fit(x_train, y_train)

params = model.get_params()
print(params)
# model.set_params()
print('Making prediction . . .')
prediction = model.predict(x_test)


print('Getting accuracy score . . .')
accuracy = accuracy_score(y_test, prediction)
print(f'Predicted price increases/decreases with {accuracy * 100}% accuracy')


'''
from joblib import dump, load  # joblib is preferred for sklearn

print('Fitting model . . .')
model.fit(x_train, y_train)

# Save the whole trained model to disk
dump(model, 'logreg_model.joblib')
Then next time, instead of re-fitting:

python
Copy code
from joblib import load

print('Loading model . . .')
model = load('logreg_model.joblib')

print('Making prediction . . .')
prediction = model.predict(x_test)'''