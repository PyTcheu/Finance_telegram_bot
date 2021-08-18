from bs4 import BeautifulSoup
import requests



def stock(update, context):
    paper = " ".join(context.args)
    value = get_stock_price(paper.lower())
    update.message.reply_text(paper.upper() + ": R$" + str(value[0]) + '\n\nVariação do dia: ' + str(value[1]))


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


def simulate_fii(update, context):
    parameters = " ".join(context.args).split(' ')
    fii = fii_calculation(parameters[0], parameters[1], parameters[2], parameters[3])
    
    msg = "Investindo no Fundo {} com um valor inicial de R${}, "           "aportando com {} cotas ao mês, sob uma rentabilidade de {}% ao mês "           "durante {} meses, você terá R$ {} no fim do prazo e recebendo "           "R$ {} por mês!".format(
        parameters[0], parameters[1], parameters[3], fii[4], parameters[2], fii[2], fii[3])
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


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