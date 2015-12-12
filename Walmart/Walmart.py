
"""
TripType - a categorical id representing the type of shopping trip the customer made. This is the ground truth that you are predicting. TripType_999 is an "other" category.
VisitNumber - an id corresponding to a single trip by a single customer
Weekday - the weekday of the trip
Upc - the UPC number of the product purchased
ScanCount - the number of the given item that was purchased. A negative value indicates a product return.
DepartmentDescription - a high-level description of the item's department
FinelineNumber - a more refined category for each of the products, created by Walmart
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Some Basic Analysis

train_data = pd.read_csv("train.csv")

train_data.info() 
#Missing Values from 'UPC', 'DepartmentDescription', 'FinelineNumber'

train_data['Weekday'].value_counts().plot(kind='bar') # Saturday and Sunday


#Remove all NA Values for Analysis
train_clean = train_data.dropna()






