# Machine Learning 101 : Data Pre-Processing

## Prerequisites
Install the Python and Anaconda environment as described in the [Development Environment Setup][] Page.

## Data Preparation - Data Preprocessing
Training a Model needs Data, Data needs to be valid, Validation requires preprocessing.
Assuming we have a `CSV` file which has data in the below format; such that `Country`, `Age`, & `Salary` become the input **features** and `Purchaced` becomes the **result** which needs to be **Predicted** by our model:
<table>
   <tr><th> Country</th><th>Age</th><th>Salary</th><th>Purchased</th></tr>
   <tr><td> France</td><td>44</td><td>72000</td><td>No</td></tr>
   <tr><td> Spain</td><td>27</td><td>48000</td><td>Yes</td></tr>
   <tr><td> Germany</td><td>30</td><td>54000</td><td>No</td></tr>
   <tr><td> Spain</td><td>38</td><td>61000</td><td>No</td></tr>
   <tr><td> Germany</td><td>40</td><td></td><td>Yes</td></tr>
   <tr><td> France</td><td>35</td><td>58000</td><td>Yes</td></tr>
   <tr><td> Spain</td><td></td><td>52000</td><td>No</td></tr>
   <tr><td> France</td><td>48</td><td>79000</td><td>Yes</td></tr>
   <tr><td> Germany</td><td>50</td><td>83000</td><td>No</td></tr>
   <tr><td> France</td><td>37</td><td>67000</td><td>Yes</td></tr>
</table>

## Steps
The preprocessing steps would be:
+ Load the data so that it can be processed. This is achieved using the library `pandas`
    > Code
    ```
    import pandas as pd

    dataset = pd.read_csv('Data.csv')
    features = dataset.iloc[:, :-1].values
    result = dataset.iloc[:, 3].values
    ```
    >Output
    ```
    >>> print(dataset)
    Country   Age   Salary Purchased
    0   France  44.0  72000.0        No
    1    Spain  27.0  48000.0       Yes
    2  Germany  30.0  54000.0        No
    3    Spain  38.0  61000.0        No
    4  Germany  40.0      NaN       Yes
    5   France  35.0  58000.0       Yes
    6    Spain   NaN  52000.0        No
    7   France  48.0  79000.0       Yes
    8  Germany  50.0  83000.0        No
    9   France  37.0  67000.0       Yes

    >>> print(features)
    [['France' 44.0 72000.0]
     ['Spain' 27.0 48000.0]
     ['Germany' 30.0 54000.0]
     ['Spain' 38.0 61000.0]
     ['Germany' 40.0 nan]
     ['France' 35.0 58000.0]
     ['Spain' nan 52000.0]
     ['France' 48.0 79000.0]
     ['Germany' 50.0 83000.0]
     ['France' 37.0 67000.0]]

    >>> print(result)
    ['No' 'Yes' 'No' 'No' 'Yes' 'Yes' 'No' 'Yes' 'No' 'Yes']
    ```

+ **Handle the missing Data**  
This can be done using a [Mean][] or a [Standard Deviation][] for the corresponding feature set. Moost of the times the ML Library being used can handle handle missing data automatically, as such this step is optional for most of the use cases.  

  Missing data handling is achieved using the library `Scikit-Learn`
    > Code
    ```
    from sklearn.preprocessing import Imputer

    imputer = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0)
    imputer = imputer.fit(features[:, 1:3])
    features[:, 1:3] = imputer.transform(features[:, 1:3])
    ```
    > Output
    ```
    >>> print(features)
    [['France' 44.0 72000.0]
     ['Spain' 27.0 48000.0]
     ['Germany' 30.0 54000.0]
     ['Spain' 38.0 61000.0]
     ['Germany' 40.0 63777.77777777778]
     ['France' 35.0 58000.0]
     ['Spain' 38.77777777777778 52000.0]
     ['France' 48.0 79000.0]
     ['Germany' 50.0 83000.0]
     ['France' 37.0 67000.0]]
    ```
 + **Encoding categorical data**  
  Another optional step where we try to categorize or Encode the Text into some kind of numerical representation so that our numerical model can handle this data easily. For example in the current data set `Country` is converted to numbers so as `France` -> `0`, `Spain` -> `2`, `Germany` -> `1` and `Purchased` is converted to `yes` -> `1`, `No` -> `0`
    > Code
    ```
    from sklearn.preprocessing import LabelEncoder

    labelencoder_features = LabelEncoder()
    features[:, 0] = labelencoder_features.fit_transform(features[:, 0])
    labelencoder_results = LabelEncoder()
    result = labelencoder_results.fit_transform(result)
    ```  
    > Output  
    ```
    >>> print (features)
    [[0 44.0 72000.0]
     [2 27.0 48000.0]
     [1 30.0 54000.0]
     [2 38.0 61000.0]
     [1 40.0 63777.77777777778]
     [0 35.0 58000.0]
     [2 38.77777777777778 52000.0]
     [0 48.0 79000.0]
     [1 50.0 83000.0]
     [0 37.0 67000.0]]

    >>> print(result)
    [0 1 0 0 1 1 0 1 0 1]
    ```

