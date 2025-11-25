import pandas as pd
from random import randint
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

csv_filepath = './practice/arbitrary_data.csv'
with open(csv_filepath, 'w') as f:
    f.write('weight,height,gender')
    for i in range(1000):
        random_weight_for_male = randint(130, 220)
        random_height_for_male = randint(200, 400)
        random_weight_for_female = randint(110, 160)
        random_height_for_female = randint(175, 250)
        f.write(f'\n{random_weight_for_male},{random_height_for_male},male')
        f.write(f'\n{random_weight_for_female},{random_height_for_female},female')

data_features = pd.read_csv(csv_filepath)
data_features['gender'] = data_features['gender'].map({'male': 0, 'female': 1})

x_features = ['height', 'weight']
x = data_features[x_features].to_numpy()
y = data_features['gender'].to_numpy()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.9)

model = LogisticRegression(
    max_iter=1000,
    random_state=1
)

model.fit(x_train, y_train)

y_prediction = model.predict(x_test)

accuracy = accuracy_score(y_test, y_prediction)

print(f'Accuracy score was {accuracy * 100}')

