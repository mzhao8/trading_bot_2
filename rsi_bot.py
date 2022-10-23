# conda activate finance
import websocket
import json
import pprint
import talib
import config
from binance.client import Client
from binance.enums import *
import numpy

client = Client(config.API_KEY, config.API_SECRET, tld="us")

# https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSD"
TRADE_QUANTITY = 0.015
in_position = False
closes = []
"""
{
  "e": "kline",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "k": {
    "t": 123400000, // Kline start time
    "T": 123460000, // Kline close time
    "s": "BNBBTC",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
}
"""

def order(side, symbol, quantity, order_type=ORDER_TYPE_MARKET) -> bool:
    try:
        print("sending")
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity
        )
        print(order)
    except Exception as e:
        print(f"an exception occured - {e}")
        return False
    return True

def on_open(ws):
    print("opened connection")


def on_close(ws):
    print("closed connection")


def on_message(ws, message):
    global closes, in_position

    print("received message")
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message["k"]

    is_candle_closed = candle["x"]
    close = candle["c"]

    if is_candle_closed:
        print(f"candle closed at {close}")
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsi's calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print(f"the current rsi is {last_rsi}")

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Sell!")
                    # put binance sell order logic here
                    order_succeeded = order(SIDE_SELL, TRADE_SYMBOL, TRADE_QUANTITY)
                    if order_succeeded:
                        in_position = False
                else:
                    print("Overbought, but you don't own it. Nothing to do.")

            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("Oversold, but you own it. Nothing to do.")
                else:
                    print("Buy!")
                    # put binance buy order logic here
                    order_succeeded = order(SIDE_BUY, TRADE_SYMBOL, TRADE_QUANTITY)
                    if order_succeeded:
                        in_position = True

ws = websocket.WebSocketApp(
    SOCKET, on_open=on_open, on_close=on_close, on_message=on_message
)
ws.run_forever()
