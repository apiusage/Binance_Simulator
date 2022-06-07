import streamlit as st
from tradingView import *
from datetime import datetime
import requests
import json
import pandas as pd
from db import *
from styles import *

def spot():
    # coin selection
    coinName = selectCoin()
    bqAsset = getBaseQuoteAsset(coinName)
    baseAsset = str(bqAsset[0])
    quoteAsset = str(bqAsset[1])

    run_tradingView(coinName)

    active_tab = tabs(["Buy", "Sell", "Top up"])

    now = datetime.now()  # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    coin_transaction_date = date_time
    if active_tab == 'Buy':
        buySellOption(coin_transaction_date, "Buy", coinName, baseAsset, quoteAsset)
    elif active_tab == 'Sell':
        buySellOption(coin_transaction_date, "Sell", coinName, baseAsset, quoteAsset)
    elif active_tab == 'Top up':
        topUpAmount = st.number_input("Top up amount", min_value=0.0, key="topUpAmount")
        if st.button("Top up"):
            add_data(coin_transaction_date, "USDT", "", topUpAmount, "")
            usdtBal = get_coin_balance("USDT")
            totalUSDT = float(usdtBal[0][0]) + topUpAmount
            update_coin_balance("", str(totalUSDT), "", "USDT")
            st.success("USDT has been topped up successfully!")

            st.write("USDT Balance: " + str(usdtBal[0][0]))

    listing = view_all_data()
    df = pd.DataFrame(listing)
    df.columns = ['Date', 'Coin Name', 'Buy Price', 'Balance', 'Quote Price']
    st.info("Wallets")
    st.table(df[['Coin Name', 'Balance']])

    listing1 = view_all_transaction_data()
    df1 = pd.DataFrame(listing1)
    df1 = df1.reset_index(drop=True)
    df1.columns = ['buySellString', 'coin_transaction_date', 'baseAsset', \
                   'coinPrice', 'totalCoins', 'totalCost']
    # df1["coin_transaction_date"] = pd.to_datetime(df1["coin_transaction_date"])
    df1 = df1.sort_values(by="coin_transaction_date", ascending=False)
    st.info("Transaction")
    st.table(df1)

    if st.button('Drop Database'):
        drop_db()
        st.info("DB has been dropped!")

def selectCoin():
    marketpairsList = []
    dataMarketPairs = GetMarketPairs()
    for i in range(0, len(dataMarketPairs['symbols'])):
        marketpairsList.append(dataMarketPairs['symbols'][i]['symbol'])
    coinOption = st.multiselect("Select a coin", marketpairsList, default="BTCUSDT")
    coinName = str(coinOption[0])

    return coinName

def buySellOption(coin_transaction_date, buyOrSell, coinName, baseAsset, quoteAsset):
    totalCoins = 0
    option = st.selectbox('', ('Limit', 'Market', 'Stop Limit', 'OCO'))
    coinOrUSDT = st.selectbox("", ('Amount', 'Total'))

    coinPrice = getCoinLatestPrice(coinName)
    usdtBal = get_coin_balance("USDT")

    if coinOrUSDT == 'Amount':
        totalCoins = st.number_input(baseAsset, min_value=0.0, key="buyAmount")
    elif coinOrUSDT == 'Total':
        totalQuoteAsset = st.number_input(quoteAsset, min_value=0.0, key="buyTotal")
        totalCoins = float(totalQuoteAsset) / float(coinPrice)

    st.write("Avbl: ")
    st.select_slider('', options=['25%', '50%', '75%', '100%'])

    if buyOrSell == "Buy":
        if st.button('Buy'):
            buySell("Bought", coin_transaction_date, baseAsset, quoteAsset, coinPrice, totalCoins)
            st.success('Buy Successfully')
    if buyOrSell == "Sell":
        if st.button('Sell'):
            buySell("Sold", coin_transaction_date, baseAsset, quoteAsset, coinPrice, totalCoins)
            st.success('Sell Successfully')

def buySell(buySellString, coin_transaction_date, baseAsset, quoteAsset, coinPrice, totalCoins):
    add_data(coin_transaction_date, baseAsset, "", "0", "")
    add_data(coin_transaction_date, quoteAsset, "", "0", "")
    totalBaseAsset = get_coin_balance(baseAsset)
    totalQuoteAsset = get_coin_balance(quoteAsset)
    totalCostString = 0

    if buySellString == "Bought":
        totalBaseAsset = float(totalBaseAsset[0][0]) + totalCoins
        totalQuoteAsset = float(totalQuoteAsset[0][0]) - (float(coinPrice)*totalCoins)
    elif buySellString == "Sold":
        totalBaseAsset = float(totalBaseAsset[0][0]) - totalCoins
        totalQuoteAsset = float(totalQuoteAsset[0][0]) + (float(coinPrice)*totalCoins)

    # create transaction record to db
    totalCost = float(coinPrice) * float(totalCoins)
    totalCostString = str(totalCost) + " " + str(quoteAsset)
    add_transaction_data(buySellString, coin_transaction_date, baseAsset, coinPrice, totalCoins, totalCostString)

    quoteAssetString = str((float(coinPrice)*totalBaseAsset)) + " " + str(quoteAsset)

    update_coin_balance(coinPrice, str(totalQuoteAsset), "", quoteAsset)
    update_coin_balance(coinPrice, str(totalBaseAsset), quoteAssetString, baseAsset)

def GetMarketPairs():
    result = requests.get('https://api.binance.com/api/v3/exchangeInfo')
    if result.ok:
        json_data = json.loads(result.text)
        return json_data

def getBaseQuoteAsset(coinName):
    result = requests.get('https://api.binance.com/api/v3/exchangeInfo?symbol=' + coinName)
    if result.ok:
        json_data = json.loads(result.text)
        baseAsset = json_data["symbols"][0]["baseAsset"]
        quoteAsset = json_data["symbols"][0]["quoteAsset"]

    return [baseAsset, quoteAsset]

def getCoinLatestPrice(coinName):
    result = requests.get('https://api.binance.com/api/v3/ticker/price?symbol='+str(coinName))
    json_data = json.loads(result.text)
    return json_data["price"]