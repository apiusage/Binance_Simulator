from styles import *
from db import *
from tradingView import *
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import calendar


def spot():
    # coin selection
    coinName = selectCoin()
    bqAsset = getBaseQuoteAsset(coinName)
    baseAsset = str(bqAsset[0])
    quoteAsset = str(bqAsset[1])

    streamCryptoPrice(coinName)
    run_tradingView(coinName)
    # get quote asset price, should be streaming
    st.session_state.coinPrice = getCoinLatestPrice(coinName)
    add_data(baseAsset, "0")
    add_data(quoteAsset, "0")
    st.session_state.qavalue = get_coin_balance(quoteAsset)
    st.session_state.bavalue = get_coin_balance(baseAsset)

    buyOrSellOption = buySellButtons()
    if buyOrSellOption == 'Buy':
        buySellOption("Buy", coinName, baseAsset, quoteAsset)
    elif buyOrSellOption == 'Sell':
        buySellOption("Sell", coinName, baseAsset, quoteAsset)


def selectCoin():
    col1, col2 = st.columns(2)
    marketpairsList = []
    dataMarketPairs = GetMarketPairs()

    for i in range(0, len(dataMarketPairs['symbols'])):
        marketpairsList.append(dataMarketPairs['symbols'][i]['symbol'])

    with col1:
        coinOption = st.multiselect("", marketpairsList, default="BTCUSDT")
        coinName = str(coinOption[0])
    with col2:
        if st.button("⭐"):
            addFavourites(coinName)

    return coinName


def orderTypes():
    orderType = st.selectbox('', ('Limit', 'Market', 'Stop Limit', 'OCO'), index=2)
    return orderType


def getAvailableUSDT():
    st.write("Avbl: " + str("{:.2f}".format(get_coin_balance("USDT"))) + " USDT")


def buySellOption(buyOrSell, coinName, baseAsset, quoteAsset):
    # try:
    orderTypeSelected = orderTypes()

    if orderTypeSelected == 'Limit':
        limitOrder(buyOrSell, coinName, baseAsset, quoteAsset)
    elif orderTypeSelected == 'Market':
        marketOrder(buyOrSell, coinName, baseAsset, quoteAsset)
    elif orderTypeSelected == 'Stop Limit':
        stopLimitOrder(buyOrSell, coinName, baseAsset, quoteAsset)
    elif orderTypeSelected == 'OCO':
        ocoOrder(baseAsset)

# except:
#    pass

# =========================== Limit order =========================== #
def getBuyLimitOrderPercentage():
    if st.session_state.price > 0:
        percentage = st.session_state.percent.replace("%", "")
        st.session_state.usdt = (int(percentage) / 100) * st.session_state.qavalue
        st.session_state.baseasset = st.session_state.usdt / st.session_state.price


def getSellLimitOrderPercentage():
    if st.session_state.baseasset > 0:
        percentage = st.session_state.percent.replace("%", "")
        st.session_state.usdt = (int(percentage) / 100) * (st.session_state.bavalue * st.session_state.price)
        st.session_state.baseasset = st.session_state.usdt / st.session_state.price


def updatePrice():
    st.session_state.usdt = st.session_state.price * st.session_state.baseasset


# https://www.geeksforgeeks.org/different-ways-to-iterate-over-rows-in-pandas-dataframe/
def limitOrder(buyOrSell, coinName, baseAsset, quoteAsset):
    coinPrice = st.number_input('Price (' + baseAsset + ')', value=0.0, key="price", on_change=updatePrice)

    if buyOrSell == 'Buy':
        totalCoins = st.number_input('Amount (' + baseAsset + ')', value=0.0, key="baseasset", on_change=updatePrice)
        st.select_slider('', value='100%', options=['25%', '50%', '75%', '100%'], key='percent',
                         on_change=getBuyLimitOrderPercentage)
        st.number_input('', value=st.session_state.qavalue, key='usdt')
    elif buyOrSell == 'Sell':
        totalCoins = st.number_input('Amount (' + baseAsset + ')', value=st.session_state.bavalue, key="baseasset",
                                     on_change=updatePrice)
        st.select_slider('', value='100%', options=['25%', '50%', '75%', '100%'], key='percent',
                         on_change=getSellLimitOrderPercentage)
        st.number_input('', value=st.session_state.usdt, key='usdt')

    getAvailableUSDT()
    updateCryptoDB(buyOrSell, coinName, "Limit", baseAsset, quoteAsset, coinPrice, totalCoins)
    limitOrderDT = displayPendingLimitOrder()

    format_data = "%d/%m/%Y, %H:%M:%S"
    for index, row in limitOrderDT.iterrows():
        side = row["Side"]
        coinName = row["Pair"]
        orderType = row["Type"]
        bqAsset = getBaseQuoteAsset(coinName)
        baseAsset = str(bqAsset[0])
        quoteAsset = str(bqAsset[1])
        coinPrice = row["Price"]
        totalCoins = row["Amount"]

        dateString = datetime.strptime(row["Date"], format_data)
        d = dateString - timedelta(days=5)
        dateInMS = get_unix_ms_from_date(d)
        df = getKLineData(coinName, dateInMS)
        minimum = df[4].min()
        maximum = df[4].max()

        if float(minimum) <= float(coinPrice) <= float(maximum):
            updateCryptoDBLimitOrder(side, coinName, "Limit", baseAsset, quoteAsset, coinPrice, totalCoins)
            delete_data_by_ID(index)
            st.success("Limit order filled successfully")


