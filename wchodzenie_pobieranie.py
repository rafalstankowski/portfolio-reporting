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
import yaml

#Data for log in
login = input('Podaj login:\n')
passwrd = input('Podaj haslo:\n')

#Configuration file
config = open(r'C:\Users\John\PycharmProjects\degiro\config.yaml', 'r')
config = yaml.safe_load(config)

#Setting dates and missing data files
time_max = dt.datetime.strptime('01/01/2000', '%d/%m/%Y').date()
path_data = config['paths']['dest_path']
files = os.listdir(path_data)
for f in files:
    if 'Portfolio' in f:
        name, ext = os.path.splitext(f)
        time = name[10:].replace('-', '/')
        time = dt.datetime.strptime(time, '%d/%m/%Y').date()
        if time > time_max:
            time_max = time
    else:
        pass

print(time_max)
yesterday = dt.datetime.today().date() + dt.timedelta(days= -1)
diff = yesterday - time_max
print(f'Brakujacych raportow: {diff.days}, ostatni jest za {time_max}')

#Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--start-maximized')

#Run browser and website
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://www.degiro.pl/')
wait = WebDriverWait(driver, 20)
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/div/nav/div[1]/a[1]')))
driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div/nav/div[1]/a[1]').click()
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[2]/form/div[4]/button')))

#Log in
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

    filename = config['files']['filename']
    ext = '.xls'
    file_new = filename + ' ' + f'{time_max.strftime("%d-%m-%Y")}' + f'{ext}'
    dl_path = config['paths']['dl_path']
    dest_path = config['paths']['dest_path']
    shutil.move(dl_path, os.path.join(dest_path, file_new))
    print(i, time_max)
    i += 1
    time.sleep(1)

driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="appContainer"]/div/aside/nav[2]/div[2]/button/i').click()
driver.close()