+ **Data Normalization**  
    Optional interesting processing that is done on the feature for `Country`, the data is encoded into a unique binary form. Thus `Spain` becomes `001`, `Germany` becomes `010`, and `France` becomes `100` called as **OneHotEncoding**. This is to avoid any confusions leading to wrong assumptions like `Spain` < `Germany` < `France`, and would only make sense in the use cases where there is feature like temperature or grades or some related comparison between the values of the feature.  
  
  We use the same library here for the data processing. 
    > Code  
    ```
    from sklearn.preprocessing import OneHotEncoder
    onehotencoder = OneHotEncoder(categorical_features = [0])
    features = onehotencoder.fit_transform(features).toarray()
    ```
    > Output
    ```
    >>> print (features)
    [[1.00000000e+00 0.00000000e+00 0.00000000e+00 4.40000000e+01 7.20000000e+04]
     [0.00000000e+00 0.00000000e+00 1.00000000e+00 2.70000000e+01 4.80000000e+04]
     [0.00000000e+00 1.00000000e+00 0.00000000e+00 3.00000000e+01 5.40000000e+04]
     [0.00000000e+00 0.00000000e+00 1.00000000e+00 3.80000000e+01 6.10000000e+04]
     [0.00000000e+00 1.00000000e+00 0.00000000e+00 4.00000000e+01 6.37777778e+04]
     [1.00000000e+00 0.00000000e+00 0.00000000e+00 3.50000000e+01 5.80000000e+04]
     [0.00000000e+00 0.00000000e+00 1.00000000e+00 3.87777778e+01 5.20000000e+04]
     [1.00000000e+00 0.00000000e+00 0.00000000e+00 4.80000000e+01 7.90000000e+04]
     [0.00000000e+00 1.00000000e+00 0.00000000e+00 5.00000000e+01 8.30000000e+04]
     [1.00000000e+00 0.00000000e+00 0.00000000e+00 3.70000000e+01 6.70000000e+04]]
    ```  
+ **Train to test data Split**  
  When we are training our model we also need some data for a to test so that we can check how the model is performing with the result predictions.  
  We normally can have `70:30` split for the `Training Data : Test Data`.or even less training data percentage but `never greater than 35%`  
    > Code  
    ```
    from sklearn.model_selection import train_test_split
    features_train, features_test, results_train, results_test = train_test_split(features, result, test_size = 0.2, random_state = 0)
    ```  
    > Output  
    ```
    >>> print (features_train)
    [[0.00000000e+00 1.00000000e+00 0.00000000e+00 4.00000000e+01 6.37777778e+04]
     [1.00000000e+00 0.00000000e+00 0.00000000e+00 3.70000000e+01 6.70000000e+04]
     [0.00000000e+00 0.00000000e+00 1.00000000e+00 2.70000000e+01 4.80000000e+04]
     [0.00000000e+00 0.00000000e+00 1.00000000e+00 3.87777778e+01 5.20000000e+04]
     [1.00000000e+00 0.00000000e+00 0.00000000e+00 4.80000000e+01 7.90000000e+04]
     [0.00000000e+00 0.00000000e+00 1.00000000e+00 3.80000000e+01 6.10000000e+04]
     [1.00000000e+00 0.00000000e+00 0.00000000e+00 4.40000000e+01 7.20000000e+04]
     [1.00000000e+00 0.00000000e+00 0.00000000e+00 3.50000000e+01 5.80000000e+04]]
    
    >>> print(features_test)
    [[0.0e+00 1.0e+00 0.0e+00 3.0e+01 5.4e+04]
     [0.0e+00 1.0e+00 0.0e+00 5.0e+01 8.3e+04]]
    
    >>> print(results_train)
    [1 1 1 0 1 0 0 1]
    
    >>> print (results_test)
    [0 0]
    ```  
+ **Feature Scaling**  
  Again an optional but important step in data preprocessing where we try to normalize the range of data into a finite space such as between `-1` to `+1`, or may be in percentages. The idea here is to have a `Euclidean distance` on the same scale between the feature sets.

  ![euclideanDistanceImage][]  

  This helps the algorithms and models to converge much faster then using the regular values.  
  This is achieved using the same library. Note That the output or the results do not need to be scaled as they are already between the finite range of 1 or 0  
  > Code  
  ```
  from sklearn.preprocessing import StandardScaler
  standardScaler_features = StandardScaler()
  features_train = standardScaler_features.fit_transform(features_train)
  features_test = standardScaler_features.transform(features_test)
  ```
  > Output
  ```
  >>> print(features_train)
  [[-1.          2.64575131 -0.77459667  0.26306757  0.12381479]
  [ 1.         -0.37796447 -0.77459667 -0.25350148  0.46175632]
  [-1.         -0.37796447  1.29099445 -1.97539832 -1.53093341]
  [-1.         -0.37796447  1.29099445  0.05261351 -1.11141978]
  [ 1.         -0.37796447 -0.77459667  1.64058505  1.7202972 ]
  [-1.         -0.37796447  1.29099445 -0.0813118  -0.16751412]
  [ 1.         -0.37796447 -0.77459667  0.95182631  0.98614835]
  [ 1.         -0.37796447 -0.77459667 -0.59788085 -0.48214934]]

  >>> print(features_test)
  [[-1.          2.64575131 -0.77459667 -1.45882927 -0.90166297]
  [-1.          2.64575131 -0.77459667  1.98496442  2.13981082]]
  ```  

