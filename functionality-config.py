import yfinance as yf
import pandas as pd
import psycopg2 as dbEditor
from datetime import datetime, timedelta

def ticker_lookup():
    ticker = input("Enter the Ticker of the stock you would like to look up\n")
    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)
    close_df = pd.DataFrame()

    data = yf.download(ticker, start=start_date, end=end_date)
    close_df[ticker] = data['Close']

    print(close_df)

