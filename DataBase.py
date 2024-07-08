import pandas as pd
import os
import sqlite3


class DataBase:
    def __init__(self, file_name='db.sqlite3'):
        self.file_name = file_name
        if self.checkDataBase():
            print('Connect to Database...')
            self.conn = sqlite3.connect(self.file_name)
        else:
            self.createDataBase()
            print('Database created')

    def checkDataBase(self):
        return os.path.exists(self.file_name)

    def createDataBase(self):
        flag = input("Do you want to create a new database? [Y/n]")
        if flag.lower() == "y" or flag == "":
            self.conn = sqlite3.connect(self.file_name)
        else:
            print('Exit...')
            exit()

    def __del__(self):
        self.conn.close()

    def __check_table(self, table):
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
        return bool(cursor.fetchone())

    def check_table(func):
        def wrapper(self, table, *args, **kwargs):
            if self.__check_table(table):
                return func(self, table, *args, **kwargs)
            else:
                print(f"Table {table} not found")
                return False
        return wrapper

    @check_table
    def add_table(self, table):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            CREATE TABLE {table} (
                Date DATE PRIMARY KEY,
                Open REAL,
                High REAL,
                Low REAL,
                Close REAL,
                AdjClose REAL,
                Volume REAL
            )
        ''')
        print("Create table")

    @check_table
    def max_min_value(self, table, column):
        result = self.conn.execute(f'''
            SELECT MIN({column}), MAX({column}) FROM {table}
                                   ''').fetchone()
        return {"Max": result[1], "Min": result[0]}

    @check_table
    def insert_data(self, df, table):
        for _, row in df.iterrows():
            self.conn.execute(f'''
            INSERT OR IGNORE INTO {table} (Date,Open,High,Low,Close,AdjClose,Volume) VALUES (?, ?, ?, ?,?, ? , ?)
            ''', (row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']))
        self.conn.commit()
        print("add all data")

    @check_table
    def select_data(self, table, start=None, end=None):
        cursor = self.conn.cursor()
        result = self.max_min_value(table, "Date")
        if start is None:
            start = result["Min"]
        if end is None:
            end = result["Max"]

        query = f"SELECT * FROM {table} WHERE Date BETWEEN '{start}' AND '{end}'"

        cursor.execute(query)

        rows = cursor.fetchall()
        df = pd.DataFrame(
            rows,
            columns=[
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "AdjClose",
                "Volume"])
        df.set_index("Date", inplace=True)
        return df


if __name__ == "__main__":
    sql = DataBase()
    table = "MSFT"
    column = "Date"
    # sql.add_table(table)
    # sql.check_table(table)
    # df = pd.read_csv("./.cache/tmp_.csv")
    # print(df.columns)
    # sql.insert_data(df, table)

    # result = sql.max_min_value(table, column)
    # print(result)
    # result = sql.select_data(table, start="2024-06-28",end="2024-07-03")
    # print(result)
