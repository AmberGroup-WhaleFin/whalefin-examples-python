# whalefin-examples-python
Python examples for the Whalefin API

[Official Whalefin API Pages](https://pro.whalefin.com/apidoc/)

## Install Pre-Requisites
Requires websocket-client and rel to run
- pip install -r requirements

## Environment Variables
So as not to store API Keys and Secrets in the code, please set the following as OS environment variables:
- API_KEY
- API_SECRET

## Examples
- ### [websocket_marketdata.py](websocket_marketdata.py)
Logon and subscribe to Whalefin's Websocket market data feed.