import streamlit as st
import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS \
        cryptoDB ( \
            coin_transaction_date DATE, \
            coinName TEXT, \
            price TEXT, \
            units TEXT, \
            quotePrice TEXT \
  )')

def create_transaction_table():
    c.execute('CREATE TABLE IF NOT EXISTS \
        transactionDB ( \
            buySellString TEXT, \
            coin_transaction_date DATE, \
            baseAsset TEXT, \
            coinPrice TEXT, \
            totalCoins TEXT, \
            totalCost TEXT \
  )')

def checkCoinExists(coinName):
    c.execute('SELECT coinName FROM cryptoDB WHERE coinName = "{}"'.format(coinName))
    data = c.fetchall()
    return data

def add_data(*data):
    if not checkCoinExists(data[1]):
        c.execute('INSERT INTO cryptoDB (coin_transaction_date, coinName, price, \
                    units, quotePrice) \
                    VALUES (?,?,?,?,?)', data)
    conn.commit()

def add_transaction_data(*data):
    c.execute('INSERT INTO transactionDB (buySellString, coin_transaction_date, baseAsset, \
                    coinPrice, totalCoins, totalCost) \
                    VALUES (?,?,?,?,?,?)', data)
    conn.commit()

def get_coin_balance(coinName):
    c.execute('SELECT units FROM cryptoDB WHERE coinName = "{}"'.format(coinName))
    data = c.fetchall()
    return data

def update_coin_balance(*usdtUpdate):
    c.execute("UPDATE cryptoDB SET \
                price=?,\
                units=?,\
                quotePrice=? WHERE \
                coinName=?", usdtUpdate)
    conn.commit()

def get_coin_by_name(coin):
    c.execute('SELECT * FROM cryptoDB WHERE coinName = "{}"'.format(coin))
    data = c.fetchall()
    return data

def view_all_data():
    c.execute('SELECT * FROM cryptoDB')
    data = c.fetchall()
    return data

def view_all_transaction_data():
    c.execute('SELECT * FROM transactionDB')
    data = c.fetchall()
    return data

def edit_coin_data(*updatedData):
    c.execute("UPDATE cryptoDB SET \
                sellPrice=?,\
                soldUnits=?,\
                totalSales=?,\
                profit=? WHERE \
                coinName=?", updatedData)
    conn.commit()
    data = c.fetchall()
    return data

def delete_data(coin):
    c.execute('DELETE FROM cryptoDB WHERE coinName = "{}"'.format(coin))
    conn.commit()

def drop_db():
    c.execute('DELETE FROM cryptoDB')
    c.execute('DELETE FROM transactionDB')
    conn.commit()
