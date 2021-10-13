import os
import pandas as pd
import numpy as np
import datetime as dt
import time
import requests
import json
import charts_tables_visualization as ctv


##########
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth= desired_width)
pd.set_option('display.max_columns',20)
##########

data_file = r'E:\Self\data.csv'
df = pd.read_csv(data_file, delimiter= ',', parse_dates= ['Data'])

time_last = df['Data'].max()
time_last = time_last.date() #data do petli while dla plikow
time_df_max = pd.to_datetime(time_last) #data do tabeli
df_time_max = df[df['Data'] == time_df_max]

path = r'E:\Self\data'
df_data = pd.DataFrame()
while time_last < dt.datetime.now().date():
    time_last = time_last + dt.timedelta(days= 1)
    file = 'Portfolio ' + f'{time_last.strftime("%d-%m-%Y")}' + '.xls'
    f_path = os.path.join(path, file)
    print(f_path)

    ###EUR rate
    try:
        if time_last.weekday() == 5:
            time_last_new = time_last + dt.timedelta(days= -1)
            eur_rate_link = 'http://api.nbp.pl/api/exchangerates/rates/a/eur/' + f'{time_last_new}' + '/?format=json'
            eur_json = requests.get(eur_rate_link).text
            eur_rate = json.loads(eur_json)
            eur_rate = eur_rate['rates'][0]['mid']
        elif time_last.weekday() == 6:
            time_last_new = time_last + dt.timedelta(days= -2)
            eur_rate_link = 'http://api.nbp.pl/api/exchangerates/rates/a/eur/' + f'{time_last_new}' + '/?format=json'
            eur_json = requests.get(eur_rate_link).text
            eur_rate = json.loads(eur_json)
            eur_rate = eur_rate['rates'][0]['mid']
        else:
            eur_rate_link = 'http://api.nbp.pl/api/exchangerates/rates/a/eur/' + f'{time_last}' + '/?format=json'
            eur_json = requests.get(eur_rate_link).text
            eur_rate = json.loads(eur_json)
            eur_rate = eur_rate['rates'][0]['mid']
    except json.decoder.JSONDecodeError:
        try:
            eur_rate = eur_rate  ### tutaj zrobic aby wyszukiwalo z
        except Exception:
            eur_rate = df['Kurs lokalnej waluty'][df['Data'] == df['Data'].max()]
    else:
        eur_rate = eur_rate

    ###USD rate

    try:
        usd_rate_link = 'http://api.nbp.pl/api/exchangerates/rates/a/usd/' + f'{time_last}' + '/?format=json'
        usd_json = requests.get(usd_rate_link).text
        usd_rate = json.loads(usd_json)
        usd_rate = usd_rate['rates'][0]['mid']
    except json.decoder.JSONDecodeError:
        try:
            usd_rate = usd_rate  ### tutaj zrobic aby wyszukiwalo z
        except Exception:
            usd_rate = 3
    else:
        usd_rate = usd_rate

    ###df with exchange rate
    df_kursy = pd.DataFrame({'Lokalna waluta': ['EUR', 'USD', 'PLN'], 'Kurs lokalnej waluty': [eur_rate, usd_rate, 1]})

    if os.path.exists(f_path) == True:
        df_time = pd.Series(time_last, name= 'Data')
        df_daily = pd.read_excel(f_path, sheet_name='Stan portfela')
        df_daily = df_daily.replace(['CASH & CASH FUND & FTX CASH (EUR)', 'CASH & CASH FUND & FTX CASH (PLN)'], 'Gotówka')

        df_wartosc = df_daily['Lokalna wartość'].str.split(expand=True)
        df_wartosc.columns = ['Lokalna waluta', 'Lokalna wartość']

        # df_waluta_krajowej = pd.Series('PLN', name= 'Waluta krajowa')

        df_daily.drop(['Symbol/ISIN', 'Lokalna wartość', 'Wartość w EUR'], axis='columns', inplace=True)
        df_daily = pd.concat([df_time, df_daily, df_wartosc], axis= 1)
        df_daily = pd.merge(df_daily, df_kursy, on='Lokalna waluta', how='inner')
        df_data = pd.concat([df_data, df_daily], axis= 0)
        time.sleep(1)
    else:
        print('Brak danych za ' + f'{time_last}')
        pass

