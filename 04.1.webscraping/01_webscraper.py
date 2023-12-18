from bs4 import BeautifulSoup
import requests
import pandas as pd

html_response = requests.get('https://www.scrapethissite.com/pages/simple/')
html_text = requests.get('https://www.scrapethissite.com/pages/simple/').text

# print(f"Response: {html_response}")
# print("Content:\n")
# print(html_text)

soup = BeautifulSoup(html_text, 'html.parser')
countries = soup.find_all('div', {'class', 'col-md-4 country'})

dataset = []
table_header = ['Name', 'Capital', 'Population', 'Area']
dataset.append(table_header)

# print(f'{"Name":35} | {"Capital":35} | {"Population":15} | {"Area":20}')
for country in countries:
    country_name = country.find('h3', {'class', 'country-name'}).text.strip()
    country_capital = country.find('span', {'class', 'country-capital'}).text.strip()
    country_population = country.find('span', {'class', 'country-population'}).text.strip()
    country_area = country.find('span', {'class', 'country-area'}).text.strip()
    dataset.append([country_name, country_capital, country_population, country_area])

    # print()
    # print(f'{country_name:35} | {country_capital:35} | {country_population:15} | {country_area:20}')

print(dataset)
df = pd.DataFrame(dataset)
print(df)
df.to_csv('countries_data')








