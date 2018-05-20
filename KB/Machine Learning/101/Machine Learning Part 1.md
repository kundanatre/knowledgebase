# Machine Learning 101

## Prerequisites
Install the Python and Anaconda environment as described in the [Development Environment Setup][] Page.

## Data Preparation - Data Preprocessing
Training a Model needs Data, Data needs to be valid, Validation requires preprocessing.

Steps involved in data preprocessing are normally the same which include the following:
+ Load the data so that it can be processed. This is achieved using the library `pandas`
```
import pandas as pd
dataset = pd.read_csv('Data.csv')
```

[Development Environment Setup]:../System%20Setup/Development%20Environment.md
[Pandas]:https://pandas.pydata.org/
