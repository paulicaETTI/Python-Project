import requests
from bs4 import BeautifulSoup
import pandas as pd

r = requests.get("https://www.bnr.ro/Cursul-de-schimb--7372.aspx")
link = BeautifulSoup(r.text, 'html.parser')

title = link.find_all('div', attrs={'class': 'contentDiv'})
dataset = []

for tr_index in title[0].find_all('table'):
    for td_index in tr_index.find_all('tr'):
        td_list = []
        if td_index.find_all('th'):
            header = []
            for th_index in td_index.find_all('th'):
                header.append(th_index.get_text())
            dataset.append(header)
        for index, td_value in enumerate(td_index.find_all('td')):
            if index == 0:
                td_list.append(td_value.get_text())
            else:
                td_list.append(float(td_value.get_text().strip().replace(',', '.')) if td_value.get_text().strip() != '' else '')
        if len(td_list) > 0:
            dataset.append(td_list)

# print(dataset)
df = pd.DataFrame(dataset)
print(df)
df.to_csv('bnr_data')