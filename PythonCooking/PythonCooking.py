###Kaggle Competition - Cooking

import json
from pandas import DataFrame
from collections import OrderedDict
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

#### Load the Json data into Variables
with open('train.json') as train_f, open('test.json') as test_f:
    train_data = json.load(train_f)
    test_data = json.load(test_f)

### Cleaning the Data	
train_X = [' '.join(e['ingredients']) for e in train_data]
train_Y = [e['cuisine'] for e in train_data]
test_X = [' '.join(e['ingredients']) for e in test_data]
test_id = [e['id'] for e in test_data]


### Transforming the Data
le = LabelEncoder() ### Create Variable for the encoder
ngram_vectorizer = CountVectorizer() ### Create Variable for the CountVectorizer()
train_Y = le.fit_transform(train_Y) ### Transform 'cuisine' data into Numerical Labels
train_X = ngram_vectorizer.fit_transform(train_X).toarray() ### Transform Train_X 'ingredients' into an array
test_X = ngram_vectorizer.transform(test_X).toarray() ### Transform Train_X 'ingredients' into an array


#### Applying Randomforest
rf_classifier = RandomForestClassifier() ### Create Variable for the RandomForest
rf_classifier.fit(train_X, train_Y) ### (

test_Y = rf_classifier.predict(test_X) #### Predict Using Test_X Data
test_Y = le.inverse_transform(test_Y) #### Turn the Data Back into Categorical

d = DataFrame(data=OrderedDict([('id', test_id), ('cuisine', test_Y)])) #### Create Dataframe of data
d.to_csv('submission.csv', index=False)
