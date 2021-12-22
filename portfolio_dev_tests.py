import pandas as pd
import yaml
import os

# config_localiation = os.path.join(os.getcwd(), 'config.yaml')
# config = open(config_localiation, 'r')
# config = yaml.safe_load(config)
#
# print(config)


path = 'E:\Self\deposits_withdraws.csv'

csv = pd.read_csv(path, delimiter= ',', parse_dates=['Date'])
# csv['Date'] = csv['Date'].astype('datetime64')

csv= csv.groupby(['Date']).sum()

csv["C"] = csv["Amount"].cumsum()
csv.reset_index(inplace=True)

print(csv)