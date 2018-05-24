import pandas as pd

# Importing the dataset
dataset = pd.read_csv('../datasets/Salary_Data.csv')
features = dataset.iloc[:, :-1].values
result = dataset.iloc[:, 1].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
features_train, features_test, results_train, results_test = train_test_split(features, result, test_size = 1/3, random_state = 0)

# Fit the Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(features_train, results_train)

# Predict the Salaries
predicted_salaries = regressor.predict(features_test)

print(predicted_salaries)
print(results_test)

# Plot the Training Set data
import matplotlib.pyplot as plt
plt.scatter(features_train, results_train, color='red')
plt.plot(features_train, regressor.predict(feature_train), color='blue')
plt.title('Salary v/s Experience [Training Set]')
plt.xlable('Years of Experience')
plt.ylable('Salary')
plt.show()

# Plot the Test Set Data
plt.scatter(features_test, results_test, color='red')
plt.plot(features_train, regressor.predict(feature_train), color='blue')
plt.title('Salary v/s Experience [Test Set]')
plt.xlable('Years of Experience')
plt.ylable('Salary')
plt.show()