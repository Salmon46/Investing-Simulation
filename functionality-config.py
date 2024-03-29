import yfinance as yf
import pandas as pd
import psycopg2 as dbEditor
from datetime import datetime, timedelta

initial_investment_id = 1

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


def buy():
    global initial_investment_id
    
    ticker = input("Enter the ticker of the stock you would like to buy\n")

    shares_bought = input("How many shares would you like to buy?\n")

    end_date = datetime.today()
    start_date = end_date - timedelta(days=1)
    data = yf.download(ticker, start_date, end_date)
    close_price_df = pd.DataFrame(data['Close'])
    close_price = float(close_price_df.iat[0, 0])

    money_spent = float(shares_bought)*float(close_price)

    sql = f'SELECT * FROM "Portfolio"' + f" WHERE ticker='{str(ticker)}'"
    cursor.execute(sql)
    result = cursor.fetchone()
    if(result):
        table_modification = f'UPDATE "Portfolio"' + f" SET shares_bought={float(result[3])+float(shares_bought)}, money_spent={float(result[2])+float(money_spent)}" + f" WHERE ticker='{ticker}'"
    else:
        sql = f'SELECT MAX(investment_id) FROM "Portfolio"'
        cursor.execute(sql)
        result2 = cursor.fetchone()
        if(result2[0] != None):
            table_modification = f'INSERT INTO "Portfolio" (investment_id, ticker, money_spent, shares_bought)' + f" VALUES ( {int(initial_investment_id)+int(result2[0])},'{str(ticker)}', {float(money_spent)}, {float(shares_bought)})"
        else:
            table_modification = f'INSERT INTO "Portfolio" (investment_id, ticker, money_spent, shares_bought)' + f" VALUES ( {int(initial_investment_id)},'{str(ticker)}', {float(money_spent)}, {float(shares_bought)})"

    cursor.execute(table_modification)
    connection_details.commit()
    cursor.close()
    connection_details.close()