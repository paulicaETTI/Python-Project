from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time
import re

option = webdriver.ChromeOptions()
option.add_argument('start-maximized')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.get('https://www.mai.gov.ro/informare-covid-19-grupul-de-comunicare-strategica-10-decembrie-ora-13-00-2/')

dictionar = {
        'Nr. crt.': [],
        'Judet': [],
        '10.12.2021': []
    }

try:
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div/div[3]/button[1]")))
    button.click()
    time.sleep(2)
finally:
    table = driver.find_element(by=By.XPATH, value='//*[@id="post-28531"]/div/div/table[1]/tbody')
    table_list = table.text.split('\n')
    del table_list[0]
    for row_index, row_value in enumerate(table_list):
        if row_index < 42:
            dictionar['Nr. crt.'].append(row_index + 1)
            row_value_split = row_value.split(' ')
            number = row_value_split[-2]
            del row_value_split[0]
            del row_value_split[-3:]
            judet = str(row_value_split)
            dictionar['Judet'].append(judet)
            dictionar['10.12.2021'].append(number)
    print(dictionar)











