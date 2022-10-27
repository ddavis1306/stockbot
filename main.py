#!/usr/bin/env python3

"""DARRYL DAVIS | MAIN SCRIPT FOR STOCKBOT"""
from config import api_key
import os
import json
import requests
import sendMsg
def main():
#from bestbuy.apis import BestBuy
    bb = api_key
    #print(bb)
    sku = input("please enter the sku you want to monitor \n")
    response_API = requests.get("https://api.bestbuy.com/v1/products/" + sku + ".json?apiKey=uKxiL0ChCxCWmxGLSLpIBHxS")
    print(response_API.status_code)
    DATA = response_API.json()
    #print(data)
    #^shows the entine json
    if DATA["onlineAvailability"] == True:
        print("its in stock")
        sendMsg.instock(DATA)
    else:
        print("OOS try again later")
    print(DATA["addToCartUrl"])
    print(DATA["onlineAvailability"])
    # parse_json = json.loads(data)
    # headphones = parse_json['products']['']
    # print(headphones)
    #test sku: 5901353 in stock | 6521517 sold out

main()