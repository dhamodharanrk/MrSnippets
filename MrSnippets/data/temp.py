__author__ = 'dhamodharan.k'
import pickle
import pandas as pd

df = pd.read_excel('Book1.xlsx')
with open('cities.pickle', 'wb') as f:
    pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)


import pickle

with open('cities.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    data = pickle.load(f)
    print(data)