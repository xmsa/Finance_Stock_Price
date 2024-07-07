import pandas as pd
import os
import sqlite3


class DataBase:
    def __init__(self, file_name='db.sqlite3'):
        self.file_name = file_name
        if self.checkDataBase():
            print('Connect to DataSet...')
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

    def check_table(self, table):
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
        if cursor.fetchall():
            print(f"Table {table} found")
            return True
        else:
            print(f"Table {table} not found")
            return False

    def add_table(self, table):
        if not self.check_table(table):
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

    def max_min_value(self, table, column):
        result = {"Max": None, "Min": None}
        if self.check_table(table):
            result = self.conn.execute(f'''
                SELECT MIN({column}), MAX({column}) FROM {table}
                                       ''').fetchone()
            result = {"Max": result[0], "Min": result[1]}
        return result

    def insert_data(self, df, table):
        for _, row in df.iterrows():
            self.conn.execute(f'''
            INSERT OR IGNORE INTO {table} (Date,Open,High,Low,Close,AdjClose,Volume) VALUES (?, ?, ?, ?,?, ? , ?)
            ''', (row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']))
        else:
            self.conn.commit()
            print("add all data")


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
