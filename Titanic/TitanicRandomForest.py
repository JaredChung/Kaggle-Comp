
from pandas import DataFrame,Series
import pandas as pd
import numpy as np
from collections import OrderedDict
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm

# Data cleanup
# TRAIN DATA
train_data = pd.read_csv('train.csv', header=0)        # Load the train file into a dataframe

# female = 0, Male = 1
train_data[train_data.Gender == 'female'] = 0
train_data[train_data.Gender == 'male'] = 1

train_data['Gender'] = train_data['Sex'].map( {'female': 0, 'male': 1} ).astype(int)

# Fill in missing Age with the Average
train_data.loc[train_data.Age.isnull(),'Age'] = np.average(train_data.loc[train_data.Age.notnull()].Age)


# Embarked from 'C', 'Q', 'S'
# Note this is not ideal: in translating categories to numbers, Port "2" is not 2 times greater than Port "1", etc.

# All missing Embarked -> just make them embark from most common place
if len(train_data.Embarked[ train_data.Embarked.isnull() ]) > 0:
    train_data.loc[ train_data.Embarked.isnull(),'Embarked'] = train_data.Embarked.dropna().mode().values

Ports = list(enumerate((train_data['Embarked']).unique()))    # determine all values of Embarked,
Ports_dict = { name : i for i, name in Ports }              # set up a dictionary in the form  Ports : index
train_data.Embarked = train_data.Embarked.map( lambda x: Ports_dict[x]).astype(int)     # Convert all Embark strings to int

# Remove the Name column, Cabin, Ticket, and Sex (since I copied and filled it to Gender)
train_data = train_data.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'PassengerId'], axis=1) 



# TEST DATA
test_data = pd.read_csv('test.csv', header=0)        # Load the test file into a dataframe

# I need to do the same with the test data now, so that the columns are the same as the training data
# I need to convert all strings to integer classifiers:
# female = 0, Male = 1
test_data['Gender'] = test_data['Sex'].map( {'female': 0, 'male': 1} ).astype(int)

# Embarked from 'C', 'Q', 'S'
# All missing Embarked -> just make them embark from most common place
if len(test_data.Embarked[ test_data.Embarked.isnull() ]) > 0:
    test_data.Embarked[ test_data.Embarked.isnull() ] = test_data.Embarked.dropna().mode().values
# Again convert all Embarked strings to int
test_data.Embarked = test_data.Embarked.map( lambda x: Ports_dict[x]).astype(int)

#Fill in missing Age with Average
test_data.loc[test_data.Age.isnull(),'Age'] = np.average(test_data.loc[test_data.Age.notnull(),'Age'])


#fill in missing Fare... Might need to change this
test_data.loc[test_data.Fare.isnull(),'Fare'] = np.average(test_data.loc[test_data.Fare.notnull(),'Fare'])

# Collect the test data's PassengerIds before dropping it
ids = test_data['PassengerId'].values
# Remove the Name column, Cabin, Ticket, and Sex (since I copied and filled it to Gender)
test_data = test_data.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'PassengerId'], axis=1) 


# The data is now ready to go. So lets fit to the train, then predict to the test!
# Convert back to a numpy array
train_data = train_data.values
test_data = test_data.values


print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( train_data[0::,1::], train_data[0::,0] )

print 'Predicting...'
output = forest.predict(test_data).astype(int)


d = DataFrame(data=OrderedDict([('PassengerId', ids), ('Survived', output)])) #### Create Dataframe of data
d.to_csv('submission.csv', index=False)
