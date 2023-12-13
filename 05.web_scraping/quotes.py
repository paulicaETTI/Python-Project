import requests
from bs4 import BeautifulSoup
import pandas as pd
import itertools
import threading
import time
import sys

data_quotes = {                               # data is now a dictionary
    'Quote': [],
    'Author': [],
    'Tags': []
}
data_quotes = pd.DataFrame(data_quotes)       # data is now a pandas dataframe
auth_set = set()
tag_set = set()

base_page_url = "https://quotes.toscrape.com/"

for page_nr in range(1, 11):

    current_page_url = f'{base_page_url}page/{page_nr}/'
    resource = requests.get(current_page_url)
    soup = BeautifulSoup(resource.text, 'html.parser')
    quotes = soup.find_all('div', attrs={'class': 'quote'})

    for quote in quotes:
        quote_text = quote.find('span', attrs={'class': 'text'}).text.strip()          # quote text
        quote_auth = quote.find('small', attrs={'class': 'author'}).text.strip()       # quote author
        quote_text = quote_text.replace('“', '').replace('”', '')                      # delete quote marks in quote
        auth_set.add(quote_auth)                                                       # add author to set

        quote_tags = quote.find_all('a', attrs={'class': "tag"})                       # get all quote tags(html format)
        tags = []
        for tags1 in quote_tags:
            tags.append(tags1.get_text())                                              # append tags to tag list
            tag_set.add(tags1.get_text())                                              # add tags to global tags set

        new_row = [quote_text, quote_auth, ', '.join(tags)]
        data_quotes.loc[len(data_quotes)] = new_row

# print(data_quotes)
# print(f"Authors: {auth_set}, \n\nTags: {tag_set}, ")

df = pd.DataFrame(data_quotes)
print(df)
df.to_csv('bnr_data')



