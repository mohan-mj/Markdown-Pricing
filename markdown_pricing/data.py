
#!/usr/bin/env python

"""data.py: Get data"""

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


class DATA:
    
    def __init__(self):
        self.stores = pd.read_csv("data/stores.csv")
        self.train = pd.read_csv("data/train.csv")
        self.test = pd.read_csv("data/test.csv")
        self.features = pd.read_csv("data/features.csv")
    
    def get_data(self):
        # stores
        print(f"Shape of stores.csv: {self.stores.shape}")
        print("Types of stores:")
        print(self.stores['Type'].value_counts())

        def pie_plot():
            labels = 'store A','store B','store C'
            sizes = [(22/(45))*100,(17/(45))*100,(6/(45))*100]
            colors = ['gold', 'yellowgreen', 'lightcoral']
            explode = (0.1, 0, 0)  # explode 1st slice

            # Plot
            plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
            plt.legend(labels, loc="best")
            plt.axis('equal')
            plt.show()

        # train
        print(f"Shape of train.csv: {self.train.shape}")
        print(self.train.head())
        self.train.plot(kind='line', x='Dept', y='Weekly_Sales',fig=(7,15))
        # plt.show()

        # test
        print(f"Shape of test.csv: {self.test.shape}")
        print(self.test.head())

        # features
        print(f"Shape of features.csv: {self.features.shape}")
        print(self.features.head())


    def get_new_featuers(self):
        self.train['Date'] = pd.to_datetime(self.train['Date'])
        self.test['Date'] = pd.to_datetime(self.test['Date'])

        # add week feature
        self.train['Week'] = self.train['Date'].dt.week
        self.test['Week'] = self.test['Date'].dt.week

        # self.train['Day_of_week'] =self.train['Date'].dt.dayofweek
        # self.test['Day_of_week'] =self.test['Date'].dt.dayofweek

        # self.train['Month'] =self.train['Date'].dt.month 
        # self.test['Month'] =self.test['Date'].dt.month 

        # self.train['Year'] =self.train['Date'].dt.year
        # self.test['Year'] =self.test['Date'].dt.year

        # self.train['Day'] =self.train['Date'].dt.day 
        # self.test['Day'] =self.test['Date'].dt.day


    def merge_features(self):

        # split
        train_with_feature =  self.features.iloc[:,:]
        test_with_feature =  self.features.iloc[:,:]

        self.features['Date'] = pd.to_datetime(self.features['Date'])

        # merge train & features
        train_with_feature = pd.merge_asof(self.train, self.features, on='Store',by='Date')
        test_with_feature = pd.merge_asof(self.test, self.features, on='Store',by='Date')

        # merge with stores
        train_with_feature_new = pd.merge(train_with_feature,self.stores)
        test_with_feature_new = pd.merge(test_with_feature,self.stores)

        # drop the dublicate of IsHoliday column
        train_with_feature = train_with_feature_new.drop(columns=['IsHoliday_x'])
        test_with_feature = test_with_feature_new.drop(columns=['IsHoliday_x'])

        # rename the IsHoliday_y column to IsHoliday
        train_with_feature = train_with_feature.rename(columns={"IsHoliday_y": "IsHoliday"})
        test_with_feature = test_with_feature.rename(columns={"IsHoliday_y": "IsHoliday"})

        def mapping(x):
            if x == False:
                return 1
            return 0.76

        #Train.csv
        actualScore = train_with_feature['IsHoliday']
        posiveNegave = actualScore.map(mapping)
        train_with_feature['IsHoliday'] = posiveNegave
        print("Shape of train_with_feature: ", train_with_feature.shape)
        train_with_feature.head(3)

        #Test.csv
        actualScore_test = test_with_feature['IsHoliday']
        posiveNegave = actualScore.map(mapping)
        test_with_feature['IsHoliday'] = posiveNegave
        print("Shape of test_with_feature: ", test_with_feature.shape)
        test_with_feature.head(3)

        def type_count(x):
            ''' This function will chang
            IsHoliday column with Flase to be 0 
            and True to be 1'''
            
            if x == 'A':
                return 1
            elif x == 'B':
                return 2
            return 3

        #Train.csv
        actualScore = train_with_feature['Type']
        type_coun = actualScore.map(type_count)
        train_with_feature['Types'] = type_coun

        #Test.csv
        actualScore = test_with_feature['Type']
        type_coun = actualScore.map(type_count)
        test_with_feature['Types'] = type_coun

        # #train data
        # #let's take mean of Temp and Unemployment
        # train_with_feature['Temp_mean'] = train_with_feature['Temperature'].mean()
        # train_with_feature['Unemployment_mean'] = train_with_feature['Unemployment'].mean()

        # #test data
        # test_with_feature['Temp_mean'] = test_with_feature['Temperature'].mean()
        # test_with_feature['Unemployment_mean'] = test_with_feature['Unemployment'].mean()

        train_with_feature = train_with_feature.drop(['Type'], axis=1)
        test_with_feature = test_with_feature.drop(['Type'], axis=1)

        train_with_feature = train_with_feature[train_with_feature["Types"]==1]
        test_with_feature = test_with_feature[test_with_feature["Types"]==1]

        train_with_feature.to_csv("data/train_with_feature_final.csv")
        test_with_feature.to_csv("data/test_with_feature_final.csv")


if __name__=="__main__":
    Data = DATA()
    Data.get_data()
    Data.get_new_featuers()
    Data.merge_features()
