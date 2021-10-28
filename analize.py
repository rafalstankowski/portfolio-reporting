import os
import pandas as pd
import numpy as np
import datetime as dt
import time
import visualization as v
import yaml
import functions
import openpyxl


##########Remove later only for project purposes
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth= desired_width)
pd.set_option('display.max_columns',20)
##########

#Configuration file
cwd = os.getcwd()
config_localiation = os.path.join(cwd, 'config.yaml')
config = open(config_localiation, 'r')
config = yaml.safe_load(config)

data_file = config['files']['data_file']
df = pd.read_csv(data_file, delimiter= ',', parse_dates= ['Data'])

yesterday = dt.datetime.today().date() + dt.timedelta(days= -1)
time_last = df['Data'].max()
time_last = time_last.date() #data do petli while dla plikow
time_df_max = pd.to_datetime(time_last) #data do tabeli
df_time_max = df[df['Data'] == time_df_max]

path = config['paths']['dest_path']
df_data = pd.DataFrame()

### lists for function cur_rates, for additional df to take last currency rate for errors
cur_list_helper = []
rates_helper = []
date_list_helper = []
df_currency_helper = pd.DataFrame()

while time_last < yesterday:
    time_last = time_last + dt.timedelta(days= 1)
    file = 'Portfolio ' + f'{time_last.strftime("%d-%m-%Y")}' + '.xls'
    f_path = os.path.join(path, file)
    print(f_path)

    if os.path.exists(f_path) == True:
        df_time = pd.Series(time_last, name= 'Data')
        df_daily = pd.read_excel(f_path, sheet_name='Stan portfela')
        df_daily = df_daily.replace(['CASH & CASH FUND & FTX CASH (EUR)', 'CASH & CASH FUND & FTX CASH (PLN)'], 'Gotówka')

        df_value = df_daily['Lokalna wartość'].str.split(expand=True)
        df_value.columns = ['Lokalna waluta', 'Lokalna wartość']

        cur = set(df_value['Lokalna waluta'])
        df_cur = functions.cur_rates(cur, df, time_last, cur_list_helper, rates_helper, date_list_helper)

        df_daily.drop(['Symbol/ISIN', 'Lokalna wartość', 'Wartość w EUR'], axis='columns', inplace=True)
        df_daily = pd.concat([df_time, df_daily, df_value], axis= 1)
        df_daily = pd.merge(df_daily, df_cur, on='Lokalna waluta', how='inner')
        df_data = pd.concat([df_data, df_daily], axis= 0)
        # time.sleep(1)
    else:
        print('Brak danych za ' + f'{time_last}')
        pass

###daily summary
df_data = pd.concat([df_time_max, df_data])
df_data['Suma'] = df_data['Suma'].replace(np.NaN, '1')
df_data['Kurs '] = df_data['Kurs '].replace(np.NaN, '1')
# df_proc_portfel = df_data[['Data', 'Procent portfela']] ####<<<<
df_data.drop(['Wartość w PLN zmiana', 'Akcje zmiana w %', 'Procent portfela', 'Zmiana procentu portfela', 'Zmiana ilości akcji'], axis='columns', inplace=True)
df_data = df_data.fillna(method= 'ffill')
df_data['Wartość w PLN'] = df_data['Lokalna wartość'].astype('float') * df_data['Kurs lokalnej waluty'].astype('float')
df_data['Data'] = df_data['Data'].astype('datetime64')
df_data['Suma'] = df_data['Suma'].astype('float64')
df_data['Lokalna wartość'] = df_data['Lokalna wartość'].astype('float64')

###daily changes
df_data_diff = df_data.copy()
df_data_diff2 = df_data.copy()
df_data_diff2['Data'] = df_data_diff2['Data'] + dt.timedelta(days=1)

