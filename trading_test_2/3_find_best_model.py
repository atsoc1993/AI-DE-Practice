import time
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from joblib import dump  # for saving the best model

print('Loading CSV . . .')
df = pd.read_csv('./trading_test_2/algo_data_with_rsi.csv')

features = [
    'open','high','low','close','volume',
    'increaseThree','increaseFour','increaseFive',
    'increaseSix','increaseSeven','increaseEight',
    'increaseNine','increaseTen',
    'rsi_14','rsi_60','rsi_240'
]

val_counts = df['increased'].value_counts()
if len(val_counts) == 2:
    val_1, val_2 = val_counts.values
    total = val_1 + val_2
    base_line = max(val_1, val_2) / total
    print(f'Base line accuracy is {base_line * 100:.2f}%')
else:
    print("Warning: 'increased' doesn't have exactly 2 classes, baseline skipped.")

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

base_model = LogisticRegression(
    random_state=1,
    max_iter=10_000
)

param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'penalty': ['l1', 'l2'],
    'class_weight': [None, 'balanced'],
    'solver': ['liblinear'],
}

print('Starting grid search (brute forcing params) . . .')
t0 = time.time()

grid_search = GridSearchCV(
    estimator=base_model,
    param_grid=param_grid,
    scoring='accuracy',
    cv=5,
    n_jobs=-1,
    verbose=1
)

grid_search.fit(x_train, y_train)

t1 = time.time()
print(f'Grid search done in {t1 - t0:.2f} seconds.')

print('Best params found:')
print(grid_search.best_params_)
print(f'Best CV accuracy: {grid_search.best_score_ * 100:.2f}%')

best_model = grid_search.best_estimator_

print('Making prediction with best model . . .')
prediction = best_model.predict(x_test)

print('Getting accuracy score . . .')
accuracy = accuracy_score(y_test, prediction)
print(f'Predicted price increases/decreases with {accuracy * 100:.2f}% accuracy')

dump(best_model, 'logreg_best_model.joblib')
print("Saved best model to 'logreg_best_model.joblib'")
