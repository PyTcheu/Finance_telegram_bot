import requests

def get_coin_bid(coin):
    response = requests.get('https://economia.awesomeapi.com.br/json/last/'+ coin)
    result = response.json()
    c = coin.replace('-','')
    return result[c]['bid']


def euro(update, context):
    eur = "Cotação do Euro Hoje: R$ " + str(get_coin_bid('EUR-BRL')).replace('.',',')
    context.bot.send_message(chat_id=update.effective_chat.id, text=eur)


def vilzyn(update, context):
    dol = "Cotação do Dolar Hoje: R$ " + str(get_coin_bid('USD-BRL')).replace('.',',')
    context.bot.send_message(chat_id=update.effective_chat.id, text=dol)

def dolar(update, context):
    dol = "Cotação do Dolar Hoje: R$ " + str(get_coin_bid('USD-BRL')).replace('.',',')
    context.bot.send_message(chat_id=update.effective_chat.id, text=dol)
    