

from pandas import DataFrame,Series
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

### Import Data
data = pd.read_csv('train.csv', parse_dates=['Dates'])

data['Year'] = data['Dates'].map(lambda x: x.year)
data['Week'] = data['Dates'].map(lambda x: x.week)
data['Hour'] = data['Dates'].map(lambda x: x.hour)

### Graph Categories 
data.Category.value_counts().order().plot(kind='bar')

### Graph PdDistricts 
data.PdDistrict.value_counts().order().plot(kind='bar')

data['event']=1
weekly_events =data[['Week','Year','event']].groupby(['Year','Week']).count().reset_index()
weekly_events_years = weekly_events.pivot(index='Week', columns='Year', values='event').fillna(method='ffill')
#%matplotlib inline
ax = weekly_events_years.interpolate().plot(title='number of cases every 2 weeks', figsize=(10,6))
plt.savefig('events_every_two_weeks.png')


hourly_events =data[['Hour','event']].groupby(['Hour']).count().reset_index()
hourly_events.plot(kind='bar', figsize=(6, 6))
plt.savefig('hourly_events.png')


hourly_district_events =data[['PdDistrict','Hour','event']].groupby(['PdDistrict','Hour']).count().reset_index()
hourly_district_events_pivot = hourly_district_events.pivot(index='Hour', columns='PdDistrict', values='event').fillna(method='ffill')
hourly_district_events_pivot.interpolate().plot(title='number of cases hourly by district', figsize=(10,6))
plt.savefig('hourly_events_by_district.png')



## Random Forest Example
X_tr = data
y_tr = data["Category"]
X_tr = X_tr.drop("Category", axis=1)

X_test = pd.read_csv('test.csv')

# transform vector of strings into matrix of bools
y_tr = pd.get_dummies(y_tr)

# fit classifier
clf = RandomForestClassifier(n_estimators=20)
clf.fit(X_tr, y_tr)

# make predictions, place in a data frame preserving indexing and columns
y_test = pd.DataFrame(clf.predict(X_test), index=X_test.index, columns=y_tr.columns)