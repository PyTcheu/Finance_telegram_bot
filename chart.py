import yfinance as yf 
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def chart(update, context):
    paper = " ".join(context.args)
    get_stock_chart(paper)
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(paper + '.png', 'rb'))
    os.remove(paper + '.png')


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
    
