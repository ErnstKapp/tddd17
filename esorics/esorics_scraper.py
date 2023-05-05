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

    for i in range(1, 3):
        if year in [2012, 2013]:
            xml = requests.get(f"https://dblp.org/db/conf/esorics/esorics{year}.xml").text
        else:
            xml = requests.get(f"https://dblp.org/db/conf/esorics/esorics{year}-{i}.xml").text
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
   
    
        file = open(f"esorics{year}.txt", 'a', encoding='utf-8') ## fixa bort hårdkodning, in i mappar också

        no_of_articles = len(articles)
        article_no = 0

        for article in articles:
            article_no += 1

            html_text = requests.get(article['url'], headers={'User-Agent': 'Mozilla/5.0'}).text
            print(article['url'])
            soup = bs(html_text, 'html.parser')
            abstract_element = soup.find(id = "Abs1-content")

            if abstract_element == None:
                abstract = "*** No abstract available ***"
            elif "Keywords" in abstract_element.text:
                abstract = abstract_element.text[:abstract_element.text.find("Keywords")]
            else:
                abstract = abstract_element.text

            article['abstract'] = abstract
            print(article['abstract'])
        
            file.writelines(article['title'])
            file.writelines("\n")
        
            file.writelines(article['abstract'])
            file.write("\n\n")


            #time.sleep(random.randint(1, 4))
            print(str(article_no) + "/" + str(no_of_articles) + " " + str(year))

        
        if year in [2012, 2013]:
            break