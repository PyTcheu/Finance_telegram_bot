import pandas as pd # Para evitar escrever pandas e trocar pela escrita apenas de pd para facilitar
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import yfinance as yf 
import telegram
import requests
import telegram_send
import schedule
import time
import random
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pandas_datareader import data as web # Evita a escrita do data e troca pelo web
from datetime import datetime

#Token PRD
#token = '1796099831:AAGteQJXlcNd2dLSSq0kbbqa0QoV0B_xtTU'

#Token DEV
token = '1788977298:AAG7qKmlDhSazNpCMBjQ3GonWJzGLhj1Mno'
    
bot = telegram.Bot(token) #Replace TOKEN with your token string
updater = Updater(token=token, use_context=True) #Replace TOKEN with your token string

dispatcher = updater.dispatcher


def get_coin_bid(coin):
    response = requests.get('https://economia.awesomeapi.com.br/json/last/'+ coin)
    result = response.json()
    c = coin.replace('-','')
    return result[c]['bid']



def get_bdrs_price(paper):
    response = 'https://statusinvest.com.br/bdrs/' + paper
    result = requests.get(response)
    soup = BeautifulSoup(result.content, 'html.parser')
    stock_price = str(soup.find(class_='value')).split('>')[1].split('<')[0]
    var = str(soup.find(title='Variação do valor do ativo com base no dia anterior'))
    
    var = var.split('\n')[4].split('>')[1].split('<')[0]
        
    if not var.startswith('-'):
        var = '+' + var
            
    return stock_price, var


def get_fiis_price(paper):
    response = 'https://statusinvest.com.br/fundos-imobiliarios/' + paper
    result = requests.get(response)
    soup = BeautifulSoup(result.content, 'html.parser')
    stock_price = str(soup.find(class_='value'))
    var = str(soup.find(title='Variação do valor do ativo com base no dia anterior'))
    
    if stock_price == 'None':
        return get_bdrs_price(paper)
    else: 
        stock_price = stock_price.split('>')[1].split('<')[0]
        var = var.split('\n')[4].split('>')[1].split('<')[0]
        
        if not var.startswith('-'):
            var = '+' + var
            
        return stock_price, var

def get_stock_price(paper):
    response = 'https://statusinvest.com.br/acoes/' + paper
    result = requests.get(response)
    soup = BeautifulSoup(result.content, 'html.parser')
    stock_price = str(soup.find(class_='value'))
    var = str(soup.find(title='Variação do valor do ativo com base no dia anterior'))
    
    if stock_price == 'None':
        return get_fiis_price(paper)
    else: 
        
        stock_price = stock_price.split('>')[1].split('<')[0]
        var = var.split('\n')[4].split('>')[1].split('<')[0]
        
        if not var.startswith('-'):
            var = '+' + var
            
        return stock_price, var
    
    
def stock(update, context):
    paper = " ".join(context.args)
    value = get_stock_price(paper.lower())
    update.message.reply_text(paper.upper() + ": R$" + value[0] + '\n \n Variação do dia: ' + value[1])

def euro(update, context):
    eur = "Cotação do Euro Hoje: R$ " + str(get_coin_bid('EUR-BRL')).replace('.',',')
    context.bot.send_message(chat_id=update.effective_chat.id, text=eur)



def vilzyn(update, context):
    dol = "Cotação do Dolar Hoje: R$ " + str(get_coin_bid('USD-BRL')).replace('.',',')
    context.bot.send_message(chat_id=update.effective_chat.id, text=dol)


def dolar(update, context):
    dol = "Cotação do Dolar Hoje: R$ " + str(get_coin_bid('USD-BRL')).replace('.',',')
    context.bot.send_message(chat_id=update.effective_chat.id, text=dol)


def hey(update, context):
    photo = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRowHhdTB04EQSOcRuRTqLHvk96K4lS3UupYg&usqp=CAU', 'https://img.freepik.com/fotos-gratis/o-orangotango-jovem-sorriu-e-agiu-como_60359-323.jpg?size=626&ext=jpg', 'https://i.pinimg.com/originals/73/58/70/7358702b2780ce3933cf474c15035dde.jpg'] 
 
    caption = ['Eai Kamako', 'Aoba', 'Salve Kamakada'] 
     
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo = random.choice(photo), caption = random.choice(caption))


def chart(update, context):
    paper = " ".join(context.args)
    get_stock_chart(paper)
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(paper + '.png', 'rb'))
    os.remove(paper + '.png')


def get_stock_chart(paper):
    data = yf.download(
    tickers=paper + '.SA', 
    period="3mo",
    interval="1d")

    data = data.reset_index()
    data = data.rename(columns={data.columns[0]:'Date'})
    
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.write_image(paper + '.png')
    

dispatcher.add_handler(CommandHandler("hey", hey))

dispatcher.add_handler(CommandHandler('dolar', dolar))
dispatcher.add_handler(CommandHandler('euro', euro))
dispatcher.add_handler(CommandHandler('vilzyn', vilzyn))

dispatcher.add_handler(CommandHandler("stock", stock))
dispatcher.add_handler(CommandHandler("chart", chart))

updater.start_polling()