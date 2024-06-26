import yfinance as yf
import pandas as pd
import psycopg2 as dbEditor
from datetime import datetime, timedelta
import time

initial_investment_id = 1

connection_details = dbEditor.connect( #IMPORTANT!!!: This database connection is unaccurate since it has been detached from the project. 
    host="ceu9lmqblp8t3q.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
    database="d2o7fsji8voktj",
    user="u9ssoi3qi31nm8", 
    password="pd754de5e907f36c44793b6f4472fc3dd6e09ef86c61d0da2fd7afb648fbfcc97", 
    port="5432"
)
cursor = connection_details.cursor()

def ticker_lookup(tickerr):
    ticker = tickerr
    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)

    data = yf.download(ticker, start_date, end_date)
    close_prices_df= pd.DataFrame(data['Close'])
    close_price = round(float(close_prices_df.iat[0,0]), 2)

    return close_price

def portfolio_update():
    sql = 'SELECT ticker FROM "Portfolio"'
    cursor.execute(sql)
    ticker_tuple = cursor.fetchall()

    sql2 = 'SELECT shares_owned FROM "Portfolio"'
    cursor.execute(sql2)
    shares_owned_tuple = cursor.fetchall()

    for x in ticker_tuple:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=1)
        data = yf.download(x[0],start_date, end_date)
        close_price_df = pd.DataFrame(data['Close'])
        close_price = float(close_price_df.iat[0, 0])

        index = int(ticker_tuple.index(x))

        sql3 = f'UPDATE "Portfolio"' + f" SET investment_value='{int(float(close_price)*float(shares_owned_tuple[index][0]))}'" + f"WHERE ticker='{x[0]}'"
        cursor.execute(sql3)
        connection_details.commit()

def retrieve_values():
    sql = 'SELECT ticker, shares_owned, investment_value FROM "Portfolio"'
    cursor.execute(sql)
    result = cursor.fetchall()

    return result

def buy(ticker, shares_bought):
    global initial_investment_id

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
        table_modification = f'UPDATE "Portfolio"' + f" SET shares_owned={float(result[3])+float(shares_bought)}" + f" WHERE ticker='{ticker}'"
    else:
        sql = f'SELECT MAX(investment_id) FROM "Portfolio"'
        cursor.execute(sql)
        result2 = cursor.fetchone()
        if(result2[0] != None):
            table_modification = f'INSERT INTO "Portfolio" (investment_id, ticker, investment_value, shares_owned)' + f" VALUES ( {int(initial_investment_id)+int(result2[0])},'{str(ticker)}', {float(money_spent)}, {float(shares_bought)})"
        else:
            table_modification = f'INSERT INTO "Portfolio" (investment_id, ticker, investment_value, shares_owned)' + f" VALUES ( {int(initial_investment_id)},'{str(ticker)}', {float(money_spent)}, {float(shares_bought)})"

    cursor.execute(table_modification)
    connection_details.commit()

def sell(ticker, shares_sold):
    sql = f'SELECT shares_owned FROM "Portfolio"' + f" WHERE ticker='{ticker}'"
    cursor.execute(sql)
    result = cursor.fetchall()

    sql2 = f'UPDATE "Portfolio"' + f" SET shares_owned={result[0][0]-shares_sold}" + f" WHERE ticker='{ticker}'"
    cursor.execute(sql2)
    connection_details.commit()