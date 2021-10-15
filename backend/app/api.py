from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import dill as pickle

app = FastAPI()

origins=[
    "http://localhost:3000",
    'localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#import pickled files
filename = './pickled/model_v1.pk'
with open(filename ,'rb') as f:
    loaded_model = pickle.load(f)

filename = './pickled/sorted_arrays.pk'
with open(filename ,'rb') as f:
    sorted_arrays = pickle.load(f)
    
filename = './pickled/feature_arrays.pk'
with open(filename ,'rb') as f:
    feature_arrays = pickle.load(f)

#initialize objects from pickled files

#sorted arrays
properties = sorted_arrays[0]
neighbs = sorted_arrays[1]
rooms = sorted_arrays[2]
bors = sorted_arrays[3]

#sorted arrays
properties = sorted_arrays[0]
neighbs = sorted_arrays[1]
rooms = sorted_arrays[2]
bors = sorted_arrays[3]

#feature arrays
property_types = feature_arrays[0]
neighborhoods = feature_arrays[1]
boroughs = feature_arrays[2]
room_types = feature_arrays[3]

#define functions

def set_property(prop_in):
    props = np.searchsorted(properties, prop_in)

    if props != 0:
        for i in range(10):
            property_types[i][props-1] = 1
        
def set_neighborhood(neighb_in):
    neighb = np.searchsorted(neighbs, neighb_in)

    if neighb != 0:
        for i in range(10):
            neighborhoods[i][neighb-1] = 1
        
def set_borough(borough_in):
    bor = np.searchsorted(bors, borough_in)

    if bor != 0:
        for i in range(10):
            boroughs[i][bor-1] = 1

def set_room(room_in):
    room = np.searchsorted(rooms, room_in)

    if room != 0:
        for i in range(10):
            room_types[i][room-1] = 1

def build_numerical(beds_in, accom_in):
    array = np.zeros((10,4))
    for i in range(10):
        array[i][3] = int(accom_in) #accomodates
        array[i][2] = int(beds_in) #num of beds
        array[i][1] = (np.random.rand() * 2) + 3 #rating - generate a number between 3 and 5
        array[i][0] = np.random.randint(1, 454) #num of reviews, generate number between 1 and max # of reviews
    return array

class PredictionRequest(BaseModel):
    prop_type: str
    neighborhood: str
    borough: str
    room_type: str
    num_rooms: int
    num_accom: int

@app.get('/')
def read_root():
    return {"message":"Welcome to Fair Fare Finder"}

@app.post('/predict')
def predict_fare(
    data: PredictionRequest,
) -> Any:
    set_property(data.prop_type)
    set_neighborhood(data.neighborhood)
    set_borough(data.borough)
    set_room(data.room_type)
    numerical = build_numerical(data.num_rooms, data.num_accom)

    features = np.concatenate((numerical, room_types, boroughs, neighborhoods, property_types), 1)
    y_pred = loaded_model.predict(features)
    average = np.mean(y_pred).round(0)
    return {'predicted': average}

