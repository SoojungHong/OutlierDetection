# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 14:03:59 2017

@author: a613274
@about: 1. mapping string value to int value 2. plot to see the clustering
"""


#------------------------
# import libraries 
#------------------------
import csv
import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
from random import randint
import datetime as dt



#----------------------------------------------
# function : transform csv file to dataframe
#----------------------------------------------
def readAsDataframe(fileName): 
    #filePath = '/Users/soojunghong/Documents/AthleticumData_1/AthExportData_September2017/'
    atosFilePath = 'C:/Users/a613274/AthleticumPoc/RawData/AthExportData_September2017/'
 
    #file = filePath + fileName
    file = atosFilePath + fileName 
    
    #if the read row contains error, throw error 
    df = pd.read_csv(file, error_bad_lines=False)
    #df.info()
    
    #strip column names 
    df.columns = df.columns.str.strip()

    #print(df.head(10))
    return df

     
#----------------------------------------------
# function : transform tsv file to dataframe
#----------------------------------------------
def readTsvAsDataframe(fileName):
    #filePath = '/Users/soojunghong/Documents/AthleticumData_1/AthExportData_September2017/'
    atosFilePath = 'C:/Users/a613274/AthleticumPoc/RawData/AthExportData_September2017/'
 
    #file = filePath + fileName
    file = atosFilePath + fileName 
    
    #read .csv file using tab separator, if the read row contains error, throw error 
    df = pd.read_csv(file, error_bad_lines=False, sep="\t")
    return df


#-----------------------------
# Test : Read one sales file
#-----------------------------
salesFile = 'factSalesTransactions_201705.csv' #150706 rows 
sales = readAsDataframe(salesFile) 
sales.info()


#------------------------------------------------------------------------------------------
# Join Product and Salestransaction table with select only interested columns from sales and product file

simpleSales = sales[['DateID', 'TimeID', 'ProductID','ProductGroupID', 'NetPrice']]
simpleSales

dimProduct = 'dimProduct_TSV.csv' #ToDo : Read TSV
product = readTsvAsDataframe(dimProduct)
product.info()

simpleProduct = product[['ProductID', 'ProductFamilyCode', 'ProductFamilyCodeDesc', 'ProductCode', 'ProductCodeDesc', 'UniverseCode', 'UniverseCodeDesc']]
simpleProduct

#product.head(5)
#product.groupby(['UniverseCodeDesc']).size()

# do a bit of data cleaning 
simpleSales = simpleSales.convert_objects(convert_numeric=True)
simpleSales.columns = simpleSales.columns.str.strip()

simpleProduct.columns = simpleProduct.columns.str.strip()
simpleProduct = simpleProduct.dropna(subset=['ProductID']) #251550
#product = product.convert_objects(convert_numeric=True)

   
joined = pd.merge(simpleProduct, simpleSales, on='ProductID', how='inner')
joined.info()
joined.tail(10)

productIDarr = joined[['ProductID']]
productIDarr.max()
productIDarr.min()

import matplotlib.pyplot as plt
import numpy as np
plt.plot(productIDarr) #plot the array
plt.show()


productCodearr = joined[['ProductCode']]
productCodearr.max()
productCodearr.min()

import matplotlib.pyplot as plt
import numpy as np
plt.plot(productCodearr) #plot the array
plt.show()


univCodearr = joined[['UniverseCode']]
univCodearr
univCodearr.max()
univCodearr.min()

import matplotlib.pyplot as plt
import numpy as np
plt.plot(univCodearr) #plot the array
plt.show()


#check the range of productID


#columnNames = ['Date', 'Most Frequent Product Category', 'Least Frequent Product Category', 'Abnormality Class']


#---------------------------------------------------------------------------
# ToDo : need some text analysis
# 'ProductFamilyCodeDesc' column contains useful description about products
# combine all 'description' column and find out proper mappting 
