# https://www.youtube.com/watch?v=HdZLDXtF_rQ
# https://www.youtube.com/watch?v=z2ePTq-KTzQ
# https://docs.streamlit.io/library/api-reference/layout/st.empty

import streamlit.components.v1 as components
from datetime import datetime
import pytz

def getTransactionDT():
    now = datetime.now()  # current date and time
    coin_transaction_DT = now.strftime("%d/%m/%Y, %H:%M:%S")
    return coin_transaction_DT

def run_tradingView(coinOption):
    components.html(
        """
            <div class="tradingview-widget-container">
              <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
              <script type="text/javascript">
              new TradingView.widget(
              {
              "width": 350,
              "height": 400,
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
        height=400
    )


# https://www.youtube.com/watch?v=XXuUNZIQUVA
def streamCryptoPrice(coinName):
    components.html(
        """
        <h1 id ="crypto-price" style ="font-family: Inter,ui-sans-serif,system-ui,Helvetica,Arial,sans-serif;">---</span> 
        <script type="text/javascript">
        let ws = new WebSocket('wss://stream.binance.com:9443/ws/""" + coinName.lower() + """@trade');
        let cryptoPriceElement = document.getElementById('crypto-price');
        let lastPrice = null;

        ws.onmessage = (event) => {
            let cryptoObject = JSON.parse(event.data);
            let price = parseFloat(cryptoObject.p)
            cryptoPriceElement.innerText = price;
            cryptoPriceElement.style.color = !lastPrice || lastPrice === price ? 'black' : price > lastPrice ? 'green': 'red';
            lastPrice = price;
        }
        </script>
        """,
        height=60,
    )


# https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-streams
# https://www.w3schools.com/jsref/prop_style_aligncontent.asp
def webSocketStreams(coinList):
    components.html(
        """
        Total <span id="totalstreams"></span> Coins<br/>

        <div id="streams" style="text-align-last: justify; font-weight:bold;">Coin Price Volume Percent</div>
        <script type="text/javascript">
            let streams = """ + coinList + """;

              let trackedStreams = [];

              let ws = new WebSocket("wss://stream.binance.com:9443/ws/" + streams.join('/'));
              // let ws = new WebSocket("wss://stream.binance.com:9443/ws/!miniTicker@arr");

              ws.onopen = function() {
                  console.log("Binance connected...");
              };

              ws.onmessage = function(evt) {
                try {
                  let msgs = JSON.parse(evt.data);
                  if (Array.isArray(msgs)) {
                    for (let msg of msgs) {
                      handleMessage(msg);
                    }
                  } else {
                    handleMessage(msgs)
                  }
                } catch (e) {
                  console.log('Unknown message: ' + evt.data, e);
                }
              }

              ws.onclose = function() {
                console.log("Binance disconnected");
              }

              function handleMessage(msg) {
                const coinName = msg.s;
                if (trackedStreams.indexOf(coinName) === -1) {
                  document.getElementById('streams').innerHTML += '<br/><br/>' + coinName + 
                  ' <span id="closePrice_' + coinName + '"></span>' + ' ' + 
                  '<span id="volume_' + coinName + '"></span>' + ' ' +
                  '<span style = "color: white; border-radius: 3px; padding: 5px" id="percentChange_' + coinName + '"></span>'; 
                    
                  trackedStreams.push(coinName);
                  document.getElementById('totalstreams').innerText = trackedStreams.length;
                }
                
                document.getElementById('closePrice_' + coinName).innerText = parseFloat(msg.c).toFixed(4);
                document.getElementById('volume_' + coinName).innerText = parseFloat(msg.v).toFixed(2);
                document.getElementById('percentChange_' + coinName).innerText = parseFloat(msg.P).toFixed(2) +'%';

                let closePrice = document.getElementById('closePrice_' + coinName);
                closePrice.style.color = msg.c === 0 ? 'grey' : msg.c > 0 ? 'green': 'red';

                let percentChange = document.getElementById('percentChange_' + coinName);
                percentChange.style.backgroundColor = !msg.P || msg.P === 0 ? 'grey' : msg.P > 0 ? '#32CD32': 'red';
                percentChange.style.style.padding = "10px";
              }
              
        </script>
        """,
        height=1000,
    )


def longfuturesContract(coinName, baseAssetAmount, quoteAssetAmount):
    components.html(
        """
        <style>
            .slidecontainer {
              width: 100%;
            }
            
            .slider {
              -webkit-appearance: none;
              width: 100%;
              height: 25px;
              background: #d3d3d3;
              outline: none;
              opacity: 0.7;
              -webkit-transition: .2s;
              transition: opacity .2s;
            }
            
            .slider:hover {
              opacity: 1;
            }
            
            .slider::-webkit-slider-thumb {
              -webkit-appearance: none;
              appearance: none;
              width: 25px;
              height: 25px;
              background: #04AA6D;
              cursor: pointer;
            }
            
            .slider::-moz-range-thumb {
              width: 25px;
              height: 25px;
              background: #04AA6D;
              cursor: pointer;
            }
        </style>
        <div class="slidecontainer">
            <input type="range" min="1" max="125" value="50" class="slider" id="myRange">
            <h4>""" + coinName + """ Perpetual <span id="demo"></span>x (LONG) !!!</h4> 
        </div>
        <table>
          <tr>
            <th>Unrealized PNL (USDT)</th>
            <th></th>
            <th>ROE</th>
          </tr>
          <tr>
            <td id = "pnl" style="font-weight:bold";>---</td>
            <th></th>
            <td id = "roe" style="font-weight:bold";>---</td>
          </tr>
          <tr>
            <td>Size</td>
            <td>Margin (USDT)</td>
            <td>Risk</td>
          </tr>
          <tr>
            <td>""" + str(baseAssetAmount) + """</td>
            <td>""" + str(round(quoteAssetAmount, 2)) + """</td>
            <td id ="risk"></td>
          </tr>
          <tr>
            <td>Entry Price</td>
            <td>Mark Price</td>
            <td>Liq Price</td>
          </tr>
          <tr>
            <td id ="entry-price"></td>
            <td id ="crypto-price"></td>
            <td id ="liq-price"></td>
           </tr>
        </table>
        
        <script type="text/javascript">
            let entryPrice = 0
            let pnlElement = document.getElementById('pnl');
            var slider = document.getElementById("myRange");
            var output = document.getElementById("demo");
            output.innerHTML = slider.value;
            slider.oninput = function() {
              output.innerHTML = this.value;
            }
            
            let ws = new WebSocket('wss://stream.binance.com:9443/ws/""" + coinName.lower() + """@trade');
            fetch('https://api.binance.com/api/v3/ticker/price?symbol=""" + coinName.upper() + """')
            .then(response =>{
                return response.json();
            }).then(data =>{
                entryPrice = data["price"];
                let entryPriceElement = document.getElementById('entry-price');
                entryPriceElement.innerText = parseFloat(entryPrice).toFixed(2);
            })
            let cryptoPriceElement = document.getElementById('crypto-price');
            let roeElement = document.getElementById('roe');
            let lastPrice = null;

            ws.onmessage = (event) => {
                let cryptoObject = JSON.parse(event.data);
                let price = parseFloat(cryptoObject.p)
                liquidationPrice = entryPrice - (entryPrice / parseFloat(slider.value));
                let liqPriceElement = document.getElementById('liq-price');
                liqPriceElement.innerText = parseFloat(liquidationPrice).toFixed(2);
                
                risk = (1 - (liquidationPrice / entryPrice)) * 100;
                let riskElement = document.getElementById('risk');
                riskElement.innerText = Math.abs(parseFloat(risk).toFixed(2)) + "%";
                
                cryptoPriceElement.innerText = price;
                roeValue = parseFloat((((price / entryPrice) - 1) * 100) * slider.value).toFixed(2);
                roeElement.innerText = roeValue + "%";
                pnlElement.innerText = parseFloat((price - entryPrice) * slider.value).toFixed(2);
                cryptoPriceElement.style.color = !lastPrice || lastPrice === price ? 'black' : price > lastPrice ? 'green': 'red';
                pnlElement.style.color = !entryPrice || price === entryPrice ? 'black' : price > entryPrice ? 'green': 'red';
                roeElement.style.color = roeValue >= 0 ? 'green' : 'red';
                lastPrice = price;
            }
        </script>
            
        <span>TP/SL:</span>
        """,
        height=1000,
    )


def shortfuturesContract(coinName, baseAssetAmount, quoteAssetAmount):
    components.html(
        """
        <style>
            .slidecontainer {
              width: 100%;
            }

            .slider {
              -webkit-appearance: none;
              width: 100%;
              height: 25px;
              background: #d3d3d3;
              outline: none;
              opacity: 0.7;
              -webkit-transition: .2s;
              transition: opacity .2s;
            }

            .slider:hover {
              opacity: 1;
            }

            .slider::-webkit-slider-thumb {
              -webkit-appearance: none;
              appearance: none;
              width: 25px;
              height: 25px;
              background: #04AA6D;
              cursor: pointer;
            }

            .slider::-moz-range-thumb {
              width: 25px;
              height: 25px;
              background: #04AA6D;
              cursor: pointer;
            }
        </style>
        <div class="slidecontainer">
            <input type="range" min="1" max="125" value="50" class="slider" id="myRange">
            <h4>""" + coinName + """ Perpetual <span id="demo"></span>x (SHORT) !!!</h4> 
        </div>
        <table>
          <tr>
            <th>Unrealized PNL (USDT)</th>
            <th></th>
            <th>ROE</th>
          </tr>
          <tr>
            <td id = "pnl" style="font-weight:bold";>---</td>
            <th></th>
            <td id = "roe" style="font-weight:bold";>---</td>
          </tr>
          <tr>
            <td>Size</td>
            <td>Margin (USDT)</td>
            <td>Risk</td>
          </tr>
          <tr>
            <td>""" + str(baseAssetAmount) + """</td>
            <td>""" + str(round(quoteAssetAmount, 2)) + """</td>
            <td id ="risk"></td>
          </tr>
          <tr>
            <td>Entry Price</td>
            <td>Mark Price</td>
            <td>Liq Price</td>
          </tr>
          <tr>
            <td id ="entry-price"></td>
            <td id ="crypto-price"></td>
            <td id ="liq-price"></td>
           </tr>
        </table>

        <script type="text/javascript">
            let entryPrice = 0
            let pnlElement = document.getElementById('pnl');
            var slider = document.getElementById("myRange");
            var output = document.getElementById("demo");
            output.innerHTML = slider.value;
            slider.oninput = function() {
              output.innerHTML = this.value;
            }

            let ws = new WebSocket('wss://stream.binance.com:9443/ws/""" + coinName.lower() + """@trade');
            fetch('https://api.binance.com/api/v3/ticker/price?symbol=""" + coinName.upper() + """')
            .then(response =>{
                return response.json();
            }).then(data =>{
                entryPrice = data["price"];
                let entryPriceElement = document.getElementById('entry-price');
                entryPriceElement.innerText = parseFloat(entryPrice).toFixed(2);
            })
            let cryptoPriceElement = document.getElementById('crypto-price');
            let roeElement = document.getElementById('roe');
            let lastPrice = null;

            ws.onmessage = (event) => {
                let cryptoObject = JSON.parse(event.data);
                let price = parseFloat(cryptoObject.p)
                liquidationPrice = parseFloat(entryPrice) + (parseFloat(entryPrice) / parseFloat(slider.value));
                let liqPriceElement = document.getElementById('liq-price');
                liqPriceElement.innerText = parseFloat(liquidationPrice).toFixed(2);
                
                risk = (1 - (entryPrice / liquidationPrice)) * 100;
                let riskElement = document.getElementById('risk');
                riskElement.innerText = Math.abs(parseFloat(risk).toFixed(2)) + "%";
                
                cryptoPriceElement.innerText = price;
                roeValue = parseFloat((((entryPrice / price) - 1) * 100) * slider.value).toFixed(2);
                roeElement.innerText = roeValue + "%";
                pnlElement.innerText = parseFloat((entryPrice - price) * slider.value).toFixed(2);
                cryptoPriceElement.style.color = !lastPrice || lastPrice === price ? 'black' : price > lastPrice ? 'green': 'red';
                pnlElement.style.color = !entryPrice || price === entryPrice ? 'black' : price < entryPrice ? 'green': 'red';
                roeElement.style.color = roeValue >= 0 ? 'green' : 'red';
                lastPrice = price;
            }
        </script>

        <span>TP/SL:</span>
        """,
        height=1000,
    )

