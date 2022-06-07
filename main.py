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
from styles import *

img = Image.open("images/bitcoin.png").convert('RGB').save('Logo.jpeg')
PAGE_CONFIG = {"page_title": "Trading Simulator", "page_icon":img, "layout":"wide", "initial_sidebar_state": "expanded" }
st.set_page_config(**PAGE_CONFIG)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():
    try:
        # create db
        create_table()
        create_transaction_table()

        with st.sidebar:
            option = optionMenu()

        if option == "Favorites":
            displayPageTitle("Favorites")
            favorites()
        elif option == "Spot":
            displayPageTitle("Spot Trading")
            spot()
        elif option == "Futures":
            displayPageTitle("Futures Trading")
            futures()
        elif option == "Wallet":
            displayPageTitle("Wallet")
            wallet()
        elif option == "Transaction Record":
            displayPageTitle("Transaction Record")
            transactionRecord()
        elif option == "About":
            displayPageTitle("About Binance Simulator")
            about()

    except:
        pass

def optionMenu():
    option = option_menu("Binance",
                         ["Favorites", "Spot", "Futures", "Wallet", "Transaction Record", "About"],
                         icons=['star-fill', 'graph-up', 'graph-up-arrow', 'wallet', 'card-checklist',
                                'question-circle'],
                         menu_icon="currency-bitcoin", default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "#fafafa"},
                             "icon": {"color": "orange", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "#02ab21"},
                         }
                         )
    return option

if __name__ == '__main__':
    main()










