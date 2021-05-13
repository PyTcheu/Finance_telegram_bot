import requests
import telegram_send
import schedule
import time
import os
from bs4 import BeautifulSoup

CONFS = ['user1.conf','user2.conf','user3.conf','user4.conf']

COINS = {'Dolar':'USD-BRL',
         'Euro':'EUR-BRL'}

STOCKS = {'VVAR3':'via-varejo-sa',
          'PETR4':'petrobras-pn'}


def get_coin_bid(coin):
    response = requests.get('https://economia.awesomeapi.com.br/json/last/'+ coin)
    result = response.json()
    c = coin.replace('-','')
    return result[c]['bid']

def get_stock_price(paper):
    response = 'https://br.investing.com/equities/' + paper
    result = requests.get(response)
    soup = BeautifulSoup(result.content, 'html.parser')
    stock_price = str(soup.find(class_='instrument-price_last__KQzyA'))
    
    return stock_price.split('>')[1].split('<')[0]

def form_message():
    full_message = 'Bom dia! Segue resumão de hoje: \n\n'
    full_message += '\n Moedas: \n'

    for k, v in COINS.items():
        full_message += "Cotação do  " + k + " hoje: R$ " + get_coin_bid(v) + '\n'

    full_message += '\n Acões: \n'

    for k, v in STOCKS.items():
        full_message += k + " : R$ " + get_stock_price(v) + '\n'

    return full_message
    

def send_periodic_message():

    
    full_msg = form_message()
    
    print(full_msg)

    for user in CONFS:
        telegram_send.send(messages=[full_msg], conf=user)

schedule.every(5).seconds.do(send_periodic_message)

while True:
    schedule.run_pending()
    time.sleep(1)

