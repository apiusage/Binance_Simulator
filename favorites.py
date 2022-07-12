import streamlit as st
import pandas as pd
from db import *
from tradingView import *

def favorites():
    favoritesList = []
    favourites = select_all_favourites()
    aList = list(favourites)
    for i in range(len(favourites)):
        favoritesList.append(aList[i][0].lower() + "@ticker")

    webSocketStreams(str(favoritesList))

    # favouritesDF = pd.DataFrame(favourites, columns=['Coin'])
    # st.dataframe(favouritesDF)