## Summary  
Data pre-processing is required for the input data set to **clean the missing data, standardize and normalize** it, before it can be spilt into a **Training** and **Test** sets for the model.  
The entire python code is here for a quick reference  
> [Code][]
```
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('../datasets/Data.csv')
features = dataset.iloc[:, :-1].values
result = dataset.iloc[:, 3].values

# Handling missing data
from sklearn.preprocessing import Imputer
imputer = Imputer(missing_values='NaN', strategy='mean', axis=0)
features[:, 1:3] = imputer.fit_transform(features[:, 1:3])

# Feature Encoding
from sklearn.preprocessing import LabelEncoder
labelencoder_features = LabelEncoder()
features[:, 0] = labelencoder_features.fit_transform(features[:, 0])
# Result Encoding
labelencoder_results = LabelEncoder()
result = labelencoder_results.fit_transform(result)

# Normalizing the features
from sklearn.preprocessing import OneHotEncoder
onehotencoder = OneHotEncoder(categorical_features = [0])
features = onehotencoder.fit_transform(features).toarray()

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
features_train, features_test, results_train, results_test = train_test_split(features, result, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
standardScaler_features = StandardScaler()
features_train = standardScaler_features.fit_transform(features_train)
features_test = standardScaler_features.transform(features_test)
# Not required as there is only one column of data in the form of 1 and 0
# standardScaler_results = StandardScaler()
# results_train = standardScaler_results.fit_transform(results_train)

```

This has resulted the data to be processed **from**  
<table>
   <tr><th> Country</th><th>Age</th><th>Salary</th><th>Purchased</th></tr>
   <tr><td> France</td><td>44</td><td>72000</td><td>No</td></tr>
   <tr><td> Spain</td><td>27</td><td>48000</td><td>Yes</td></tr>
   <tr><td> Germany</td><td>30</td><td>54000</td><td>No</td></tr>
   <tr><td> Spain</td><td>38</td><td>61000</td><td>No</td></tr>
   <tr><td> Germany</td><td>40</td><td></td><td>Yes</td></tr>
   <tr><td> France</td><td>35</td><td>58000</td><td>Yes</td></tr>
   <tr><td> Spain</td><td></td><td>52000</td><td>No</td></tr>
   <tr><td> France</td><td>48</td><td>79000</td><td>Yes</td></tr>
   <tr><td> Germany</td><td>50</td><td>83000</td><td>No</td></tr>
   <tr><td> France</td><td>37</td><td>67000</td><td>Yes</td></tr>
</table>  
  

**to**  

<table>
  <tr><th>Country</th><th>Age</th><th>Salary</th><th>Purchased</th></tr>
  <tr><td>-1.0  2.64575131 -0.77459667</td><td> 0.26306757</td><td> 0.12381479</td><td>1</td></tr>
  <tr><td> 1.0 -0.37796447 -0.77459667</td><td>-0.25350148</td><td> 0.46175632</td><td>1</td></tr>
  <tr><td>-1.0 -0.37796447  1.29099445</td><td>-1.97539832</td><td>-1.53093341</td><td>1</td></tr>
  <tr><td>-1.0 -0.37796447  1.29099445</td><td> 0.05261351</td><td>-1.11141978</td><td>0</td></tr>
  <tr><td> 1.0 -0.37796447 -0.77459667</td><td> 1.64058505</td><td> 1.7202972</td><td>1</td></tr>
  <tr><td>-1.0 -0.37796447  1.29099445</td><td>-0.0813118</td><td>-0.16751412</td><td>0</td></tr>
  <tr><td> 1.0 -0.37796447 -0.77459667</td><td> 0.95182631</td><td> 0.98614835</td><td>0</td></tr>
  <tr><td> 1.0 -0.37796447 -0.77459667</td><td>-0.59788085</td><td>-0.48214934</td><td>1</td></tr>
  <tr><td>-1.0  2.64575131 -0.77459667</td><td>-1.45882927</td><td>-0.90166297</td><td>0</td></tr>
  <tr><td>-1.0  2.64575131 -0.77459667</td><td> 1.98496442</td><td> 2.13981082</td><td>0</td></tr>
</table>  

[Development Environment Setup]: ../System%20Setup/Development%20Environment.md
[Pandas]:https://pandas.pydata.org/
[Mean]:https://en.wikipedia.org/wiki/Mean
[Standard Deviation]:https://en.wikipedia.org/wiki/Standard_deviation
[Code]:../code/preprocessor.py
[euclideanDistanceImage]:../../images/euclidean%20Distance.png