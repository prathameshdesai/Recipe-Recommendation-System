import pandas as pd

# Read all the excel files
xls = pd.ExcelFile('Datasets_Group4.xlsx') # reading the datasets excel file
orders = pd.read_excel(xls, "order_products__train") # reading order products from excel file
recipes = pd.read_excel(xls, "Final_Merged_Dataset") # reading final merged dataset
dept = pd.read_excel(xls, "departments") #reading department ids-name pairs
products = pd.read_excel(xls, 'products') # reading products file
category_count = pd.read_excel(xls, 'category_count')



# Asssociation Rule Mining 

import AssociationRuleMining as am
am.arms(orders,recipes,dept,products)


# Recipe recommendation code runs
import Recipe_Recom as rr
rr.recipe(orders,recipes,dept,products)


