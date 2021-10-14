import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.pipeline import make_pipeline
import dill as pickle

july = pd.read_csv('./data/tomslee_airbnb_new_york_1438_2017-07-12.csv')
july = july.drop(['room_id','survey_id', 'host_id', 'country', 'city', 'bathrooms', 'minstay', 'last_modified', 'location', 'name', 'latitude', 'longitude'], 1)
#remove listings we already know are outliers (price greater than 500 and rooms at 50)
july = july[(july.price < 500) & (july.bedrooms < 50) & (july.overall_satisfaction >= 3)]
#july.head()

#clean up place types
prop_dict = {}
for prop_type in july.property_type.unique():
    prop_dict[prop_type] = 'Other'

prop_dict['Apartment'] = 'Apartment'
prop_dict['Bed & Breakfast'] = 'Bed & Breakfast'
prop_dict['Serviced Apartment'] = 'Apartment'
prop_dict['Casa particular'] = 'Bed & Breakfast'
prop_dict['Loft'] = 'Loft'
prop_dict['Townhouse'] = 'Townhouse'
prop_dict['Condominium'] = 'Condominium'
prop_dict['House'] = 'House'

july.property_type.replace(prop_dict, inplace=True)

#setting up sorted arrays so position is easy to find
properties = np.sort(july.property_type.unique())
neighbs = np.sort(july.neighborhood.unique())
rooms = np.sort(july.room_type.unique())
bors = np.sort(july.borough.unique())

sorted_arrays = [properties, neighbs, rooms, bors]

#uncomment below to save to pickle
# filename = 'sorted_arrays.pk'
# with open(filename, 'wb') as file:
#    pickle.dump(sorted_arrays, file)

#setting up arrays that will be put together at the end to make X for prediction
property_types = np.zeros((10, len(july.property_type.unique())-1))
neighborhoods = np.zeros((10, len(july.neighborhood.unique())-1))
boroughs = np.zeros((10, len(july.borough.unique())-1))
room_types = np.zeros((10, len(july.room_type.unique())-1))

feature_arrays = [property_types, neighborhoods, boroughs, room_types]

#uncomment below to save to pickle
# filename = 'feature_arrays.pk'
# with open(filename, 'wb') as file:
#     pickle.dump(feature_arrays, file)

july = july[july.overall_satisfaction >= 3]
july_y = july.price
july_dumb = july.drop('price',1)
july_x = pd.get_dummies(july_dumb, drop_first=True)

# Split the data into a training and test set.
Xlr, Xtestlr, ylr, ytestlr = train_test_split(july_x, july_y, test_size=.3, random_state=50)

scaler = preprocessing.StandardScaler()
#X_train = scaler.fit_transform(Xlr)

elnet = ElasticNet()

pipe = make_pipeline(scaler, elnet)

# Fit the model on the trainng data.
pipe.fit(Xlr, ylr)

#save to pickle
filename = './pickled/model_v1.pk'

with open(filename, 'wb') as file:
    pickle.dump(pipe, file)