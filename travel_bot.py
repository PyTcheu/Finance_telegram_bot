#!/usr/bin/env python
# coding: utf-8

# In[1]:


import telegram
import requests
import pandas as pd # Para evitar escrever pandas e trocar pela escrita apenas de pd para facilitar
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import yfinance as yf 
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import stockstats
import random 

from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pandas_datareader import data as web # Evita a escrita do data e troca pelo web
from datetime import datetime
from stockstats import StockDataFrame
from plotly.subplots import make_subplots


# In[2]:


token = '1796099831:AAELnNVjGV1dVwYGpk4ZG08jZciUbvgp4UM'
    
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
    response = 'https://www.fundsexplorer.com.br/funds/' + paper
    result = requests.get(response)
    soup = BeautifulSoup(result.content, 'html.parser')
    
    stock_price = str(soup.find(class_='price'))
    var = str(soup.find(class_='percentage positive'))
    div_yield = str(soup.find_all(class_='indicator-value')[2])
    
    
    if stock_price == 'None':
        return get_bdrs_price(paper)
            
    else: 
        stock_price = float(stock_price.split('\n')[1].split('$')[1].strip().replace(',','.'))
        var = ''
        div_yield = float(div_yield.split('\n')[1].strip().replace('%','').replace(',','.'))/100
        
            
        return stock_price, var, div_yield


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
        
        stock_price = float(stock_price.split('>')[1].split('<')[0].replace(',','.'))
        var = var.split('\n')[4].split('>')[1].split('<')[0]
        
        if not var.startswith('-'):
            var = '+' + var
            
        return stock_price, var
    
    
    
    


# In[7]:


def stock(update, context):
    paper = " ".join(context.args)
    value = get_stock_price(paper.lower())
    update.message.reply_text(paper.upper() + ": R$" + str(value[0]) + '\n\nVariação do dia: ' + str(value[1]))


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


def chart(update, context):
    paper = " ".join(context.args)
    get_stock_chart(paper)
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(paper + '.png', 'rb'))
    os.remove(paper + '.png')


# In[12]:


def hey(update, context):
    photo = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRowHhdTB04EQSOcRuRTqLHvk96K4lS3UupYg&usqp=CAU', 'https://img.freepik.com/fotos-gratis/o-orangotango-jovem-sorriu-e-agiu-como_60359-323.jpg?size=626&ext=jpg', 'https://i.pinimg.com/originals/73/58/70/7358702b2780ce3933cf474c15035dde.jpg'] 
 
    caption = ['Eai Kamako', 'Aoba', 'Salve Kamakada'] 
     
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo = random.choice(photo), caption = random.choice(caption))


# In[13]:


def simulate_fii(update, context):
    parameters = " ".join(context.args).split(' ')
    fii = fii_calculation(parameters[0], parameters[1], parameters[2], parameters[3])
    
    msg = "Investindo no Fundo {} com um valor inicial de R${}, "           "aportando com {} cotas ao mês, sob uma rentabilidade de {}% ao mês "           "durante {} meses, você terá R$ {} no fim do prazo e recebendo "           "R$ {} por mês!".format(
        parameters[0], parameters[1], parameters[3], fii[4], parameters[2], fii[2], fii[3])
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


# In[14]:


def help(update, context):
    text = "Olá Kamako, precisando de uma ajuda? Segue lista de comandos e parâmetros: \n\n"            "/dolar ou /vilzyn - Cotação atual do dólar \n"            "/euro - Cotação atual do Euro \n"            "/stock <ação> - Retorna o valor da ação e sua variação no dia \n"            "/chart <ação> - Retorna o gráfico da performance da ação e seu RSI \n"            "/simulate_fii <fii> <valor inicial> <meses> <aporte em cotas> - Realiza uma simulação de FIIs a longo prazo com determinado aporte em quantidade de cotas \n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


# In[15]:


def fii_calculation(paper, valor_inicial, tempo_mes, aporte):
    valor_cota = int(get_fiis_price(paper.lower())[0])
    taxa = float(get_fiis_price(paper.lower())[2])
    acumulado = 0
    total = float(valor_inicial)
    aporte = int(aporte)
    for i in range (int(tempo_mes)):
        acumulado += total * taxa
        total += aporte * valor_cota
        if acumulado >= valor_cota:
            total += (acumulado//valor_cota) * valor_cota
            acumulado = acumulado - ((acumulado//valor_cota) * valor_cota)
    total_bruto = total + acumulado
    return round(total,2), round(acumulado,2), round(total_bruto,2), round(total*taxa,2), taxa*100


# In[ ]:





# In[16]:


def get_stock_chart(paper):
    data = yf.download(
    tickers=paper + '.SA', 
    period="1wk",
    interval="15m")
    # Plot the close prices
    
    data_rsi = yf.download(
    tickers=paper + '.SA', 
    period="2mo",
    interval="1d")
    
    
    rsi = calculate_RSI(data_rsi)
    
    data = data.reset_index()
    data = data.rename(columns={data.columns[0]:'Date'})
    
    fig = make_subplots(rows=2, cols=1, row_heights=[0.6, 0.4], subplot_titles=("Variação", "RSI"))

    fig.add_trace(
        go.Candlestick(x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Variation'),
            row=1, col=1)
    
    fig.add_trace(
        go.Scatter(x=rsi['Date'], y=rsi['RSI'], name='RSI'),
            row=2, col=1)
    
    fig.update_coloraxes(colorbar_tickfont_color='gray')
    
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(paper_bgcolor='#000326')
    fig.update_layout(font_color='white')
    fig.update_layout(plot_bgcolor='#000326')
    
    fig.update_xaxes(rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
            #dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
            ], row=1, col=1)
    
    fig.update_yaxes(range=[0,100], row=2, col=1)
    fig.update_yaxes(tickmode = 'array',tickvals = [0, 30, 70, 100], row=2, col=1)
        
    fig.write_image(paper + '.png')


# In[17]:


def calculate_RSI(data_rsi, n=14):
    delta = data_rsi['Adj Close'].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)
    ema_up = up.ewm(com=n-1, adjust=False).mean()
    ema_down = down.ewm(com=n-1, adjust=False).mean()
    rs = ema_up/ema_down
    data_rsi['RSI'] = 100 - (100/(1 + rs))
    data_rsi = data_rsi.iloc[14:]
    data_rsi = data_rsi.reset_index()
    return data_rsi
    


# In[ ]:





# In[ ]:





# In[18]:


dispatcher.add_handler(CommandHandler("help", help))

dispatcher.add_handler(CommandHandler("hey", hey))
dispatcher.add_handler(CommandHandler('dolar', dolar))
dispatcher.add_handler(CommandHandler('euro', euro))
dispatcher.add_handler(CommandHandler('vilzyn', vilzyn))

dispatcher.add_handler(CommandHandler("stock", stock))
dispatcher.add_handler(CommandHandler("chart", chart))

dispatcher.add_handler(CommandHandler("simulate_fii", simulate_fii))


# In[19]:


updater.start_polling()


# In[ ]:




