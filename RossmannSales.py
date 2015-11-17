"""
Id - an Id that represents a (Store, Date) duple within the test set
Store - a unique Id for each store
Sales - the turnover for any given day (this is what you are predicting)
Customers - the number of customers on a given day
Open - an indicator for whether the store was open: 0 = closed, 1 = open
StateHoliday - indicates a state holiday. Normally all stores, with few exceptions, are closed on state holidays. Note that all schools are closed on public holidays and weekends. a = public holiday, b = Easter holiday, c = Christmas, 0 = None
SchoolHoliday - indicates if the (Store, Date) was affected by the closure of public schools
StoreType - differentiates between 4 different store models: a, b, c, d
Assortment - describes an assortment level: a = basic, b = extra, c = extended
CompetitionDistance - distance in meters to the nearest competitor store
CompetitionOpenSince[Month/Year] - gives the approximate year and month of the time the nearest competitor was opened
Promo - indicates whether a store is running a promo on that day
Promo2 - Promo2 is a continuing and consecutive promotion for some stores: 0 = store is not participating, 1 = store is participating
Promo2Since[Year/Week] - describes the year and calendar week when the store started participating in Promo2
PromoInterval - describes the consecutive intervals Promo2 is started, naming the months the promotion is started anew. E.g. "Feb,May,Aug,Nov" means each round starts in February, May, August, November of any given year for that store
"""

%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor


train = pd.read_csv("train.csv", parse_dates = ['Date'])
store = pd.read_csv("store.csv")
test = pd.read_csv("test.csv", parse_dates = ['Date'])


#Unique Store Count 1115
len(train.Store.unique())
len(store.Store.unique())

def clean_data(data)
    
    data = pd.merge(data,store, left_on='Store',right_on = 'Store',how='left')
    data = data[data.Sales > 0] # Remove $0 Sales
    data.loc[data.Open.isnull(),'Open'] = 0
    #add extra date columns
    data = data[data.Sales > 0] # remove sales of $0
    data['month'] = data.Date.apply(Lambda x: x.month)
    data['day'] = data.Date.apply(Lambda x: x.day)
    data['year'] = data.Date.apply(Lambda x: x.year)
    data['wkofyr'] = data.Date.apply(Lambda x: x.weekofyear)
    data.drop(['Date'], axis = 1, inplace= True)
    
    # Calculate time competition open time in months
    data['CompetitionOpen'] = 12 * (data.year - data.CompetitionOpenSinceYear) + \
	  (data.month - data.CompetitionOpenSinceMonth)
    data['CompetitionOpen'] = data.CompetitionOpen.apply(lambda x: x if x > 0 else 0)
    data.drop(['CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear'], axis = 1, 
	         inplace = True)
	
	# Promo open time in months
	data['PromoOpen'] = 12 * (data.year - data.Promo2SinceYear) + \
	(data.woy - data.Promo2SinceWeek) / float(4)
	data['PromoOpen'] = data.CompetitionOpen.apply(lambda x: x if x > 0 else 0)
	data.drop(['Promo2SinceYear', 'Promo2SinceWeek'], axis = 1, 
	         inplace = True)

	# Get promo months
	data['p_1'] = data.PromoInterval.apply(lambda x: x[:3] if type(x) == str else 0)
	data['p_2'] = data.PromoInterval.apply(lambda x: x[4:7] if type(x) == str else 0)
	data['p_3'] = data.PromoInterval.apply(lambda x: x[8:11] if type(x) == str else 0)
	data['p_4'] = data.PromoInterval.apply(lambda x: x[12:15] if type(x) == str else 0)
	
	#Get Dummies for Categorical         
	data = pd.get_dummies(data, columns = ['p_1', 'p_2', 'p_3', 'p_4', 
	                                       'StateHoliday' , 
	                                       'StoreType', 
	                                       'Assortment'])
  	data.drop(['Store',
	           'PromoInterval', 
	           'p_1_0', 'p_2_0', 'p_3_0', 'p_4_0', 
	           'StateHoliday_0', 
	           'year'], axis=1,inplace=True)


	# Fill in missing values
	data = data.fillna(0)
	data = data.sort_index(axis=1)

	return data


data = train[train['Open'] != 0]

# Process training data
data = clean_data(data)
print('training data processed')

# Set up training data
X_train = data.drop(['Sales', 'Customers'], axis = 1)
y_train = data.Sales

# Fit random forest model
rf = RandomForestRegressor(n_jobs = -1, n_estimators = 100)
rf.fit(X_train, y_train)
print('model fit')

# Process test data
test = clean_data(test)

# Ensure same columns in test data as training
for col in data.columns:
    if col not in test.columns:
        test[col] = np.zeros(test.shape[0])
        
test = test.sort_index(axis=1).set_index('Id')
print('test data loaded and processed')

# Make predictions
X_test = test.drop(['Sales', 'Customers'], axis=1).values
y_test = rf.predict(X_test)

# Make Submission
result = pd.DataFrame({'Id': test.index.values, 'Sales': y_test}).set_index('Id')
result = result.sort_index()
result.to_csv('submission.csv')
print('submission created')



