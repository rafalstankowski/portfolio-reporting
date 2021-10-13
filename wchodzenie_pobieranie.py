from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import datetime as dt
import os
import shutil

#Dane do logowania
login = input('Podaj login:\n')
passwrd = input('Podaj haslo:\n')

#Ustawianie dat i ilosc brakujacych raportow
time_max = dt.datetime.strptime('01/01/2000', '%d/%m/%Y').date()
path_data = r'E:\Self\data'
files = os.listdir(path_data)
for f in files:
    if 'Portfolio' in f:
        name, ext = os.path.splitext(f)
        # print(name[10:])
        czas = name[10:].replace('-', '/')
        czas = dt.datetime.strptime(czas, '%d/%m/%Y').date()
        # print(czas)
        if czas > time_max:
            time_max = czas
    else:
        pass

print(time_max)
wczoraj = dt.datetime.today().date() + dt.timedelta(days= -1)
diff = wczoraj - time_max
print(f'Brakujacych raportow: {diff.days}, ostatni jest za {time_max}')

#Wchodzenie na strone i logowanie
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--start-maximized')

    #Odpalanie przegladarki i odpowiedniej strony
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://www.degiro.pl/')
wait = WebDriverWait(driver, 20)
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/div/nav/div[1]/a[1]')))
driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div/nav/div[1]/a[1]').click()
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[2]/form/div[4]/button')))

    #Logowanie
driver.find_element_by_id('username').send_keys(login)
driver.find_element_by_id('password').send_keys(passwrd)
driver.find_element_by_xpath('/html/body/div[1]/div/main/div[2]/form/div[4]/button').click()
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="appContainer"]/div/aside/nav[1]/a[3]/i'))).click()
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mainContent"]/div[1]/section/div/section/div[1]/div/header/div/button/i'))).click()

i = 0
while i < diff.days:
    time_max = time_max + dt.timedelta(days=1)
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/i'))).click  # wybraniedaty
    driver.find_element_by_name('reportEndDate').send_keys(Keys.CONTROL + "a")
    driver.find_element_by_name('reportEndDate').send_keys(Keys.DELETE)
    driver.find_element_by_name('reportEndDate').send_keys(time_max.strftime('%d/%m/%Y'))
    driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div').click()

    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[2]/a[2]'))).click()  # sciaganie excela
    time.sleep(5)

    filename = 'Portfolio'
    ext = '.xls'
    file_new = filename + ' ' + f'{time_max.strftime("%d-%m-%Y")}' + f'{ext}'
    dl_path = r'C:\Users\John\Downloads\Portfolio.xls'
    dest_path = r'E:\Self\data'
    shutil.move(dl_path, os.path.join(dest_path, file_new))
    print(i, time_max)
    i += 1
    time.sleep(1)

driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="appContainer"]/div/aside/nav[2]/div[2]/button/i').click()
driver.close()
