%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVC
from sklearn import preprocessing


train = pd.read_csv("train.csv", parse_dates = ['Original_Quote_Date'])
test = pd.read_csv("train.csv", parse_dates = ['Original_Quote_Date'])

train_Y = train.QuoteConversion_Flag.values


def process_data(data):

    data['year'] = data['Original_Quote_Date'].apply(lambda x: x.year)
    data['month'] = data['Original_Quote_Date'].apply(lambda x: x.month)
    data['day'] = data['Original_Quote_Date'].apply(lambda x: x.day)
    data['wkofyr'] = data['Original_Quote_Date'].apply(lambda x: x.weekofyear)
    
    data = data.drop(['Original_Quote_Date','QuoteNumber','QuoteConversion_Flag'], axis=1)

    return data


train_X = process_data(train)
test_X = process_data(test)


for f in train.columns:
    if train[f].dtype=='object':
        print(f)
        lbl = preprocessing.LabelEncoder()
        lbl.fit(list(train_X[f].values) + list(test_X[f].values))
        train_X[f] = lbl.transform(list(train_X[f].values))
        test_X[f] = lbl.transform(list(test_X[f].values))






