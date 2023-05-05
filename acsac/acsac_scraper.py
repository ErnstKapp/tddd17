import requests
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import random
import time
import json
import re


for year in range(2012, 2023):
    time.sleep(2)

    xml = requests.get(f"https://dblp.org/db/conf/acsac/acsac{year}.xml").text
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

    file = open(f"acsac{year}.txt", 'a', encoding='utf-8') ## fixa bort hårdkodning, in i mappar också

    no_of_articles = len(articles)
    article_no = 0
    
    for article in articles:
        article_no += 1

        html_text = requests.get(article['url'], headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = bs(html_text, 'html.parser')

        print(article['url'])

        abstract = soup.find(class_="abstractSection abstractInFull") #ACM 2012-2022
        
        if abstract == None:
            abstract = "*** No abstract available ***"
        else:
            abstract = abstract.text

        article['abstract'] = abstract
        print(article['abstract'])
        
        file.writelines(article['title'])
    
        file.writelines(article['abstract'])
        file.write("\n")
        

        #time.sleep(random.randint(1, 4))
        print(str(article_no) + "/" + str(no_of_articles) + " " + str(year))
