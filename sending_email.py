from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import smtplib
import datetime as dt
import os
import yaml

#Configuration file
config = open(r'C:\Users\John\PycharmProjects\degiro\config.yaml', 'r')
config = yaml.safe_load(config)

yesterday = dt.datetime.today().date() + dt.timedelta(days= -1)
img_path = config['paths']['save_path']

img_list = []
for folder, dirs, files in os.walk(img_path):
    for filename in files:
        if str(yesterday) in filename:
            img_list.append(os.path.join(img_path, filename))

msg = MIMEMultipart()
password = config['pass']['sender']
msg['From'] = "codzienneraporty@gmail.com"
msg['To'] = "rstankowski90@gmail.com"
msg['Subject'] = f'Raport za dzień {yesterday}'

body = MIMEText('<p><img src="cid:testimage0" /><img src="cid:testimage1" /><img src="cid:testimage2" /><img src="cid:testimage3" /><img src="cid:testimage4" /></p>', _subtype='html')
msg.attach(body)

for i, pic in enumerate(img_list):
    fp = open(pic, 'rb')
    img_data = fp.read()
    img = MIMEImage(img_data, 'jpeg')
    img.add_header('Content-Id', f'<testimage{i}>')
    msg.attach(img)

server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
server.login(msg['From'], password)
server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()