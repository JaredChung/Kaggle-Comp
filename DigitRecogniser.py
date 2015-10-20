from pandas import DataFrame,Series
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

train_data = train.values
test_data = test.values

forest = RandomForestClassifier()
forest = forest.fit(train_data[:,1:],train_data[:,0]

output = forest.predict(test).astype(int)


d = DataFrame(output)
d.to_csv("Submission.csv")



