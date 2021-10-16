import pandas as pd
import datetime as dt
import time
import requests
import json

def cur_rates(cur, df, time_last):
    cur_list = []
    rates = []
    for i in cur:
        if i == 'PLN':
            exchange_rate = 1
        else:
            try:
                if time_last.weekday() == 5:
                    time_last_new = time_last + dt.timedelta(days=-1)
                    exchange_rate_link = 'http://api.nbp.pl/api/exchangerates/rates/a/' + str(
                        i) + '/' + f'{time_last_new}' + '/?format=json'
                    exchange_json = requests.get(exchange_rate_link).text
                    exchange_rate = json.loads(exchange_json)
                    exchange_rate = exchange_rate['rates'][0]['mid']
                elif time_last.weekday() == 6:
                    time_last_new = time_last + dt.timedelta(days=-2)
                    exchange_rate_link = 'http://api.nbp.pl/api/exchangerates/rates/a/' + str(
                        i) + '/' + f'{time_last_new}' + '/?format=json'
                    exchange_json = requests.get(exchange_rate_link).text
                    exchange_rate = json.loads(exchange_json)
                    exchange_rate = exchange_rate['rates'][0]['mid']
                else:
                    exchange_rate_link = 'http://api.nbp.pl/api/exchangerates/rates/a/eur/' + f'{time_last}' + '/?format=json'
                    exchange_json = requests.get(exchange_rate_link).text
                    exchange_rate = json.loads(exchange_json)
                    exchange_rate = exchange_rate['rates'][0]['mid']
            except json.decoder.JSONDecodeError:
                # try:
                exchange_rate = exchange_rate
            except Exception:
                exchange_rate = df['Kurs lokalnej waluty'][df['Data'] == df['Data'].max()].reset_index(drop= True)
            # else:
            #     exchange_rate = df['Kurs lokalnej waluty'][df['Data'] == df['Data'].max()]
        cur_list.append(i)
        rates.append(exchange_rate)
        time.sleep(1)

    ###df with exchange rate
    df_kursy = pd.DataFrame({'Lokalna waluta': cur_list, 'Kurs lokalnej waluty': rates})
    return df_kursy
    cur_list.clear()
    rates.clear()