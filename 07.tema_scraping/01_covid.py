from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

option = webdriver.ChromeOptions()
option.add_argument('start-maximized')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

dictionar = {
            'Nr. crt.': [],
            'Judet': []
        }

for i in range(5):
    driver.get(f'https://www.mai.gov.ro/informare-covid-19-grupul-de-comunicare-strategica-1{str(i)}-decembrie-ora-13'
               f'-00-2/')
    dictionar[(f'1{str(i)}.12'
               f'.2021')] = []

    if i == 0:  # First page
        try:
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div["
                                                                                               "6]/div/div[3]/button["
                                                                                               "1]")))
            button.click()
            # time.sleep(1)
            button2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div["
                                                                                                "1]/div/a")))
            button2.click()
            time.sleep(1)  #???????????????
        except NoSuchElementException as e:
            print("Element not found: ", e)

        table = driver.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[1]/main/article/div/div/table['
                                                       '1]/tbody')
        table_list = table.text.split('\n')
        del table_list[0]
        for row_index, row_value in enumerate(table_list):
            print(row_value)
            if row_index < 42:
                dictionar['Nr. crt.'].append(row_index + 1)
                row_value_split = row_value.split(' ')
                number = row_value_split[-3]
                del row_value_split[0]
                del row_value_split[-3:]
                # judet = str(row_value_split[0])
                judet = ' '.join(row_value_split)
                dictionar['Judet'].append(judet)
                dictionar[f'1{str(i)}.12.2021'].append(number)
            if row_index == 42:
                dictionar['Nr. crt.'].append(43)
                dictionar['Judet'].append('Din strainatate**')
                row_value_split = row_value.split(' ')
                dictionar[f'1{str(i)}.12.2021'].append(row_value_split[-4])
            if row_index == 46:
                dictionar['Nr. crt.'].append(44)
                dictionar['Judet'].append('TOTAL')
                row_value_split = row_value.split(' ')
                dictionar[f'1{str(i)}.12.2021'].append(row_value_split[-4])

    else:       # Next pages
        table = driver.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[1]/main/article/div/div/table['
                                                       '1]/tbody')
        table_list = table.text.split('\n')
        del table_list[0]
        for row_index, row_value in enumerate(table_list):
            print(row_value)
            if row_index < 42:
                row_value_split = row_value.split(' ')
                number = row_value_split[-3]
                dictionar[f'1{str(i)}.12.2021'].append(number)
            if row_index == 42:
                row_value_split = row_value.split(' ')
                if i == 3:
                    dictionar[f'1{str(i)}.12.2021'].append(row_value_split[-2])
                else:
                    dictionar[f'1{str(i)}.12.2021'].append(row_value_split[-4])
            if row_index == 46:
                row_value_split = row_value.split(' ')
                if i == 3:
                    dictionar[f'1{str(i)}.12.2021'].append(row_value_split[-2])
                else:
                    dictionar[f'1{str(i)}.12.2021'].append(row_value_split[-4])

df = pd.DataFrame(dictionar)
df.to_csv('date_covid')
