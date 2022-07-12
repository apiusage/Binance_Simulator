import streamlit as st
import sqlite3
from tradingView import *
import pandas as pd

conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()


def updateCryptoDB(buySellString, coinName, orderType, baseAsset, quoteAsset, coinPrice, totalCoins):
    totalBaseAsset = get_coin_balance(baseAsset)
    totalQuoteAsset = get_coin_balance(quoteAsset)

    if buySellString == "Buy":
        if st.button('Buy ' + baseAsset):
            totalQuoteAsset = totalQuoteAsset - (float(coinPrice) * totalCoins)
            if totalQuoteAsset < 0 or totalCoins == 0:
                st.warning("Buy failed , lack of " + str("{:.2f}".format(abs(totalQuoteAsset))) + " " + str(quoteAsset))
            else:
                totalBaseAsset = totalBaseAsset + totalCoins
                st.success('Buy Successfully')
                if orderType == 'Limit':
                    addLimitOrderToDB(buySellString, coinName, coinPrice)
                else:
                    updateDB(buySellString, coinName, orderType, baseAsset, quoteAsset, coinPrice, totalCoins,
                    totalBaseAsset, totalQuoteAsset)
    if buySellString == "Sell":
        if st.button('Sell ' + baseAsset):
            totalBaseAsset = totalBaseAsset - totalCoins
            if totalBaseAsset < 0 or totalCoins == 0:
                st.warning("Sell failed, lack of " + str("{:.2f}".format(abs(totalBaseAsset))) + " " + str(baseAsset))
            else:
                totalQuoteAsset = totalQuoteAsset + (float(coinPrice) * totalCoins)
                st.success('Sell Successfully')
                if orderType == 'Limit':
                    addLimitOrderToDB(buySellString, coinName, coinPrice)
                else:
                    updateDB(buySellString, coinName, orderType, baseAsset, quoteAsset, coinPrice, totalCoins,
                    totalBaseAsset, totalQuoteAsset)


def updateCryptoDBLimitOrder(buySellString, coinName, orderType, baseAsset, quoteAsset, coinPrice, totalCoins):
    totalBaseAsset = get_coin_balance(baseAsset)
    totalQuoteAsset = get_coin_balance(quoteAsset)
    totalCoins = float(totalCoins)

    if buySellString == "Buy":
        totalQuoteAsset = totalQuoteAsset - (float(coinPrice) * totalCoins)
        if totalQuoteAsset > 0 or totalCoins != 0:
            totalBaseAsset = totalBaseAsset + totalCoins
            updateDB(buySellString, coinName, orderType, baseAsset, quoteAsset, coinPrice, totalCoins,
                     totalBaseAsset, totalQuoteAsset)
    if buySellString == "Sell":
        totalBaseAsset = totalBaseAsset - totalCoins
        if totalBaseAsset > 0 or totalCoins != 0:
            totalQuoteAsset = totalQuoteAsset + (float(coinPrice) * totalCoins)
            updateDB(buySellString, coinName, orderType, baseAsset, quoteAsset, coinPrice, totalCoins,
                     totalBaseAsset, totalQuoteAsset)


def addLimitOrderToDB(buyOrSell, coinName, coinPrice):
    ID = select_next_highest_id_from_limitOrder()
    data = {'ID': str(int(ID)+1), 'Date': getTransactionDT(), 'Pair': coinName, 'Type': "Limit (Pending)",
            'Side': buyOrSell, 'Price': coinPrice, 'Amount': st.session_state.baseasset,
            'Filled': st.session_state.baseasset, 'Total': st.session_state.usdt, 'Trigger Conditions': 0}
    limitOrderList = list(data.values())
    add_limitorder_data(*limitOrderList)


def updateDB(buySellString, coinName, orderType, baseAsset, quoteAsset, coinPrice, totalCoins, totalBaseAsset,
             totalQuoteAsset):
    totalBaseString = str(totalCoins) + " " + str(baseAsset)
    totalCost = float(coinPrice) * float(totalCoins)
    totalCostString = str(totalCost) + " " + str(quoteAsset)
    add_transaction_data(buySellString, getTransactionDT(), coinName, orderType, coinPrice, totalBaseString, "0",
                         totalCostString)

    update_coin_balance(baseAsset, str(totalBaseAsset), baseAsset)
    update_coin_balance(quoteAsset, str(totalQuoteAsset), quoteAsset)


# ======================= CREATE ======================= #
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS \
        walletDB ( \
            coinName TEXT, \
            totalUnits TEXT \
  )')


def create_transaction_table():
    c.execute('CREATE TABLE IF NOT EXISTS \
        tradeHistoryDB ( \
            buySellString TEXT, \
            coin_transaction_date DATE, \
            coinPair TEXT, \
            orderType TEXT, \
            coinPrice TEXT, \
            coinQty TEXT, \
            fees TEXT, \
            totalCost TEXT \
  )')


