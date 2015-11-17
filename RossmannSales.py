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
test = pd.read_csv("test.csv")


#Unique Store Count 1115
len(train.Store.unique())
len(store.Store.unique())

#Merge store information
train_store = pd.merge(train,store, left_on='Store',right_on = 'Store',how='left')

def clean_data(data)
    
    data = data[data.Sales > 0] # Remove $0 Sales
    #add extra date columns
    data = data[data.Sales > 0] # remove sales of $0
    data['Month'] = data.Date.apply(Lambda x: x.month)
    data['Day'] = data.Date.apply(Lambda x: x.day)
    data['Year'] = data.Date.apply(Lambda x: x.year)
    data['Wkofyr'] = data.Date.apply(Lambda x: x.weekofyear)
    data.drop(['Date'], axis = 1, inplace= True)
    
    # Calculate time competition open time in months
	  data['CompetitionOpen'] = 12 * (data.year - data.CompetitionOpenSinceYear) + \
	  (data.month - data.CompetitionOpenSinceMonth)
	  data['CompetitionOpen'] = data.CompetitionOpen.apply(lambda x: x if x > 0 else 0)
  	data.drop(['CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear'], axis = 1, 
	         inplace = True)
	         
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


#clean test data
test.loc[test.Open.isnull(),'Open'] = 1



