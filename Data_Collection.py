from newsapi import NewsApiClient
import json

# Load API key
newsapi_key=open("/home/daniel_a_lebedinsky/newsapi_key", 'r')
newsapi = NewsApiClient(api_key=newsapi_key.readline())

# NewsAPI returns a dictionary of tuples, where the first 2 items are metadata,
# the third is a list of every article
def DictList(all_articles):
    dict_pairs = all_articles.items()
    pairs_iterator = iter(dict_pairs)
    first_pair = next(pairs_iterator)
    second_pair = next(pairs_iterator)
    third_pair = next(pairs_iterator)
    # Each article is a dictionary, with the following keys:
    # source, author, title, description, url, urlToImage, publishedAt, content
    return third_pair[1]

# If you have the free tier of NewsAPI, you will need to adjust these dates
# The earliest date must be less than one month prior to the present date.
from_date= '2023-04-07'
to_date='2023-05-06'

all_articles = DictList(newsapi.get_everything(q='AI',
                                      from_param=from_date,
                                      to=to_date,
                                      language='en'))

QueryList=[]
QueryList.append(DictList(newsapi.get_everything(q='Artificial Intelligence',
                                      from_param=from_date,
                                      to=to_date,
                                      language='en')))

QueryList.append(DictList(newsapi.get_everything(q='Machine Learing',
                                      from_param=from_date,
                                      to=to_date,
                                      language='en')))

QueryList.append(DictList(newsapi.get_everything(q='ChatGPT',
                                      from_param=from_date,
                                      to=to_date,
                                      language='en')))

QueryList.append(DictList(newsapi.get_everything(q='GPT-4',
                                      from_param=from_date,
                                      to=to_date,
                                      language='en')))

QueryList.append(DictList(newsapi.get_everything(q='OpenAI',
                                      from_param=from_date,
                                      to=to_date,
                                      language='en')))

# Combining all news queries to one list of dictionaries, and saving with JSON
for query in QueryList:
    if (type(query) is None):
        continue
    all_articles.extend(query)

with open('all_articles.txt', 'w') as file:
    for article in all_articles:
        file.write(json.dumps(article) + '\n')

newsapi_key.close()