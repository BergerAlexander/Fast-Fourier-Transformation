# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 13:31:16 2018

@author: alexa
"""

# importting numpy and pandas
import pandas as pd
import numpy as np

# import data and preprocessing
training_data1 = pd.read_csv('C:/Users/alexa/Desktop/M5/ML/Points_us1.csv')
training_data1 = training_data1.drop(training_data1.columns[0], axis = 1)
training_data2 = pd.read_csv('C:/Users/alexa/Desktop/M5/ML/Points_us2.csv')
training_data2 = training_data2.drop(training_data2.columns[0], axis = 1)
training_data3 = pd.read_csv('C:/Users/alexa/Desktop/M5/ML/Points_us3.csv')
training_data3 = training_data3.drop(training_data3.columns[0], axis = 1)
training_data4 = pd.read_csv('C:/Users/alexa/Desktop/M5/ML/Points_us137.csv')
training_data4 = training_data4.drop(training_data4.columns[0], axis = 1)
training_data5 = pd.read_csv('C:/Users/alexa/Desktop/M5/ML/Points_us158.csv')
training_data5 = training_data5.drop(training_data5.columns[0], axis = 1)

frames = [training_data1, training_data2, training_data3, training_data4, training_data5]
X = pd.concat(frames)
X = X.drop(X.columns[4], axis = 1)
X = X.rename(index=str, columns={"lag X[mm]": "lag",
                                 "speed X[mm/s]": "speed",
                                 "accel X[mm/ss]": "accel", 
                                 "DAC X[V]": "DAC"})

# create labels:
# training_data1, training_data2 and training_data3 are sensor data when 
# machine runs in normal operation mode (labeled with 0)
# training_data4 and training_data5 data with changed parametrs which influence machine 
# behavior when running (labeled with 1)
label1 = pd.DataFrame(np.zeros((training_data1.shape[0], 1)))
label2 = pd.DataFrame(np.zeros((training_data2.shape[0], 1)))
label3 = pd.DataFrame(np.zeros((training_data3.shape[0], 1)))
label4 = pd.DataFrame(np.ones((training_data4.shape[0], 1)))
label5 = pd.DataFrame(np.ones((training_data5.shape[0], 1)))

labels = [label1, label2, label3, label4, label5]
y = pd.concat(labels)

# data scaling and training with Random Forest 
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler() 
scaled_values = scaler.fit_transform(X) 
X.loc[:,:] = scaled_values

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

from sklearn.ensemble import RandomForestClassifier

random_forest = RandomForestClassifier(n_estimators=100, max_depth=10)
random_forest.fit(X_train, y_train.values.ravel()
)

# model evaluation

print(random_forest.score(X_train, y_train))
print(random_forest.score(X_test, y_test))












