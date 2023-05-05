import requests
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import random
import time
import json
import re


#conf_abbreviations = [ccs, sp, uss, ndss]

for year in [2012, 2013, 2014, 2015, 2017, 2019, 2020, 2021, 2022]: #2016 och 2018 omöjligt att skrapa på ett smidigt sätt
    xml = requests.get(f"https://dblp.org/db/conf/ndss/ndss{year}.xml").text
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

    file = open(f"ndss{year}.txt", 'a', encoding='utf-8')

    no_of_articles = len(articles)
    article_no = 0
    for article in articles:
        article_no += 1

        print(article['url'])
        html_text = requests.get(article['url'], headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = bs(html_text, 'html.parser')

        if ("/ndss-paper/" in article['url']): #2019 och framåt
            content = soup.find(class_ = "paper-data")
        else: 
            content = soup.find(class_="new-wrapper")

        if content == None:
            abstract = "*** No abstract available ***"
        elif content != None and "/ndss-paper" not in article['url']:
            abstract = content.text[content.text.find("Abstract:"):].strip("Abstract:")
        else:
            abstract = content.text[content.text.find("\n\n"):].strip("\n")

        print(abstract)
        article['abstract'] = abstract

        file.writelines(article['title'])
        file.writelines(article['abstract'])
        file.write("\n")

        #time.sleep(random.randint(1, 2))
        print(str(article_no) + "/" + str(no_of_articles) + " " + str(year))