df_merge = pd.merge(df_data_diff, df_data_diff2, how='left', left_on= ['Data', 'Produkt', 'Lokalna waluta'], right_on= ['Data', 'Produkt',  'Lokalna waluta'])
df_merge['Wartość w PLN zmiana'] = df_merge['Wartość w PLN_x'] - df_merge['Wartość w PLN_y']
df_merge['Akcje zmiana w %'] = (df_merge['Kurs _x'].astype('float64') / df_merge['Kurs _y'].astype('float64') - 1) * 100
df_merge['Zmiana ilości akcji'] = df_merge['Suma_x'] - df_merge['Suma_y']

df_group = df_data[['Data', 'Wartość w PLN']].groupby('Data').sum().reset_index()
df_merge = pd.merge(df_merge, df_group, how='left', on= 'Data')

df_merge['Procent portfela'] = df_merge['Wartość w PLN_x'] / df_merge['Wartość w PLN'] * 100
df_merge2 = df_merge.copy()
df_merge2['Data'] = df_merge2['Data'] + dt.timedelta(days=1)
df_merge = pd.merge(df_merge, df_merge2, how= 'left', left_on= ['Data', 'Produkt',  'Lokalna waluta'], right_on= ['Data', 'Produkt',  'Lokalna waluta'])
df_merge['Zmiana procentu portfela'] = df_merge['Procent portfela_x'] - df_merge['Procent portfela_y']

df_diffs = df_merge[['Data', 'Produkt', 'Akcje zmiana w %_x', 'Wartość w PLN zmiana_x', 'Procent portfela_x', 'Zmiana procentu portfela', 'Zmiana ilości akcji_x']]
df_diffs.columns = ['Data', 'Produkt', 'Akcje zmiana w %', 'Wartość w PLN zmiana', 'Procent portfela', 'Zmiana procentu portfela', 'Zmiana ilości akcji']
df_data = pd.merge(df_data, df_diffs, how= 'left', left_on= ['Data', 'Produkt'], right_on= ['Data', 'Produkt'])
df_data = df_data[df_data['Data'] != df_data['Data'].min()] ## dropping rows which are already in the file

###Daily total value and difference
df_group_prev = df_group.copy()
df_group_prev['Data'] = df_group_prev['Data'] + dt.timedelta(days=1)
df_group_merge = pd.merge(df_group, df_group_prev, how= 'left', left_on= ['Data'], right_on= ['Data'])
df_group_merge['Diff'] = df_group_merge['Wartość w PLN_x'] - df_group_merge['Wartość w PLN_y']
df_group_merge = df_group_merge[df_group_merge['Data'] != df_group_merge['Data'].min()]  ## dropping rows which are already in the file


###charts
df_chart1 = df_data[['Produkt', 'Procent portfela', 'Zmiana procentu portfela']][df_data['Data'] == df_data['Data'].max()].sort_values(by=['Procent portfela'], ascending= False)
v.chart1(df_chart1)

df_chart2 = df_data[['Produkt', 'Wartość w PLN', 'Wartość w PLN zmiana']][df_data['Data'] == df_data['Data'].max()].sort_values(by=['Wartość w PLN'], ascending= False)
v.chart2(df_chart2)

df_chart3 = df_data[['Produkt', 'Suma', 'Zmiana ilości akcji']][df_data['Data'] == df_data['Data'].max()].sort_values(by=['Suma'], ascending= False)
v.chart3(df_chart3)

###tables
df_table_topwin = df_data[['Produkt', 'Akcje zmiana w %']][df_data['Data'] == df_data['Data'].max()].sort_values(by= ['Akcje zmiana w %'], ascending= False)
v.table1(df_table_topwin)

df_table_toplose = df_data[['Produkt', 'Akcje zmiana w %']][df_data['Data'] == df_data['Data'].max()].sort_values(by= ['Akcje zmiana w %'])
v.table2(df_table_toplose)

daily_file = os.path.join(cwd, 'daily_sum.csv')
df_group_merge.to_csv(daily_file, mode='a', index = False, header=False)
df_data.to_csv(data_file, mode= 'a', index= False, header= False)