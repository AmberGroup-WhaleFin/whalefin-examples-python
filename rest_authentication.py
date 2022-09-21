import time
import hmac
import hashlib
import requests
import urllib.parse
import os
import sys
import logging

# Set your API_KEY in the OS environment
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
if(API_KEY is None or API_SECRET is None):
    print("Please set API_KEY and API_SECRET and re-run")
    sys.exit(1)

DEV_BASE_URI = "https://be-alpha.whalefin.com"
PROD_BASE_URI = "https://be.whalefin.com"
BASE_URI = PROD_BASE_URI

def query(urlPath = '/api/v2/trade/rfq', params = { "quantity": 10, "direction": "BUY", "symbol":"BTC_USD" }):
    method = 'GET'
    timestamp = int(time.time() * 1000)
    params = urllib.parse.urlencode(params)
    path = f'{urlPath}?{params}'

    # Create the query string for signing
    signStr = f'method={method}&path={path}&timestamp={timestamp}'

    # Encode the query string using SHA256 and your API_SECRET
    signature = hmac.new(bytes(API_SECRET, 'utf-8'), bytes(signStr, 'utf-8'), hashlib.sha256).hexdigest()

    # Set the request headers to include the signature, timestamp and your APIP KEY
    headers = {'access-key':API_KEY,'access-timestamp': str(timestamp),'access-sign':signature}

    # Call the API with the correct headers
    resp = requests.get(BASE_URI + path, headers=headers)
    
    # Do something with the results
    logging.info(resp.json())
    return {}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    options = sys.argv
    # Some example use cases
    if len(options) == 1 or options[1] == 'rfq':
        query()
    elif options[1] == 'earn':
        query('/api/v2/earn/products', {"type": "FIXED", "ccy": "BTC"})
    elif options[1] == 'symbols':
        query('/api/v2/trade/symbols')
    else:
        logging.info('Unknown Option')