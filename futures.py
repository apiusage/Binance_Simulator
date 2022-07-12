import streamlit as st
from styles import *
from spot import *
from db import *

# https://stackoverflow.com/questions/70648991/find-all-coins-available-for-futures-trading-from-binance

def futures():
    coinName = selectCoin()
    bqAsset = getBaseQuoteAsset(coinName)
    baseAsset = str(bqAsset[0])
    quoteAsset = str(bqAsset[1])

    streamCryptoPrice(coinName)
    run_tradingView(coinName)
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


def buySellOption(buyOrSell, coinName, baseAsset, quoteAsset):
    try:
        orderTypeSelected = orderTypes()

        if orderTypeSelected == 'Limit':
            lpmOrder(coinName, baseAsset, quoteAsset)
        elif orderTypeSelected == 'Post Only':
            lpmOrder(coinName, baseAsset, quoteAsset)
        elif orderTypeSelected == 'Market':
            marketOrder(buyOrSell, coinName, baseAsset, quoteAsset)
        elif orderTypeSelected == 'Stop Limit':
            slOrder(baseAsset, quoteAsset)
        elif orderTypeSelected == 'Stop Market':
            slOrder(baseAsset, quoteAsset)
        elif orderTypeSelected == 'Trailing Stop':
            trailingStop(baseAsset, quoteAsset)
        elif orderTypeSelected == 'TWAP':
            TWAP(baseAsset)
    except:
        pass

def lpmOrder(coinName, baseAsset, quoteAsset):
    coinPrice = getCoinLatestPrice(coinName)
    price = st.number_input("", format="%f", value=float(coinPrice), min_value=0.0,\
                            max_value=float(coinPrice), step=0.0, key="coinPrice")
    customMenu([baseAsset, quoteAsset])
    amount = st.text_input('', value=0.0, placeholder="Amount (" + baseAsset + ")", key="baseAssetAmount")
    usdtAmountUsed = getPercentage(get_coin_balance("USDT"))
    tpSLReduceOnly(quoteAsset)

def percentChange():
    try:
        percentage = st.session_state.percent.replace("%", "")
        st.session_state.qa = st.session_state.qavalue * (int(percentage) / 100)
        st.session_state.ba = st.session_state.qa / st.session_state.coinPrice
    except:
        pass

def updateQAChange():
    st.session_state.qa = st.session_state.ba * st.session_state.coinPrice

def updateBAChange():
    st.session_state.ba = st.session_state.qa / st.session_state.coinPrice


def marketOrder(buyOrSell, coinName, baseAsset, quoteAsset):
    baseAssetAmount = st.number_input('Amount (' + baseAsset + ')', value=0.0, key="ba", on_change=updateQAChange)
    quoteAssetAmount = st.number_input('Amount (' + quoteAsset + ')', value=0.0, key="qa", on_change=updateBAChange)

    st.select_slider('', value='100%', options=['0%', '25%', '50%', '75%', '100%'], key='percent', on_change=percentChange)
    getAvailableUSDT()
    if buyOrSell == 'Buy':
        if st.button('Buy'):
            longfuturesContract(coinName, baseAssetAmount, quoteAssetAmount)
    elif buyOrSell == 'Sell':
        if st.button('Sell'):
            shortfuturesContract(coinName, baseAssetAmount, quoteAssetAmount)


def slOrder(baseAsset, quoteAsset):
    customMenu(["Last", "Mark"])
    stopAmount = st.text_input('', placeholder="Stop (USDT)", key="stopUSDT")
    limitAmount = st.text_input('', placeholder="Limit (USDT)", key="limitUSDT")
    customMenu([baseAsset, quoteAsset])
    amount = st.text_input('', placeholder="Amount (" + baseAsset + ")", key="baseAssetAmount")
    usdtAmountUsed = getPercentage(get_coin_balance("USDT"))
    tpSLReduceOnly(quoteAsset)

def tpSLReduceOnly(quoteAsset):
    if st.checkbox('TP/SL'):
        takeProfit = st.text_input('', placeholder="Take Profit", key="takeProfit")
        stopLoss = st.text_input('', placeholder="Stop Loss", key="stopLoss")

    reduceOnly = st.checkbox("Reduce Only")

    st.write("Max: " + " " + quoteAsset)
    st.write("Cost: " + " " + " " + quoteAsset)

    # return [takeProfit, stopLoss, reduceOnly]

def trailingStop(baseAsset, quoteAsset):
    cbRate = st.text_input('', placeholder="C/B Rate", key="cbRate")
    percentage = st.radio('', ('1%', '2%'))
    customMenu(["Last", "Mark"])
    actPrice = st.text_input('', placeholder="Act. Price", key="cbRate")
    customMenu([baseAsset, quoteAsset])
    amount = st.text_input('', placeholder="Amount (" + baseAsset + ")", key="baseAssetAmount")
    usdtAmountUsed = getPercentage(get_coin_balance("USDT"))
    tpSLReduceOnly(quoteAsset)

def TWAP(baseAsset):
    customMenu(["Create", "Running", "History"])

    actPrice = st.text_input('', placeholder="Total Size", key="baseAsset")
    usdtAmountUsed = getPercentage(get_coin_balance("USDT"))
    duration = st.text_input('', placeholder="Duration", key="duration")
    customMenu(["1 h", "2 h", "12 h", "24 h"])
    reduceOnly = st.checkbox("Reduce-Only")
    if st.button("Buy Long"):
        st.write("long")
    if st.button("Sell Short"):
        st.write("short")

def orderTypes():
    orderType = st.selectbox('', ('Limit', 'Post Only', 'Market', 'Stop Limit', 'Stop Market', 'Trailing Stop', 'TWAP'), index=2)
    return orderType