import streamlit as st
from spot import *
from db import *
from spot import *

def wallet():
    st.info("Top up USDT")
    totalUSDT = st.number_input("", min_value=0.0, key="usdt")
    add_data("USDT", totalUSDT)

    if st.button("Top up"):
        walletUSDT = get_coin_balance("USDT")
        walletUSDT = float(walletUSDT) + totalUSDT
        update_coin_balance("USDT", walletUSDT, "USDT")

    getAvailableUSDT()

    walletData = view_wallet_data()
    walletDF = pd.DataFrame(walletData, columns=['Coin', 'Total'])
    walletDF = walletDF.set_index('Coin')
    st.dataframe(walletDF)
