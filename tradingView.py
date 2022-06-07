import streamlit as st
import streamlit.components.v1 as components

def run_tradingView(coinOption):
    components.html(
        """
            <div class="tradingview-widget-container">
              <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
              <script type="text/javascript">
              new TradingView.widget(
              {
              "width": 350,
              "height": 500,
              "symbol": "BINANCE:""" + coinOption + """", 
              "interval": "15",
              "timezone": "Asia/Singapore",
              "theme": "light",
              "style": "1",
              "locale": "en",
              "toolbar_bg": "#f1f3f6",
              "enable_publishing": false,
              "hide_legend": true,
              "save_image": false,
              "container_id": "tradingview_a7ac3"
            }
              );
              </script>
            </div>
        """,
        width=350,
        height=500
    )




