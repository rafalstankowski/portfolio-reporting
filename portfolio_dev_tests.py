import pandas as pd


path = 'E:\Self\deposits_withdraws.csv'

csv = pd.read_csv(path, delimiter= ',')
# csv['Date'] = csv['Date'].astype('datetime64')

csv= csv.groupby(['Date']).sum()

csv["C"] = csv["Amount"].cumsum()

print(csv)