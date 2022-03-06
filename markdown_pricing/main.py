#!/usr/bin/env python

"""main.py: Main"""

__author__ = "Jidhu Mohan"
__copyright__ = "Copyright (C) 2022 Factory-AI project"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jidhu Mohan"
__email__ = "Jidhu.Mohan@gmail.com"
__status__ = "PoV" 

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
from data import DATA
from preprocess import data_preprocess as dp
from forecast import SALES
from bayesian_opt import OPT

file_path = "data/data_pre_processed.csv"

def get_data():
    Data = DATA()
    Data.get_data()
    Data.get_new_featuers()
    Data.merge_features()

def objective(**args2):
        data["Selling_Price"] = args2["Selling_Price"]
        pred = Sales.model.predict(data.values)
        obj = - ( max(pred[0] - max((np.array(data["Total_Inventory"])*0.06) - pred[0], 0), 0)) + 0.1*np.std(pred[0])
        return obj

bounds = {'Selling_Price':(1900,3900)}

if __name__=="__main__":

    get_data()
    dp()
    df_train = pd.read_csv(file_path)
    print(df_train.head())
    print(df_train.tail())
    print(df_train.info())
    print(df_train.describe())

    Sales = SALES()
    Sales.build()

    data = df_train.iloc[10:11,:-1]

    Opt = OPT(objective_fun=objective, bounds=bounds,verbose=2)
    Opt.run(n_iter=10)

    result = dict()
    selected_points = np.random.randint(2000, size=10)
    for i in selected_points:
        data = df_train.iloc[i:i+1,:-1]
        Opt = OPT(objective_fun=objective, bounds=bounds,verbose=2)
        Opt.run(n_iter=10)

        result[i] = Opt.optimizer.max
    print(result)