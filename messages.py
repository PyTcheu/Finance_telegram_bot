
import random
import house_pricing as hp

def help(update, context):
    text = "Olá Kamako, precisando de uma ajuda? Segue lista de comandos e parâmetros: \n\n"            "/dolar ou /vilzyn - Cotação atual do dólar \n"            "/euro - Cotação atual do Euro \n"            "/stock <ação> - Retorna o valor da ação e sua variação no dia \n"            "/chart <ação> - Retorna o gráfico da performance da ação e seu RSI \n"            "/simulate_fii <fii> <valor inicial> <meses> <aporte em cotas> - Realiza uma simulação de FIIs a longo prazo com determinado aporte em quantidade de cotas \n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def hey(update, context):
    photo = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRowHhdTB04EQSOcRuRTqLHvk96K4lS3UupYg&usqp=CAU', 'https://img.freepik.com/fotos-gratis/o-orangotango-jovem-sorriu-e-agiu-como_60359-323.jpg?size=626&ext=jpg', 'https://i.pinimg.com/originals/73/58/70/7358702b2780ce3933cf474c15035dde.jpg'] 
 
    caption = ['Eai Kamako', 'Aoba', 'Salve Kamakada'] 
     
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo = random.choice(photo), caption = random.choice(caption))

