__author__ = 'Dhamodharan Karuppuswamy'
import os
import pickle

current_path = os.getcwd()

def get_city_list():
    try:
        with open(current_path + "\\data\\cities.pickle",'rb') as f:
            cities_data = pickle.load(f)
            return list(cities_data.City)
    except: return []

def get_state_list():
    try:
        with open(current_path + "\\data\\cities.pickle",'rb') as f:
            cities_data = pickle.load(f)
            return list(set(cities_data.State))
    except: return []

def get_city_info_obj():
    try:
        with open(current_path + "\\data\\cities.pickle", 'rb') as f:
            cities_data = pickle.load(f)
            return cities_data
    except: return None