def create_futures_transaction_table():
    c.execute('CREATE TABLE IF NOT EXISTS \
        futuresHistoryDB ( \
            buySellString TEXT, \
            coin_transaction_date DATE, \
            coinPair TEXT, \
            orderType TEXT, \
            coinPrice TEXT, \
            coinQty TEXT, \
            fees TEXT, \
            realizedProfit TEXT \
  )')


def create_limitorder_table():
    c.execute('CREATE TABLE IF NOT EXISTS \
        limitOrderDB ( \
            ID TEXT, \
            dateString DATE, \
            pair TEXT, \
            orderType TEXT, \
            side TEXT, \
            price TEXT, \
            amount TEXT, \
            filled TEXT, \
            total TEXT, \
            triggerConditions TEXT \
  )')


def create_favorites_table():
    c.execute('CREATE TABLE IF NOT EXISTS \
        favoritesDB ( \
            coinName TEXT \
  )')


# ======================= INSERT ======================= #
def add_data(*data):
    if not checkCoinExists(data[0]):
        c.execute('INSERT INTO walletDB (coinName, totalUnits) \
                    VALUES (?,?)', data)
    conn.commit()


def add_transaction_data(*data):
    c.execute('INSERT INTO tradeHistoryDB (buySellString, coin_transaction_date, coinPair, \
                    orderType, coinPrice, coinQty, fees, totalCost) \
                    VALUES (?,?,?,?,?,?,?,?)', data)
    conn.commit()


def add_futures_transaction_data(*data):
    c.execute('INSERT INTO futuresHistoryDB (buySellString, coin_transaction_date, coinPair, \
                    orderType, coinPrice, coinQty, fees, realizedProfit) \
                    VALUES (?,?,?,?,?,?,?,?)', data)
    conn.commit()


def add_limitorder_data(*data):
    c.execute('INSERT INTO LimitOrderDB (ID, dateString, pair, orderType, side, price,\
                amount, filled, total, triggerConditions) \
                VALUES (?,?,?,?,?,?,?,?,?,?)', data)
    conn.commit()


def addFavourites(*favorite):
    if not checkFavoritesExists(favorite[0]):
        c.execute('INSERT INTO favoritesDB (coinName) \
                    VALUES (?)', favorite)
    conn.commit()


# ======================= SELECT ======================= #
def checkFavoritesExists(coinName):
    c.execute('SELECT coinName FROM favoritesDB WHERE coinName = "{}"'.format(coinName))
    data = c.fetchall()
    return data


def checkCoinExists(coinName):
    c.execute('SELECT coinName FROM walletDB WHERE coinName = "{}"'.format(coinName))
    data = c.fetchall()
    return data


def select_next_highest_id_from_limitOrder():
    c.execute('SELECT MAX(ID) FROM LimitOrderDB')
    data = c.fetchall()
    if data[0][0]:
        return data[0][0]
    else:
        return '0'


def select_all_favourites():
    c.execute('SELECT coinName FROM favoritesDB')
    data = c.fetchall()
    return data


def select_all_limit_records():
    c.execute('SELECT * FROM LimitOrderDB')
    data = c.fetchall()
    return data


def view_all_favourites():
    c.execute('SELECT * FROM favoritesDB')
    data = c.fetchall()
    return data


def view_wallet_data():
    c.execute('SELECT * FROM walletDB')
    data = c.fetchall()
    return data


def get_coin_balance(coinName):
    c.execute('SELECT totalUnits FROM walletDB WHERE coinName = "{}"'.format(coinName))
    data = c.fetchall()
    return float(data[0][0])


def view_all_transaction_data():
    c.execute('SELECT * FROM tradeHistoryDB')
    data = c.fetchall()
    return data


def view_all_futures_transaction_data():
    c.execute('SELECT * FROM futuresHistoryDB')
    data = c.fetchall()
    return data


def get_coin_by_name(coin):
    c.execute('SELECT * FROM walletDB WHERE coinName = "{}"'.format(coin))
    data = c.fetchall()
    return data


# ======================= Update ======================= #
def update_coin_balance(*coinBalance):
    c.execute("UPDATE walletDB SET \
                coinName=?,\
                totalUnits=? WHERE \
                coinName=?", coinBalance)
    conn.commit()


# ======================= Drop ======================= #
def drop_db():
    c.execute('DELETE FROM walletDB')
    c.execute('DELETE FROM tradeHistoryDB')
    c.execute('DELETE FROM limitOrderDB')
    c.execute('DELETE FROM futuresHistoryDB')
    conn.commit()


# ======================= Others ======================= #
def delete_data_by_ID(ID):
    c.execute('DELETE FROM limitOrderDB WHERE ID = "{}"'.format(ID))
    conn.commit()


def edit_coin_data(*updatedData):
    c.execute("UPDATE walletDB SET \
                coinName=?,\
                totalUnits=? WHERE \
                coinName=?", updatedData)
    conn.commit()
    data = c.fetchall()
    return data


def delete_data(coin):
    c.execute('DELETE FROM walletDB WHERE coinName = "{}"'.format(coin))
    conn.commit()
