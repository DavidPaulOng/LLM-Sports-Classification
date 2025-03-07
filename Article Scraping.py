from bs4 import BeautifulSoup
import requests
from newspaper import Article
import newspaper
import re

import pandas as pd

# URLs of the index pages
index_urls = [
    "https://sport.detik.com/sepakbola/liga-inggris",
    "https://sport.detik.com/sepakbola/liga-indonesia",
    "https://www.liputan6.com/tag/liga-spanyol",
    "https://www.liputan6.com/tag/liga-italia",
    "https://sport.detik.com/"
]

classification_article = [
    "Liga Inggris", 
    "Liga Indonesia", 
    "Liga Spanyol",
    "Liga Italia",
    "Non sepak bola"
]

# Limit articles per index page
limit = 25  
FINAL_DF = pd.DataFrame()

for i, index_url in enumerate(index_urls):
    response = requests.get(index_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract article links (adjust selectors for each website)
    # For example, links in Detik might use a specific structure, so inspect the HTML:
    article_links = set()

    if (classification_article[i] != "Non sepak bola"):
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            # Ensure it's a full URL AND IS IN THE CORRECT DIRECTORY
            if ('http' in link and link.startswith(index_url + '/'))\
            or link.startswith("https://www.liputan6.com/hot/read/"):  # Liputan works differently to detik.com
                article_links.add(link)

    else:
        # ARTICLES FOR "berita olahraga non sepak bola"
        index_url = "https://sport.detik.com"
        pattern = re.compile(re.escape(index_url) + r"/.+/d") # 'd' IS ADDED BECAUSE ALL ARTICLES IN detik.com STARTS WITH 'd'

        response = requests.get(index_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']
                if 'http' in link and pattern.match(link) and not link.startswith("https://sport.detik.com/sepakbola"):
                    article_links.add(link)


    # LIMIT NUMBER OF ARTICLES IN EACH URL
    article_links = list(article_links)[:limit]

    # PROCESS EACH ARTICLE IN THE URL
    list_title = []
    list_text = []
    list_source =[]
    for article in article_links:
        built_article = Article(article)
        built_article.download()
        built_article.parse()
        list_title.append(built_article.title)
        list_text.append(built_article.text)
        list_source.append(built_article.source_url)
    
    # CREATE DATAFRAME WITH ALL THE RELEVANT INFORMATION
    temp_df = pd.DataFrame(
        {'Title': list_title, 
         'Text': list_text, 
         'Source': list_source,
         'URL': article, 
         'Label': classification_article[i]}
    )
    
    FINAL_DF = pd.concat([FINAL_DF, temp_df], axis=0)

print(FINAL_DF)
FINAL_DF.to_csv("Scraped Articles.csv")
