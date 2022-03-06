
#!/usr/bin/env python

"""preprocess.py: Preprocess data"""

__author__ = "Jidhu Mohan"
__copyright__ = "Copyright (C) 2022 Factory-AI project"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jidhu Mohan"
__email__ = "Jidhu.Mohan@gmail.com"
__status__ = "PoV" 


import pandas as pd
import numpy as np

def data_preprocess():
    df_train = pd.read_csv("data/train_with_feature_final.csv")

    # drop columns
    features_drop = ['Unnamed: 0', 'CPI', 'Date', 'Store','Types',\
                        'MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']
    df_train.drop(features_drop, axis=1, inplace=True)

    df_train['Fuel_Price'] = df_train['Fuel_Price'].apply(lambda x:x*1000)

    # Group, inventory, selling price
    df_train.rename(columns={'IsHoliday':'Holiday', 'Type':'Group',\
                            'Temperature':'Cost_Price','Unemployment':'Total_Inventory',\
                            'Fuel_Price':'Selling_Price'}, inplace=True)
    #np.array(np.divide(np.array(df_train['Weekly_Sales']), df_train['Selling_Price'])* \
    df_train['Demand'] = np.abs(np.array(np.divide(np.array(df_train['Weekly_Sales']), df_train['Selling_Price'])*0.8+ \
                                ((np.array(df_train["Selling_Price"]) - np.array(df_train["Cost_Price"]))/7), dtype=np.int))

    # filter out for one shop
    df_train = df_train[df_train["Size"]==151315]
    df_train.drop(['Dept','Size','Weekly_Sales'], axis=1, inplace=True)

    # cost price
    df_train['Cost_Price'] = df_train['Cost_Price'].apply(lambda x:x*24)

    # selling price
    df_train['Selling_Price'] = np.multiply(df_train["Selling_Price"],df_train["Holiday"])

    df_train.drop(['Holiday'], inplace=True, axis=1)

    #Inventory
    df_train['Total_Inventory'] = np.array(np.multiply(df_train["Total_Inventory"],260),dtype=int)

    def mapping(x):
        if x<500: return 578+x
        # elif x<250: return 378+x
        elif x>2500: return 2750
        else: return x

    df_train["Demand"] = df_train["Demand"].apply(mapping)

    df_train.to_csv("data/data_pre_processed.csv", index=False)