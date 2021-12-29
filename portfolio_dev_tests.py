import pandas as pd
import yaml
import os
import numpy as np

# config_localiation = os.path.join(os.getcwd(), 'config.yaml')
# config = open(config_localiation, 'r')
# config = yaml.safe_load(config)
#
# print(config)
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth= desired_width)
pd.set_option('display.max_columns',20)

path = 'E:\Self\data.csv'

csv = pd.read_csv(path, delimiter= ',', parse_dates=['Data'])
csv = csv[csv['Data'] == '12.02.2021']
csv['Wartość w PLN zmiana'] = csv['Wartość w PLN zmiana'].fillna(csv['Wartość w PLN'])
print(csv)