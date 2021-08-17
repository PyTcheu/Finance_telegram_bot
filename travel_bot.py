#!/usr/bin/env python
# coding: utf-8

import telegram


from telegram.ext import Updater, CommandHandler

from messages import help, hey
from stock import stock, simulate_fii
from chart import chart
from coin import vilzyn, dolar, euro
from house_pricing import predict_house_price

token = '1796099831:AAHUR1939omXqYfVf_CsyxeiH184IWmiNU4'
    
bot = telegram.Bot(token) #Replace TOKEN with your token string
updater = Updater(token=token, use_context=True) #Replace TOKEN with your token string

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("help", help))

dispatcher.add_handler(CommandHandler("hey", hey))
dispatcher.add_handler(CommandHandler('dolar', dolar))
dispatcher.add_handler(CommandHandler('euro', euro))
dispatcher.add_handler(CommandHandler('vilzyn', vilzyn))

dispatcher.add_handler(CommandHandler("stock", stock))
dispatcher.add_handler(CommandHandler("chart", chart))

dispatcher.add_handler(CommandHandler("simulate_fii", simulate_fii))

dispatcher.add_handler(CommandHandler("predict_house_price", predict_house_price))

updater.start_polling()
