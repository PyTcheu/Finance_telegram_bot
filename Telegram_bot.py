import requests
import telegram_send

import schedule
import time

import os

from bs4 import BeautifulSoup

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

def send_periodic_message():
    dol = "Cotação do Dolar Hoje: R$ " + get_coin_bid('USD-BRL')
    eur = "Cotação do Euro Hoje: R$ " + get_coin_bid('EUR-BRL')
    petr4 = "PETR4: " + get_stock_price('petrobras-pn')
    vvar3 = "VVAR3: " + get_stock_price('via-varejo-sa')
    
    queue = [dol, eur, petr4, vvar3]
    
    full_message = 'Bom dia kamakada! Segue resumão de hoje: \n\n'
    for msg in queue:
        full_message += msg + '\n'
    
    print(full_message)
    telegram_send.send(messages=[full_message], conf='user1.conf')
    telegram_send.send(messages=[full_message], conf='user2.conf')

schedule.every(5).seconds.do(send_periodic_message)

while True:
    schedule.run_pending()
    time.sleep(1)