def displayPendingLimitOrder():
    # Show pending limit orders
    columnName = ['ID', 'Date', 'Pair', 'Type', 'Side', 'Price', 'Amount', 'Filled', 'Total', 'Trigger Conditions']
    limitOrderDT = select_all_limit_records()
    limitOrderDT = pd.DataFrame(limitOrderDT, columns=columnName)
    limitOrderDT = limitOrderDT.set_index('ID')
    st.table(limitOrderDT)
    return limitOrderDT


# =========================== Market order =========================== #
def getBuyPercentage():
    percentage = st.session_state.percent.replace("%", "")
    st.session_state.qa = st.session_state.qavalue * (int(percentage) / 100)
    st.session_state.ba = st.session_state.qa / st.session_state.coinPrice


def getSellPercentage():
    percentage = st.session_state.percent.replace("%", "")
    st.session_state.ba = st.session_state.bavalue * (int(percentage) / 100)
    st.session_state.qa = st.session_state.ba * st.session_state.coinPrice


def updateAmount():
    st.session_state.ba = float(st.session_state.qa) / st.session_state.coinPrice


def updateTotal():
    st.session_state.qa = float(st.session_state.ba) * st.session_state.coinPrice


def marketOrder(buyOrSell, coinName, baseAsset, quoteAsset):
    totalCoins = st.number_input(baseAsset, key="ba", on_change=updateTotal)
    st.number_input(quoteAsset, key="qa", on_change=updateAmount)

    if buyOrSell == 'Buy':
        st.select_slider('', value='100%', options=['25%', '50%', '75%', '100%'], key='percent',
                         on_change=getBuyPercentage)
    elif buyOrSell == 'Sell':
        st.select_slider('', value='100%', options=['25%', '50%', '75%', '100%'], key='percent',
                         on_change=getSellPercentage)
    getAvailableUSDT()
    updateCryptoDB(buyOrSell, coinName, "Market", baseAsset, quoteAsset, st.session_state.coinPrice, totalCoins)


def updateTotalUSDT():
    st.session_state.totalUSDT = st.session_state.limitUSDT * st.session_state.baseAssetAmount


def stopLimitOrder(buyOrSell, coinName, baseAsset, quoteAsset):
    coinPrice = getCoinLatestPrice(coinName)
    stopAmount = st.text_input('', placeholder="Stop (USDT)", key="stopUSDT")
    limitAmount = st.number_input('Limit (USDT)', value=coinPrice, key="limitUSDT", on_change=updateTotalUSDT)
    amount = st.number_input("Amount (" + baseAsset + ")", key="baseAssetAmount", on_change=updateTotalUSDT)
    st.select_slider('', value='100%', options=['25%', '50%', '75%', '100%'], key='percent')
    totalUSDT = st.number_input('Total (USDT)', key="totalUSDT")
    getAvailableUSDT()
    updateCryptoDB(buyOrSell, coinName, "Stop Limit", baseAsset, quoteAsset, coinPrice, amount)


def ocoOrder(baseAsset):
    stopAmount = st.text_input('', placeholder="Price (USDT)", key="stopUSDT")
    limitAmount = st.text_input('', placeholder="Stop (USDT)", key="limitUSDT")
    limitAmount = st.text_input('', placeholder="Limit (USDT)", key="limitUSDT")
    amount = st.text_input('', placeholder="Amount (" + baseAsset + ")", key="baseAssetAmount")
    # usdtAmountUsed = getPercentage(get_coin_balance("USDT"))
    totalUSDT = st.text_input('', placeholder="Total (USDT)", key="totalUSDT")
    getAvailableUSDT()


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
    result = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=' + str(coinName))
    json_data = json.loads(result.text)
    return float(json_data["price"])


def getKLineData(coinPair, startDateMS):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': coinPair,
        'interval': '1m',
        'startTime': startDateMS,
        'endTime': getCurrentMS()
    }
    response = requests.get(url, params=params)
    df = pd.DataFrame.from_dict(response.json())
    return df


def getCurrentMS():
    return get_unix_ms_from_date(datetime.now())


# https://betterprogramming.pub/how-to-easily-fetch-your-binance-historical-trades-using-python-174a6569cebd
def get_unix_ms_from_date(date):
    return int(calendar.timegm(date.timetuple()) * 1000 + date.microsecond / 1000)
