#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#Required Imports

from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup

#Initialize the variables
bsyc=""
urls = []
name=[]
ingred=[]
instruct=[]
count=0

#Loop to traverse all the 75 pages and retrieve URL
for v in range(75):
    
    #create the unique URL for each page
    x = 'https://whatscooking.fns.usda.gov/search/recipes?page='
    url=x+str(v)

    #Open the URL
    html = urlopen(url)

    #Use BeautifulSoup to read the html
    x =BeautifulSoup(html.read(), "lxml")

    #To add all teh 20 URL's on each page
    for h in x.find_all('h3'):   
        try:
             urls.append(h.find('a').attrs['href'])
            
        except:
             pass   

#Traverse through each URL      
for z in urls:
    z = "https://whatscooking.fns.usda.gov"+z
    html = urlopen(z)

    #Use BeautifulSoup to read the html
    bsyc = BeautifulSoup(html.read(), "lxml")

    #Retrieve the information regarding instructions to make the recipe
    divs = bsyc.find("div", { "class" : "recipe-instructions recipe-section field field--name-recipe-instructions field--type-text-long field--label-above" })
    try:
        for div in divs:
            try:
                inner_text = str(div.text)
                strings = str(inner_text)
                if strings == "Directions":
                    continue
                else:
                    
                    instruct.append(strings)
                    count = count+1
                    
            except:
                pass 
    except:
        pass

    #Retrieve the information regarding ingredients in the recipe
    divs = bsyc.find("div", { "class" : "field field--name-recipe-ingredient field--type-ingredient-reference field--label-above" })
    try:
        for div in divs:
            try:
                inner_text = str(div.text)
                strings = str(inner_text)
                if strings == "Ingredients":
                    continue
                else:
                    ingred.append(strings)
                    
                
                
            except:
                pass
    except:
            pass

    #Retrieve the information regarding recipe name
    divs = bsyc.find("div", { "class" : "titleWrapper" })
    try:
        for div in divs:
            try:
                inner_text = str(div.text)
                strings = str(inner_text)
                
                name.append(strings)
                
            except:
                pass
    except:
            pass
        
   

#Write all the scraped content into a csv file        
import csv
count =0
myFile = open('WhatsCooking.csv', 'w', encoding="utf-8")  
with myFile:  
    myFields = ['Name', 'Ingredients','Instructions']
    writer = csv.DictWriter(myFile, fieldnames=myFields)    
    writer.writeheader()
    for v in name:
         writer.writerow({'Name' : v, 'Ingredients': ingred[count],'Instructions': instruct[count] })
         count = count+1
        








