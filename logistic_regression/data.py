import random
import numpy as np
random_data = []

data_map = {
    7: "A",
    8: "B",
    9: "C"
}

x_map = {
    "A": 0,
    "B": 1,
    "C": 2
}

y_data = [random.randint(7, 9) for i in range(1000)]
x_data = [data_map[y] for y in y_data]
x_data = [x_map[x] for x in x_data]
x_data = np.array(x_data).reshape(-1, 1)
y_data = np.array(y_data)

print(x_data, y_data)