import yfinance as yf
import pandas as pd
import psycopg2 as dbEditor
from datetime import datetime, timedelta

connection_details = dbEditor.connect(
    host="ceu9lmqblp8t3q.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
    database="d2o7fsji8voktj",
    user="u9ssoi3qi31nm8", 
    password="pd754de5e907f36c44793b6f4472fc3dd6e09ef86c61d0da2fd7afb648fbfcc97", 
    port="5432"
)
cursor = connection_details.cursor()

def ticker_lookup():
    ticker = input("Enter the ticker of the stock you would like to look up\n")
    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)

    data = yf.download(ticker, start_date, end_date)
    close_prices_df= pd.DataFrame(data['Close'])

    print(close_prices_df)

ticker_lookup() #just used for tests
def buy():
    ticker = input("Enter the ticker of the stock you would like to buy\n")
    end_date = datetime.today()
    start_date = end_date - timedelta(days=1)

    data = yf.download(ticker, start_date, end_date)
    close_price_df = pd.DataFrame(data['Close'])

    close_price = float(close_price_df.iat[0, 0])
    print(close_price)