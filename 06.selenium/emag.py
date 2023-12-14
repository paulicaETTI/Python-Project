import pandas as pd
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

option = webdriver.ChromeOptions()
option.add_argument('start-maximized')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.get('https://www.emag.ro/#opensearch')
get_element = driver.find_element(by=By.ID, value='searchboxTrigger')
get_element.send_keys('telefon')
get_element.submit()
element = driver.find_elements(by=By.CLASS_NAME, value='card-item')

product_list = []
price_list = []
elements_list = []

for i in element:
    try:
        product = i.find_element(by=By.CLASS_NAME, value='card-v2-title')
        product_list.append(product.text)
        price = i.find_element(by=By.CLASS_NAME, value='product-new-price')
        price_list.append(price.text)
    except exceptions.NoSuchElementException:
        pass

elements_list.append(product_list)
elements_list.append(product_list)
df = pd.DataFrame(elements_list).transpose()
print(df)

# dictionar = {f"telefon_{i}": [] for i in range(1, len(element) + 1)}
# dictionar = {}
# for i in range(1, len(element) + 1):
#     dictionar[f"telefon_{i}"] = []
# print(dictionar)



