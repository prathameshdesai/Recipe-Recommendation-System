#!/usr/bin/env python
# coding: utf-8

# ## Associative Rule Mining



# Market Basket Analysis
import pandas as pd
import mlxtend
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori
from IPython.core.display import display
import warnings
warnings.filterwarnings("ignore")


def arms(orders,recipes,dept,products):

    print('Association rule mining is used to find the most bought products and their relationship')
    dept_of_interest = dept.query('department == "produce" or department == "bakery" or department == "international" or department == "beverages" or department == "dry goods pasta" or department == "bulk" or department == "meat seafood" or department == "pantry" or department == "dairy eggs"')  #fetching the 'Produce Department'


    #products = pd.read_csv(xls, 'products') # reading products file


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


    # final table contains order id mapped with product id , proudct name aisle id and department id
    final_table


    # group order id by order id and product name 
    matrix = final_table.groupby(['order_id'])['product_name'].apply(list).values.tolist()
    matrix


    # # Transform Dataframe 


    #Change variables from here
    # create a table with true and false matrix for every transactio

    te = TransactionEncoder()
    te_ary = te.fit(matrix).transform(matrix)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    df




    # # Find products that are bought more than Five percent of the times



    support = apriori(df, min_support=0.05, use_colnames=True)
    print('Products that are bought more than Five percent of the time (Support)')
    print('')
    display(support)
    print('')

    # Below items should always be kept in stock


    # #  Find products that are bought one percent of the time 

    print('Products that are bought more than One percent of the time (Support) ')
    print('')
    frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    display(frequent_itemsets)


    # # Products selected with more than one percent support and twenty percent confidence



    # Use the above data with products that are bought one percent of the times and select products that are bought in pairs i.e if one product is bought then the other product is also bought. Only give result for product that are bought more than 20 percent of the time together i.e that have a confidence of more than 20 percent
    print('Products that are bought more than Twenty percent of the times together (Confidence)')
    print('')
    products_association = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.20)
    display(products_association)
    print('')

    # #  Products filtered from the above result with more than 2.5 lift

    # Lift is support of(A and B together )/ (support of A)* (support of B)
    # We have taken the lift value greater than 2.5 as it shows that chances of A and B together occuring are more independent of A and B 

    print('Product which are more than Two and a half times likely to be bought together (Lift) ')
    print('')
    products_association = products_association[ products_association['lift'] >= 2.5]
    display(products_association)
