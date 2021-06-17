#!/usr/bin/env python
# coding: utf-8

# In[1]:


import telegram
import requests
import telegram_send

import schedule
import time
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# In[2]:


token = '1796099831:AAGteQJXlcNd2dLSSq0kbbqa0QoV0B_xtTU'
    
bot = telegram.Bot(token) #Replace TOKEN with your token string
updater = Updater(token=token, use_context=True) #Replace TOKEN with your token string

dispatcher = updater.dispatcher


# In[3]:


def get_coin_bid(coin):
    response = requests.get('https://economia.awesomeapi.com.br/json/last/'+ coin)
    result = response.json()
    c = coin.replace('-','')
    return result[c]['bid']


# In[4]:


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


# In[5]:


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
    


# In[6]:


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
    
    
    
    


# In[7]:


def stock(update, context):
    paper = " ".join(context.args)
    value = get_stock_price(paper.lower())
    update.message.reply_text(paper.upper() + ": R$" + value[0] + '\n \n Variação do dia: ' + value[1])


# In[8]:


def euro(update, context):
    eur = "Cotação do Euro Hoje: R$ " + str(get_coin_bid('EUR-BRL')).replace('.',',')
    context.bot.send_message(chat_id=update.effective_chat.id, text=eur)


# In[9]:


def vilzyn(update, context):
    dol = "Cotação do Dolar Hoje: R$ " + str(get_coin_bid('USD-BRL')).replace('.',',')
    context.bot.send_message(chat_id=update.effective_chat.id, text=dol)


# In[10]:


def dolar(update, context):
    dol = "Cotação do Dolar Hoje: R$ " + str(get_coin_bid('USD-BRL')).replace('.',',')
    context.bot.send_message(chat_id=update.effective_chat.id, text=dol)


# In[11]:


def hello(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Eai Kamako')


# In[12]:


def chart(update, context):
    paper = " ".join(context.args)
    get_stock_chart(paper)
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(paper + '.png', 'rb'))
    os.remove(paper + '.png')


# In[ ]:





# In[13]:


import pandas as pd # Para evitar escrever pandas e trocar pela escrita apenas de pd para facilitar
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import yfinance as yf 

from pandas_datareader import data as web # Evita a escrita do data e troca pelo web
from datetime import datetime


# def get_stock_chart(paper):
#     paper_data = yf.download(
#     tickers=paper + '.SA', 
#     period="1d",
#     interval="1m")
#     
#     plt.plot(paper_data['Close'])
#     plt.savefig(paper + '.png')
#     plt.clf()
#     return paper_data

# In[14]:


def get_stock_chart(paper):
    data = yf.download(
    tickers=paper + '.SA', 
    period="3mo",
    interval="1d")
    # Plot the close prices

    data = data.reset_index()
    data = data.rename(columns={data.columns[0]:'Date'})
    
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.write_image(paper + '.png')
    


# In[15]:


dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('dolar', dolar))
dispatcher.add_handler(CommandHandler('euro', euro))
dispatcher.add_handler(CommandHandler('vilzyn', vilzyn))

dispatcher.add_handler(CommandHandler("stock", stock))
dispatcher.add_handler(CommandHandler("chart", chart))


# In[16]:


updater.start_polling()


# In[ ]:





# In[ ]:




