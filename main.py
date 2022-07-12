import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

# Import pages
from db import *
from favorites import *
from spot import *
from futures import *
from wallet import *
from transactionRecord import *
from about import *

img = Image.open("images/bitcoin.png").convert('RGB').save('Logo.jpeg')
PAGE_CONFIG = {"page_title": "Trading Simulator", "page_icon": img, "layout": "centered",
               "initial_sidebar_state": "collapsed"}
st.set_page_config(**PAGE_CONFIG)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .css-qrbaxs {min-height: 0em;}
            .css-x46z32 {gap: 0rem;}
            .css-18e3th9 {padding: 2rem 1rem 10rem;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():
    # try:
    local_css("style.css")

    # create db
    create_table()
    create_transaction_table()
    create_favorites_table()
    create_limitorder_table()
    create_futures_transaction_table()
    add_data("USDT", "0")

    option = optionMenu()

    if option == "Favorites":
        favorites()
    elif option == "Spot":
        spot()
    elif option == "Futures":
        futures()
    elif option == "Wallet":
        wallet()
    elif option == "Transaction Record":
        transactionRecord()
    elif option == "About":
        about()


# except:
#   pass

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
