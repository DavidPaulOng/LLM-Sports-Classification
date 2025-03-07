# Classification of Indonesian Sports News Category using LLMs

## Overview
Transformers and LLMs were used in this project to predict the categories of Indonesian sports news categories, whether an article is writing about the Spanish League, Italian League, Indonesian League, Premiere League, 
or it's an article not relating to footbal. There were two transformer architectures used in the project, the first was an ordinary LLM classifier using IndoBert as the base model, and the second is a two stage model. The first
stage of this model is a binary classifier, predicting whether a news article is a football article or not. The second predicts the football categories.

## Data
The data were manually scraped using python libraries such as BeautifulSoup and Newspaper3k
