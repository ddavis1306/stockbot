#!/usr/bin/env python3

"""DARRYL DAVIS | MAIN SCRIPT FOR STOCKBOT"""
from config import api_key
import os
import json
import requests
from twilio.rest import Client
from config import account_sid
from config import auth_token
# import sendMsg
def main():

    bb = api_key
    #pop dashes and parens from inputted number. Create logic: if blank dont run text function
    yourNum = input("Please enter your phone number ###-###-####.To opt out of text updates, leave blank. \n>")
    #create logic: if email entered run send email function. elif null dont send email function
    yourEmail = input("Please enter your email. To opt out of email updates, leave blank.")
    #enter sku to monitor
    sku = input("Please enter the sku you want to monitor \n>")
    response_API = requests.get("https://api.bestbuy.com/v1/products/" + sku + ".json?apiKey=" + bb)
    print(response_API.status_code) 
    data = response_API.json()
    #print(data)
    #^shows the entine json
    if data["onlineAvailability"] == True:
        print("its in stock")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="+12064783243", 
            from_="+16802213523",
        body="add to cart!" + data["addToCartUrl"] + "\n" + data["name"] + " is in stock")

        print(message.sid)
    else:
        print("OOS try again later")
    print(data["addToCartUrl"])
    print(data["onlineAvailability"])
    # parse_json = json.loads(data)
    # headphones = parse_json['products']['']
    #test sku: 5901353 in stock | 6521517 sold out

main()