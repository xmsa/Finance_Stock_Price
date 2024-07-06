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


if __name__ == "__main__":
    sql = DataBase()
