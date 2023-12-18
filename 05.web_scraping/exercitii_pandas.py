import pandas as pd
import numpy as np

# dintr o lista

# lista = [10, 20, 30, 40, 50]
# etichete = ['a', 'b', 'c', 'd', 'e']
# serie = pd.Series(lista, index=etichete)
# print(serie)

# dintr un numpy array

# array_date = np.array([10,20,30,40,50])
# serie = pd.Series(array_date)
# print(serie)

# dintr un dictionar
dict_date = {'a': [10], 'b': [20], 'c': [30], 'd': [40], 'e': [50]}
df = pd.DataFrame(dict_date)
print(df)



