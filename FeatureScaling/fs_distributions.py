# -*- coding: utf-8 -*-
"""
Feature Scaling - Effectively Choose Input Variables Based on Distributions
"""
# Reading the dataset
import pandas as pd
import numpy as np
import os

path  = os.path.abspath("Data/Indian_Diabetes/Pima Indian Diabetes.csv")
data = pd.read_csv(path)
data.head()
data.columns

# Aplying Standardization to all features
from sklearn.preprocessing import StandardScaler

Y = data.Outcome
X = data.drop("Outcome", axis = 1)
columns = X.columns
scaler = StandardScaler()
X_std = scaler.fit_transform(X)
X_std = pd.DataFrame(X_std, columns = columns)
X_std.head()

# Train and Test split of the features
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X_std, Y, 
                                                    test_size = 0.15, 
                                                    random_state = 45)

#Building Logistic Regression model on the Standardized variables
from sklearn.linear_model import LogisticRegression

lr_std = LogisticRegression()
lr_std.fit(x_train, y_train)
y_pred = lr_std.predict(x_test)
print('Accuracy of logistic regression on test set with standardized features: {:.2f}'
      .format(lr_std.score(x_test, y_test)))

from sklearn.preprocessing import MinMaxScaler
norm = MinMaxScaler()
X_norm = norm.fit_transform(X)
X_norm = pd.DataFrame(X_norm, columns = columns)
X_norm.head()

# Train and Test split of Normalized features
from sklearn.model_selection import train_test_split
x1_train, x1_test, y1_train, y1_test = train_test_split(X_norm, Y, 
                                                        test_size = 0.15, 
                                                        random_state = 45)

#Building Logistic Regression model on the Normalized variables
from sklearn.linear_model import LogisticRegression
lr_norm = LogisticRegression()
lr_norm.fit(x1_train, y1_train)
y_pred = lr_norm.predict(x1_test)
print('Accuracy of logistic regression on test set with Normalized features: {:.2f}'
      .format(lr_norm.score(x1_test, y1_test)))

# Plotting the histograms of each variable
from matplotlib import pyplot
data.hist(alpha=0.5, figsize=(10, 10))
pyplot.show()

#Initializing Gaussian and Non-Gaussian features based on distributions
# Standardizing - Gaussian Distribution features
# Normalizing - Non-Gaussian Distribution features
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
Standardize_Var = ['BMI','BloodPressure', 'Glucose']
Standardize_transformer = Pipeline(steps=[('standard', StandardScaler())])
Normalize_Var = ['Age','DiabetesPedigreeFunction','Insulin','Pregnancies','SkinThickness']
Normalize_transformer = Pipeline(steps=[('norm', MinMaxScaler())])

x2_train, x2_test, y2_train, y2_test = train_test_split(X, Y, test_size=0.2)
preprocessor = ColumnTransformer(transformers=
        [('standard', Standardize_transformer, Standardize_Var),
        ('norm', Normalize_transformer, Normalize_Var)])

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LogisticRegression(solver='lbfgs'))])
clf.fit(x2_train, y2_train)
print('Accuracy of Logistic Regression model after standardizing Gaussian distributed features and normalizing Non-Gaussian distributed features: {:.2f}'.format(clf.score(x2_test, y2_test)))

