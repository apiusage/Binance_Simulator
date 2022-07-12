import streamlit as st
import streamlit.components.v1 as stc
from streamlit_option_menu import option_menu
from spot import *

def displayPageTitle(title):
    LOGO_BANNER = """
        <div style="background-color:#464e5f;padding:3px;border-radius:15px 50px 30px 5px";>
        <h1 style="color:white;text-align:center;"> """ + title + """ </h1>
        </div> """
    stc.html(LOGO_BANNER, height=90)

def optionMenu():
    option = option_menu("Binance Simulator",
                         ["Favorites", "Spot", "Futures", "Wallet", "Transaction Record", "About"],
                         icons=['star-fill', 'graph-up', 'graph-up-arrow', 'wallet', 'card-checklist',
                                'question-circle'],
                         orientation="horizontal", menu_icon="currency-bitcoin", default_index=0,
                         styles={
                             "container": {"font-weight": "bold", "padding": "2!important", "background-color": "#fafafa"},
                             "icon": {"color": "orange", "font-size": "12px"},
                             "nav-link": {"font-size": "13px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "#02ab21"},
                         }
                         )
    return option

def buySellButtons():
    option = option_menu("",
                         ["Buy", "Sell"],
                         icons=['bag-fill', 'currency-dollar'],
                         orientation="horizontal", default_index=0,
                         styles={
                             "container": {"padding": "0!important", "background-color": "#fafafa"},
                             "icon": {"color": "orange", "font-size": "16px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "#FF0000", "border-radius": "15px / 50px"}
                         }
                         )
    return option

def customMenu(tabList):
    option = option_menu("",
                         tabList,
                         orientation="horizontal", default_index=0,
                         styles={
                             "container": {"padding": "0!important", "background-color": "#EEE"},
                             "icon": {"color": "orange", "font-size": "16px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#eee", "color": "#000000"},
                             "nav-link-selected": {"background-color": "#D3D3D3", "border-radius": "15px / 50px"}
                         }
                         )
    return option

