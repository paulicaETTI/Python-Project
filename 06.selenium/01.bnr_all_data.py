import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

option = webdriver.ChromeOptions()
option.add_argument('start-maximized')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.get('https://www.bnr.ro/files/xml/nbrfxrates2022.htm')
table = driver.find_element(by=By.XPATH, value='//*[@id="Data_table"]')
print(table.text)
# lista = table.text.split('\n')
# header_len = driver.find_element(by=By.XPATH, value='//*[@id="Data_table"]/table/thead/tr')
# header = header_len.text.split('\n')
#
# dictionar = {i: [] for i in header}
#
# for j in range(len(header)):
#     for i in range(len(header) + j, len(lista), len(header)):
#         dictionar[header[int(j)]].append(lista[i])
#
# # print(dictionar)
# df = pd.DataFrame(dictionar)
# df.to_csv("BNR_ALL_DATA.csv")
