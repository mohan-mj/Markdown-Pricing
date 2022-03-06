#!/usr/bin/env python

"""forecast.py: Sales forecast"""

__author__ = "Jidhu Mohan"
__copyright__ = "Copyright (C) 2022 Factory-AI project"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jidhu Mohan"
__email__ = "Jidhu.Mohan@gmail.com"
__status__ = "PoV"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor as RFR


class SALES:

    def __init__(self):
        self.df_train = pd.read_csv("data/data_pre_processed.csv")
        # self.df_test = pd.read_csv("data/test_with_feature_final.csv")
        self.model = RFR(n_estimators=100)

    def pre_process(self):
        features_drop = ['Unnamed: 0', 'CPI','Unemployment','Fuel_Price', 'Date', 'Store',\
                        'MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']

        self.df_train.drop(features_drop, axis=1, inplace=True)
        # self.df_test.drop(features_drop, axis=1, inplace=True)

        # rename
        self.df_train.rename(columns={}, inplace=True)
    
    def split(self):
        # self.pre_process(); print("Data pre-processing Successful..")
        self.train_X = self.df_train.iloc[:,:].drop(['Demand'], axis=1).values
        self.train_y = self.df_train.iloc[:,:]['Demand'].values

        self.test_X = self.df_train.iloc[9000:,:].drop(['Demand'], axis=1).values
        self.test_y = self.df_train.iloc[9000:,:]['Demand'].values

        # self.test_y = self.df_train[:,'Weekly_Sales'].values
        # self.test_X = self.df_test.values

        self.train_X.shape, self.train_y.shape, self.test_X.shape, self.test_y.shape
    
    def corr(self):
        corr = self.df_train.corr()
        plt.figure(figsize=(15, 10))
        sns.heatmap(corr, annot=True)
        plt.show()

    def build(self):
        self.split(); print("Data Splitting Successful..")
        # self.corr()
        self.model.fit(self.train_X, self.train_y); print("Model training started..")
        y_pred = self.model.predict(self.test_X); print("Model training successful..")
        acc = round(self.model.score(self.train_X, self.train_y) * 100,2)
        print (f"Accuracy: {acc} %")

if __name__=="__main__":
    Sales = SALES()
    Sales.build()