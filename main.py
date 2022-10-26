#!/usr/bin/env/ python3
from config import api_key
import os
import json
import requests
#from bestbuy.apis import BestBuy
bb = api_key
#print(bb)
response_API = requests.get('https://api.bestbuy.com/v1/products((search=Sony)&freeShipping=true&(categoryPath.id=abcat0204000))?apiKey=uKxiL0ChCxCWmxGLSLpIBHxS&show=addToCartUrl&facet=inStoreAvailability,10&format=json')
print(response_API.status_code)
data = response_API.text
parse_json = json.loads(data)
headphones = parse_json['products'][0]
print(headphones)


