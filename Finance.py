
import requests
from datetime import datetime
from DataBase import DataBase
import pandas as pd
import os


cache_file = ".cache/tmp_.csv"
address = "127.0.0.1"
port = "2080"


def check_Ticker(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch'
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False


def feach_Ticker(ticker, start=None, end=None):
    if not check_Ticker(ticker):
        return None
    if start is None:
        start = 0
    if end is None:
        end = int(datetime.now().timestamp() + 1)

    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={
        start}&period2={end}&interval=1d&events=history&includeAdjustedClose=true"
    # url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"

    # data = {
    #     'period1': start,
    #     'period2': end,
    #     'interval': '1d',
    #     'events': 'history',
    #     'includeAdjustedClose': 'true'
    # }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # response = requests.post(url, data=data,headers=header,proxies=dict(http=f'socks5://{address}:{port}'))
    response = requests.get(
        url, headers=header, proxies=dict(
            http=f'socks5://{address}:{port}'))

    if response.status_code == 200:
        with open(cache_file, 'w') as f:
            f.write(response.text)
        print("Download data and save...")
        return True

    else:
        return False


def save_to_database(ticker):
    if os.path.exists("./.cache/tmp_.csv"):
        sql = DataBase()
        sql.add_table(ticker)
        df = pd.read_csv("./.cache/tmp_.csv")
        sql.insert_data(df, ticker)
        os.remove("./.cache/tmp_.csv")
    else:
        print("Data not found")
        print("Please download data first")


def update_database(ticker):

    sql = DataBase()
    feach_Ticker(ticker)
    result = sql.max_min_value(ticker, "Date")
    feach_Ticker(ticker, start=result["Max"])
    df = pd.read_csv("./.cache/tmp_.csv")
    sql.insert_data(df, ticker)
    os.remove("./.cache/tmp_.csv")
    print("Update data")


if __name__ == '__main__':
    # print(check_Ticker('MSFT'))
    # print(check_Ticker('FAKE'))
    # print(feach_Ticker('MSFT'))
    # save_to_database('MSFT')
    update_database('MSFT')
    # pass
