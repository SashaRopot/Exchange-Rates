import requests
from bs4 import BeautifulSoup
import time
import smtplib

class Currency:
    dollar_byn = 'https://myfin.by/converter/usd-byn/1'
    headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

    current_converted_price = 0
    difference = 5
    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(" byn", ""))


    def get_currency_price(self):
        full_page = requests.get(self.dollar_byn, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class": "converter-100__info-currency-bold"})
        return convert[0].text

    def check_currency(self):
        currency = float(self.get_currency_price().replace(" byn", ""))
        if currency >= self.current_converted_price + self.difference:
            print("Курс сильно вырос. Обрати внимание!")
            self.send_mail()
        elif currency <= self.current_converted_price - self.difference:
            print("Курс сильно упал. Обрати внимание!")
            self.send_mail()
        print("Сейчас 1 доллар равен " + str(currency))
        time.sleep(3)
        self.check_currency()

    def send_mail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('shurik7228610@gmail.com', 'mzgmlfdisjdnrofh')

        subject = 'Курс валют'
        body = 'Курс доллара изменился!'
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail(
            'shurik7228610@gmail.com',
            message
        )
        server.quit()

currency = Currency()
currency.check_currency()