# Machine Learning 101 : Simple Linear Regression

## Prerequisites
Understanding of [Data Pre-Processing][].  

## A Simple linear regression  
It follows the formula  `result = bias + slope * feature`  

Which indicates that `bias` is a point on `feature` to `result` graph, when `feature` is `zero`. This also means that bias is an intersection on the result for feature is zero.  

`slope` decides the amount of variation that can be observed **per unit** change of `feature` to corresponding **per unit** change of `result`  

The idea is to have : `Sum(Observed Result - Predicted Result)^2` should be minimum for all `features`

### Use cases where linear regression can be used  
    It can be used any where the `feature` set increases or decreases with the `result` set, with some kind of slope.

## Steps
The preprocessing steps would be:
+ **[Data Pre-Processing][]**  
Since we are dealing with features that are infact related to each other comparatively, we do not need to do feature scaling. we are also not doing the `Handling of missing Data`, `Encoding categorical data`, `Data Normalization`  
+ **Fitting to Simple Linear regression to the Training set**  
  > Code  
    ```
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(features_train, results_train)
    ```  
  At this point the Regression Model is ready and the model has learnt the Salaries based on the experience  

+ **Predicting the Salary for a Experience**  
  Here we create a Vector for predicted Salaries for all the observations of the test set  
  > Code  
  ```
    predicted_salaries = regressor.predict(feature_test)
  ```  
  > Output  
  ```
    >>> print (predicted_salaries)
    [  40835.10590871  123079.39940819  65134.55626083  63265.36777221
    115602.64545369  108125.8914992   116537.23969801  64199.96201652
    76349.68719258  100649.1375447 ]

    >>> print(results_test)
    [  37731.0  122391.0   57081.0  63218.0
    116969.0  109431.0  112635.0  55794.0
    83088.0  101302.0]
   ```
  Comparing the `Predicted_Salaries` v/s `Result_Test` is near by similar considering that we are using Simple Linear Regression.  

+ **Visualizing the training set Data**  
  > Code  
  ```
    import matplotlib.pyplot as plt
    
    plt.scatter(features_train, results_train, color='red')
    plt.plot(features_train, regressor.predict(feature_train), color='blue')
    plt.title('Salary v/s Experience [Training Set]')
    plt.xlable('Years of Experience')
    plt.ylable('Salary')
    plt.show()
  ```  
  > Output  

  ![linearRegression-TrainingSet-plot][]  
  The Predicted values are represented as a blue line  
  The actual salaries w.r.t experience is represented as red dots  

+ **Visualizing the test set Data**  
  > Code  
  ```
    import matplotlib.pyplot as plt
    
    plt.scatter(features_test, results_test, color='red')
    plt.plot(features_train, regressor.predict(feature_train), color='blue')
    plt.title('Salary v/s Experience [Test Set]')
    plt.xlable('Years of Experience')
    plt.ylable('Salary')
    plt.show()
  ```  
  > Output  

  ![linearRegression-TestSet-plot][]  
  The Predicted values are represented as a blue line  
  The actual salaries w.r.t experience is represented as red dots  

## Summary  
Linear regression is suitable for data where the `features` and the `results` increase or decrease linearly  
Data Normalization and Feature scaling is not required as data has a relationship between them.  

The entire python code is here for a quick reference  
> [Code][]
```
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('../datasets/Salary_Data.csv')
features = dataset.iloc[:, :-1].values
result = dataset.iloc[:, 1].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
features_train, features_test, results_train, results_test = train_test_split(features, result, test_size = 1/3, random_state = 0)

# Fir the Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(features_train, results_train)

predicted_salaries = regressor.predict(feature_test)

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
```

[Data Pre-Processing]:Data%20Pre-Processing.md
[linearRegression-TrainingSet-plot]:../images/linearRegression-TrainingSet-plot.png
[linearRegression-TestSet-plot]:../images/linearRegression-TestSet-plot.png
[Code]:../code/linearRegression.py