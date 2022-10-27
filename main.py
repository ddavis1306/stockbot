#!/usr/bin/env python3
from config import api_key
import os
import json
import requests
#from bestbuy.apis import BestBuy
bb = api_key
#print(bb)
sku = input("please enter the sku you want to monitor \n")
response_API = requests.get("https://api.bestbuy.com/v1/products/" + sku + ".json?apiKey=uKxiL0ChCxCWmxGLSLpIBHxS")
print(response_API.status_code)
data = response_API.json()
print(data)
print(data["addToCartUrl"])
print(data["onlineAvailability"])
# parse_json = json.loads(data)
# headphones = parse_json['products']['']
# print(headphones)