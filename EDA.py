##Exploratory Data Analysis
#%matplotlib inline
import matplotlib.pyplot as plt 
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import Scrapping as sc
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from collections import Counter
import numpy as np

##***********************
#reading department table
dept = pd.read_csv("departments.csv") 
#fetching department ids for the departments of interest
dept_of_interest = dept.query('department == "produce" or department == "bakery" or department == "international" or department == "beverages" or department == "dry goods pasta" or department == "bulk" or department == "meat seafood" or department == "pantry" or department == "dairy eggs"')

#val stores the department ids 
val = dept_of_interest['department_id'] 

#reading the products file
xls = pd.ExcelFile('Python_Prototype_Group4.xlsx')
products = pd.read_excel(xls, "products")

#getting products that belong to the above list of departments
filtered_products = products.loc[products['department_id'].isin(val)] 


filtered_products = pd.Series(filtered_products['product_id'])
filtered_products_list = filtered_products.tolist()

#reading the orders file
orders = pd.read_excel(xls, "order_products__train")
recipes = pd.read_excel(xls, "Final_Merged_Dataset")

#missing data treatment
recipes = recipes.dropna()

filtered_products_strlist = []
for elem in filtered_products_list:
    filtered_products_strlist.append(str(elem))

orders['product_id'] = orders['product_id'].astype(str)

#fetching orders which contain products from the filtered products list
filtered_orders = orders.loc[orders['product_id'].isin(filtered_products_strlist)] 

del filtered_orders['add_to_cart_order']
del filtered_orders['reordered']

product_id_name_map = products.loc[products['product_id'].isin(filtered_products_strlist)]


# Visualization showing the number of product varities by each department 
product_id_name_map.department_id.unique()
n, bins, patches = plt.hist(product_id_name_map.department_id, 47, facecolor="red", alpha=.75, align='mid')
plt.xlabel("department_id")
plt.ylabel("product Count")
plt.title("Department wise product stock")
plt.figure()
plt.show()


#merging into a final table based on product id
product_id_name_map['product_id'].apply(str)
product_id_name_map['product_id']= product_id_name_map['product_id'].apply(str)
product_id_name_map['product_id']

final_table = pd.merge(filtered_orders, product_id_name_map, on = 'product_id')

grouped_by_depts_df = final_table.aggregate()

del grouped_by_depts_df['product_id']
del grouped_by_depts_df['product_name']
del grouped_by_depts_df['aisle_id']


##*******************Category Visualization

#Word Cloud
cat1 = []
for cat,num in sc.category_count.items():
    cat1.append((cat+' ')*num)
cat_str= ' '.join(cat1)
comment_words = ' '
stopwords = set(STOPWORDS)
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(cat_str)

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()

##Horizontal Graph
plt.barh(range(len(sc.category_count)), list(sc.category_count.values()), align='center')
plt.yticks(range(len(sc.category_count)), list(sc.category_count.keys()))
plt.show()

##Swarm Plot - customer popular days and hours relationship
dept_new = dept[dept.user_id <=1000]
dept_new.dropna()
c = Counter(zip(dept.order_dow,dept.order_hour_of_day))
s = [0.0001*c[(x,y)] for x,y in zip(dept.order_dow,dept.order_hour_of_day)]
ax = plt.scatter(x="order_dow", y="order_hour_of_day", s=s, data=dept)

plt.show()

