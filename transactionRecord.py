import streamlit as st
import pandas as pd
from db import *

def transactionRecord():
    st.title("Spot")
    columnName = ['Side', 'Date', 'Pair', 'Order Type', 'Price', 'Filled', 'Fees', 'Total']
    tradeHistoryDB = view_all_transaction_data()
    tradeHistoryDF = pd.DataFrame(tradeHistoryDB, columns=columnName)
    tradeHistoryDF = tradeHistoryDF.set_index('Side')
    st.dataframe(tradeHistoryDF.sort_values(by="Date", ascending=False))

    st.title("Futures")
    columnName = ['Side', 'Date', 'Pair', 'Order Type', 'Price', 'Filled', 'Fees', 'Realized PNL']
    futuresHistoryDB = view_all_futures_transaction_data()
    futuresHistoryDF = pd.DataFrame(futuresHistoryDB, columns=columnName)
    futuresHistoryDF = futuresHistoryDF.set_index('Side')
    st.dataframe(futuresHistoryDF.sort_values(by="Date", ascending=False))

    if st.button('Drop Database'):
        drop_db()
        st.info("DB has been dropped!")
