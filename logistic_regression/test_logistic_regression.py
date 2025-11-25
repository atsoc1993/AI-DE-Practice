from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from data import x_data, y_data

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, random_state=42, train_size=0.50)
model = LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)
y_prediction = model.predict(x_test)
print(f'Accuracy: {accuracy_score(y_test, y_prediction) * 100}%')



