from bs4 import BeautifulSoup
import requests

html_response = requests.get('https://www.scrapethissite.com/pages/simple/')
html_text = requests.get('https://www.scrapethissite.com/pages/simple/').text

print(f"Response: {html_response}")
# print("Content:\n")
# print(html_text)

soup = BeautifulSoup(html_text, 'lxml')

country_row = soup.find_all('div', class_='row')

for country_div in country_row[3:]:
    country_div = soup.find_all('div', class_='col-md-4 country')
    for country_name in country_div:
        country_name = country_name.h3.text.replace(' ', '').strip()
        print(country_name)





