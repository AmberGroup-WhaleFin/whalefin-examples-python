import websocket
import _thread
import time
import rel
import json
import os

# Set your API_KEY in the OS environment
API_KEY = os.environ.get('API_KEY')

# Choose your environment
# Remember - Prod and Dev keys are different
DEV_BASE_URI = "be-alpha.whalefin.com"
PROD_BASE_URI = "be.whalefin.com"
BASE_URI = PROD_BASE_URI

# Select a symbol to subscribe to
# Full list available from https://be.whalefin.com/api/v2/trade/symbols (requires login)
SYMBOL = "btc_usd"

def subscribe(ws):
    subscription = json.dumps({"type": "subscribe", "data": {"pre": "OrderbookL1", "contract": SYMBOL, "limit": 5}})
    ws.send(subscription)

def on_message(ws, message):
    print(message)
    msg = json.loads(message)
    if('login' == msg['type'] and 'success' == msg['data']):
        subscribe(ws)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    login = json.dumps({
        "type": "login",
        "data": { "accessKey": API_KEY },
    })
    ws.send(login)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://{base_uri}/ws/socket-api".format(base_uri=BASE_URI),
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()