###daily summary
df_data = pd.concat([df_time_max, df_data])
df_data['Suma'] = df_data['Suma'].replace(np.NaN, '1')
df_data['Kurs '] = df_data['Kurs '].replace(np.NaN, '1')
df_data.drop(['Akcje zmiana', 'Wartość w PLN zmiana', 'Akcje zmiana w %', 'Procent portfela'], axis='columns', inplace=True)
df_data = df_data.fillna(method= 'ffill')
df_data['Wartość w PLN'] = df_data['Lokalna wartość'].astype('float') * df_data['Kurs lokalnej waluty'].astype('float')
df_data['Data'] = df_data['Data'].astype('datetime64')
df_data['Suma'] = df_data['Suma'].astype('float64')
df_data['Lokalna wartość'] = df_data['Lokalna wartość'].astype('float64')

###daily changes
df_data_diff = df_data.copy()
df_data_diff2 = df_data.copy()
df_data_diff2['Data'] = df_data_diff2['Data'] + dt.timedelta(days=1)

df_merge = pd.merge(df_data_diff, df_data_diff2, how='inner', left_on= ['Data', 'Produkt'], right_on= ['Data', 'Produkt'])
df_merge['Akcje zmiana'] = df_merge['Suma_x'] - df_merge['Suma_y']
df_merge['Wartość w PLN zmiana'] = df_merge['Wartość w PLN_x'] - df_merge['Wartość w PLN_y']
df_merge['Akcje zmiana w %'] = (df_merge['Kurs _x'].astype('float64') / df_merge['Kurs _y'].astype('float64') - 1) * 100
df_merge['Zmiana ilości akcji'] = df_merge['Suma_x'] - df_merge['Suma_y']

df_group = df_data[['Data', 'Wartość w PLN']].groupby('Data').sum().reset_index()
df_merge = pd.merge(df_merge, df_group, how='left', on= 'Data')

df_merge['Procent portfela'] = df_merge['Wartość w PLN_x'] / df_merge['Wartość w PLN'] * 100
df_merge2 = df_merge.copy()
df_merge2['Data'] = df_merge2['Data'] + dt.timedelta(days=1)
df_merge = pd.merge(df_merge, df_merge2, how= 'left', left_on= ['Data', 'Produkt'], right_on= ['Data', 'Produkt'])
df_merge['Zmiana procentu portfela'] = df_merge['Procent portfela_x'] - df_merge['Procent portfela_y']

df_diffs = df_merge[['Data', 'Produkt', 'Akcje zmiana_x', 'Akcje zmiana w %_x', 'Wartość w PLN zmiana_x', 'Procent portfela_x', 'Zmiana procentu portfela', 'Zmiana ilości akcji_x']]
df_diffs.columns = ['Data', 'Produkt', 'Akcje zmiana', 'Akcje zmiana w %', 'Wartość w PLN zmiana', 'Procent portfela', 'Zmiana procentu portfela', 'Zmiana ilości akcji']
df_data = pd.merge(df_data, df_diffs, how= 'left', left_on= ['Data', 'Produkt'], right_on= ['Data', 'Produkt'])

###charts
df_chart1 = df_data[['Produkt', 'Procent portfela', 'Zmiana procentu portfela']][df_data['Data'] == df_data['Data'].max()].sort_values(by=['Procent portfela'], ascending= False)
ctv.chart1(df_chart1)

df_chart2 = df_data[['Produkt', 'Wartość w PLN', 'Wartość w PLN zmiana']][df_data['Data'] == df_data['Data'].max()].sort_values(by=['Wartość w PLN'], ascending= False)
ctv.chart2(df_chart2)

df_chart3 = df_data[['Produkt', 'Suma', 'Zmiana ilości akcji']][df_data['Data'] == df_data['Data'].max()].sort_values(by=['Suma'], ascending= False)
ctv.chart3(df_chart3)

###tables
df_table_topwin = df_data[['Produkt', 'Akcje zmiana w %']][df_data['Data'] == df_data['Data'].max()].sort_values(by= ['Akcje zmiana w %'], ascending= False)
ctv.table1(df_table_topwin)

df_table_toplose = df_data[['Produkt', 'Akcje zmiana w %']][df_data['Data'] == df_data['Data'].max()].sort_values(by= ['Akcje zmiana w %'])
ctv.table2(df_table_toplose)









# daily_file = r'E:\Self\daily_sum.csv'
# df_group_merge.to_csv(daily_file, mode='a', index = False, header=False)
# df_data.to_csv(data_file, mode= 'a', index= False, header= False)

# print(df_final)