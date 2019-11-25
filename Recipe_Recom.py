#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import operator
from IPython.core.display import display
import warnings
warnings.filterwarnings("ignore")


def recipe(orders,recipes,dept,products):
    recipes = recipes.dropna()
    dept_of_interest = dept.query('department == "produce" or department == "bakery" or department == "international" or department == "beverages" or department == "dry goods pasta" or department == "bulk" or department == "meat seafood" or department == "pantry" or department == "dairy eggs"')  #fetching the 'Produce Department'

    #fetching the 'Produce Department' id

    val = dept_of_interest['department_id'] #val stores the department id for 'Produce Department'


    dept_of_interest # shows department id

    filtered_products = products.loc[products['department_id'].isin(val)] #getting products from the 'Produce Department'
    filtered_products = pd.Series(filtered_products['product_id']) # filter products that have a products id

    filtered_products_list = filtered_products.tolist() # converting datafame to list

    # converting all the values in striing
    filtered_products_strlist = [] 
    for elem in filtered_products_list:
        filtered_products_strlist.append(str(elem))


    # converting values in product id column as string
    orders['product_id'] = orders['product_id'].astype(str)

    # printing orders
    orders
        

    filtered_orders = orders.loc[orders['product_id'].isin(filtered_products_strlist)] #fetching orders which contain products from the filtered products list


    del filtered_orders['add_to_cart_order'] # removing column add_to_cart_order


    del filtered_orders['reordered'] # removing reordered column


    product_id_name_map = products.loc[products['product_id'].isin(filtered_products_strlist)] 

    product_id_name_map

    # geting product table where 'product id' matches with filtered_products_strlist

    # converts the value in string
    product_id_name_map['product_id']= product_id_name_map['product_id'].apply(str)
    product_id_name_map['product_id']

    filtered_orders['product_id'].apply(str)

    # merge the filtered orders table and  product_id_name_map table

    with pd.option_context('mode.chained_assignment', None):

        final_table = pd.merge(filtered_orders, product_id_name_map, on = 'product_id', how = 'left')

    #Select a random order number from the final_table
    order_product_names = final_table.query('order_id == 2583825')['product_name'] #28533

    #store the products from the order into a order_product_list
    order_product_list = order_product_names.tolist()

    print("The products in the order selected\n")
    #Display the products for that order
    display(order_product_list)

    recipe_product_mapping = dict()
    individual_products = []


    #loop through the products list to separate items by space
    for product in order_product_list: 
        for prod in product.split(" "):
            individual_products.append(prod)

    #create a dict to store the recipes names as key
    #and the number of items it matches from the products list in the recipe ingredients as the value        
    for product in individual_products:
        count = 0
        for index, row in recipes.iterrows(): 
            if(product in row["Ingredients"]):
                count += 1  
                recipe_product_mapping.update({row["RecipeName"]:count})
                

    #get the recipe names which have the largest value of matched items
    top_3_sorted_recipes = sorted(recipe_product_mapping, key=recipe_product_mapping.get, reverse=True)[:3]

    #get recipe details of the top 3 matched recipes
    recipe_details = recipes.loc[recipes['RecipeName'].isin(top_3_sorted_recipes)]


    print("\nThe top 3 suggested recipes \n")
    #print the detials to the matched recipes
    display(recipe_details)

