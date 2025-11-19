from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

data = pd.read_csv(
    filepath_or_buffer='./titanic_problem/train.csv', 
)

y = data['Survived']


original_test_data = pd.read_csv(
    filepath_or_buffer='./titanic_problem/test.csv', 
)


# Name, Ticket, PassengerId feels arbitrary so is removed ## 'Name', 'PassengerId', 'Ticket'
# Sex needs to be mapped to 0, 1
# Parch already mapped to 0, 1
# Sibsp already mapped to 0, 1
# Cabin temporarily removed ## 'Cabin'

all_other_columns = ['Pclass', 'Sex', 'Fare', 'Age', 'SibSp', 'Parch', 'Embarked']

test_data = original_test_data[all_other_columns]

data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
test_data['Sex'] = test_data['Sex'].map({'male': 0, 'female': 1})

data['Embarked'] = data['Embarked'].map({'S': 0, 'Q': 1, 'C': 2})
test_data['Embarked'] = test_data['Embarked'].map({'S': 0, 'Q': 1, 'C': 2})

data['Sex'] = data['Sex'].fillna(data['Sex'].mode()[0])
test_data['Sex'] = test_data['Sex'].fillna(test_data['Sex'].mode()[0])

data['Embarked'] = data['Embarked'].fillna(data['Embarked'].mode()[0])
test_data['Embarked'] = test_data['Embarked'].fillna(test_data['Embarked'].mode()[0])

data['Pclass'] = data['Pclass'].fillna(data['Pclass'].mode()[0])
test_data['Pclass'] = test_data['Pclass'].fillna(test_data['Pclass'].mode()[0])

data['SibSp'] = data['SibSp'].fillna(data['SibSp'].mode()[0])
test_data['SibSp'] = test_data['SibSp'].fillna(test_data['SibSp'].mode()[0])

data['Parch'] = data['Parch'].fillna(data['Parch'].mode()[0])
test_data['Parch'] = test_data['Parch'].fillna(test_data['Parch'].mode()[0])

data['Age'] = data['Age'].fillna(data['Age'].mean())
test_data['Age'] = test_data['Age'].fillna(test_data['Age'].mean())

data['Fare'] = data['Fare'].fillna(data['Fare'].mean())
test_data['Fare'] = test_data['Fare'].fillna(test_data['Fare'].mean())


x = data[all_other_columns]

x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.5,
    random_state=1,

)
classifier = RandomForestClassifier(
    n_estimators=500,
    random_state=1
)

classifier.fit(x_train, y_train)

y_prediction = classifier.predict(x_test)
print(y_prediction)
print(f'Accurancy: {accuracy_score(y_test, y_prediction)}')

test_y_prediction = classifier.predict(test_data)

with open('./titanic_problem/submission.csv', 'w') as f:
    f.write('PassengerId,Survived')
    for passenger_id, result in zip(original_test_data['PassengerId'], test_y_prediction):
        f.write(f'\n{passenger_id},{result}')