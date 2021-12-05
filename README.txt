Program do obliczania zysków i zmian w degiro. Poniżej instrukcja:
1. Aby program działał musisz mieć pliki:
	i) ChromeDriverManager (https://chromedriver.chromium.org)
	ii) konfiguracyjny: config.yaml
	iii) python: log_download.py, analize.py, functions.py, sending_e-mail.py (do wysyłki maila, nie jest obowiązkowy, jeśli chcesz go używać to na razie w kodzie należy zmienić odbiorcę)
	iv) excel: data.csv (z odpowiednimi kolumnami oraz w drugim wierszu jak na razie potrzebna jest data od której ma pobrać dane (tj. jesli chcemy aby pobrał dane od 2021-01-01 to data musi być 2020-12-31), daily_sum.csv z odpowiednimi kolumnami, gdzie wrzuci różnicę zysku dziennego
2. Aby uruchomić program musisz mieć:
	i) program PyCharm, ewentualnie zainstalowany python na komputerze
3. Lokalizacja plików:
	i) spójrz na lokalizację plików .csv w pliku konfiguracyjnym, jeśli chcesz ją zmienić zmień ją w pliku config.yaml
4. Przed uruchomieniem programu:
	i) sprawdź czy masz zainstalowane biblioteki w PyCharmie (File > Settings > Project > Python Interpreter > (naciskasz + i szukasz nazw bibliotek)
	ii) instalacja przez cmd prompt: python -m pip install "SomePackage"
	iii) bibloteki używane w plikach: webdriver_manager.chrome, selenium, time, datetime, os, shutil, yaml, pandas, numpy, requests, json, matplotlib.pyplot, email.mime.multipart, email.mime.image, email.mime.text, smtplib
5. Kolejność uruchamiania plików:
	i) log_download.py- poprosi Cię o podanie loginu i hasła do konta, zaloguje sie do deGiro i pobierze raporty, a na koniec się wyloguje
	ii) analize.py - połączy raporty w jedną dużą tabele i dokona obliczeń i zmian dla akcji, wygeneruje raporty dla ostatniego dostępnego dnia i zapisze dane w plikach .csv
	iii) sengind_e-mail.py - wyśle do ciebie maila z poczty codzienneraporty@gmail.com z załącznikami w treści maila z tematem gdzie będzie wpisana data za dany raport.