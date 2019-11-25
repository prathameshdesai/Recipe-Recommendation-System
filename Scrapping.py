from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import csv

def scrapping():
    url = "https://www.geniuskitchen.com/topic/casseroles"

    html = urlopen(url)
    bsyc = BeautifulSoup(html.read(), "lxml")
  


    ##**************MAIN CATEGORY OF RECIPES
    category_dict = {}
    for data in bsyc.find_all('div', class_='recipe-topics'):
        for a in data.find_all('a'):
            category_dict.update({a.text:a.get('href')})
    category_dict

    ##*****************Count Recipes per Categories
    category_count = {'Dietary':0, 'Meat':0,'Occasion':0,'Seafood':0, 'Desserts':0,
                      'Holiday':0, 'Popular':0, 'Holiday':0,'Cuisine':0,'Course':0,
                      'Main Ingredients':0,'Preparation':0}
            
    ####***************LOOPING OVER THE SUB CATEGORIES
    ingre_dict = {}
    #category = []
    category = 'Popular'
    for ingredient, ingredientLink in category_dict.items():
        if(ingredient=='Dietary'):
            category = 'Dietary'
        elif(ingredient=='Meat'):
            category = 'Meat'
        elif(ingredient=='Seafood'):
            category = 'Seafood'
        elif(ingredient=='Occasion'):
            category = 'Occasion'
        elif(ingredient=='Dessert'):
            category = 'Desserts'
        elif(ingredient=='Holiday'):
            category = 'Holiday'
        elif(ingredient=='Popular'):
            category = 'Popular'
        elif(ingredient=='Cuisine'):
            category = 'Cuisine'
        elif(ingredient=='Course'):
            category = 'Course'
        elif(ingredient=='Main\n                                            Ingredient'):
            category = 'Main Ingredients'
        elif(ingredient=='Preparation'):
            category = 'Preparation'
        category_count[category]+= 1
        #print (ingredient)
        try:
            open_link = urlopen(ingredientLink)
        except:
            continue
        category_count[category]+= 1
        bsoup = BeautifulSoup(open_link.read(), "lxml")
        data = json.loads(bsoup.find('script', type='application/ld+json').text)
        data_list = []
        data_list = data['itemListElement']
        for ele in data_list:
            in_link = ele['url']
            in_name = ' '.join(in_link.split("/")[-1].split("-")[:-1])
            ingre_dict.update({in_name:in_link})
            #category.append(ingredient)
    ingre_dict

    with open('dict.csv',"w", encoding='utf-8',newline='') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in category_count.items():
       writer.writerow([key, value])
       
    csvfile = "Recipes_Uncleaned.csv"
    with open(csvfile, "a",encoding='utf-8',newline='') as fp:
            wr = csv.writer(fp)
            wr.writerow(['RecipeName', 'Ingredients', 'Directions', 'CookingTime', 'Serves','category'])
    ####****************LOOPING OVER INGREDIENT DICT TO FETCH RECIPE
    for in_name ,in_link in ingre_dict.items():
        print(in_name)
        try:
            open_link = urlopen(in_link)
        except:
            continue
        bsyc = BeautifulSoup(open_link.read(), "lxml")
        ingredients = []
        
        for ultag in bsyc.find_all('ul', {'class': 'ingredient-list'}):
            if(ultag != None):
                for litag in ultag.find_all('li'):
                    ingredients.append(litag.text)
                ingredients = ";".join(ingredients)

        directions = []
        if(bsyc.ol != None):
            for tag in bsyc.ol.find_all("li", recursive=True):
                directions.append(tag.text)
                #directions.append(tag.text.replace('\n','').replace('\r',''))
            #directions = directions[:-1]
            directions =";".join(directions)

        #time = '0'
        time = bsyc.find('td', class_ = 'time')
        if(time != None):
            #cookingtime = time.text
            cookingtime = time.text.replace(' ','').replace('\n','')
        else:
            cookingtime= '0'
        serving_size = bsyc.find('td', class_ = 'servings')
        if(serving_size != None):
            #serves = serving_size.text
            serves = serving_size.text.replace(' ','').replace('\n','')
        else:
            serves = '0'

        rows = [in_name,ingredients, directions, cookingtime, serves, category]

        with open(csvfile, "a",encoding='utf-8',newline='') as fp:
            wr = csv.writer(fp)
            wr.writerow(rows)

    return category_count




    
