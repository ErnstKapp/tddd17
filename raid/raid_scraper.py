import requests
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import random
import time
import json
import re


#conf_abbreviations = [ccs, sp, uss]

for year in range(2012, 2023):
    time.sleep(2)

    xml = requests.get(f"https://dblp.org/db/conf/raid/raid{year}.xml").text
    root = ET.fromstring(xml)

    inproceedings = root.findall(".//inproceedings")

    articles = []
    for inproceeding in inproceedings:
        article_dict = {}
        for element in inproceeding:
            if element.tag == 'ee' and 'url' not in article_dict: # tar bara den första länken ifall det finns flera
                article_dict['url'] = element.text
            elif element.tag == 'author':
                if 'author' in article_dict:
                    article_dict['author'] += ", " + element.text
                else:
                    article_dict['author'] = element.text
            elif element.tag == 'year':
                article_dict['year'] = element.text 
            elif element.tag == 'title':
                article_dict['title'] = element.text 
        articles.append(article_dict)

    file = open(f"raid{year}.txt", 'a', encoding='utf-8') ## fixa bort hårdkodning, in i mappar också

    no_of_articles = len(articles)
    article_no = 0

    #2012-2018 springer
    #2019-2020 usenix
    #2020-2022 acm
    
    
    for article in articles:
        article_no += 1

        html_text = requests.get(article['url'], headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = bs(html_text, 'html.parser')

        print(article['url'])

        # Springer, 2012-2018
        if year >= 2012 and year <= 2018:
            abstract = soup.find(id="Abs1-content").find('p') 

        # Usenix, 2019-2020
        elif year >= 2019 and year <= 2020:
            abstract = soup.find(class_="field field-name-field-paper-description field-type-text-long field-label-above")
            if not abstract == None:        
                abstract = abstract.find(class_="field-item odd")

        #ACM, 2021-2022
        elif year >= 2020 and year <= 2022:
            abstract = soup.find(class_="abstractSection abstractInFull")
        
        if abstract == None:
            abstract = "*** No abstract available ***"
        else:
            abstract = abstract.text

        article['abstract'] = abstract
        print(article['abstract'])
        
        file.writelines(article['title'])
        file.writelines("\n")
    
        file.writelines(article['abstract'])
        file.write("\n")
        file.write("\n")
        

        #time.sleep(random.randint(1, 4))
        print(str(article_no) + "/" + str(no_of_articles) + " " + str(year))
