## Shopping Kaggle Competition

from pandas import DataFrame,Series
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

train = pd.read_csv("train.csv",parse_dates ='offerdate')
offers = pd.read_csv('offers.csv')

x = pd.merge(train,offers)

--How many Repeaters
-- f    116619
-- t     43438
x.repeater.value_counts()

--
