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