#!/usr/bin/env python3

"""DARRYL DAVIS | MAIN SCRIPT FOR STOCKBOT"""
from config import api_key
import os
import json
import requests
from twilio.rest import Client
from config import account_sid
from config import auth_token
from config import gmail_pwd
from config import sender
import time
import yagmail
import string

###GLOBAL VARIABLES###
yag = yagmail.SMTP(sender, gmail_pwd)
bb = api_key
# make sku and api_key global variables so they can be used in the while loop
    # enter sku to monitor
sku = input("Please enter the sku you want to monitor \n>")
    # Use .replace to 'pop' out unneccesary characters for message func 
    yourNum = input("Please enter your phone number ###-###-####.To opt out of text updates, leave blank. \n>").replace('-', '').replace('(', '').replace(')','')
    print(yourNum)    
    yourEmail = input("Please enter your email. To opt out of email updates, leave blank.\n>")
print(yourEmail)
###END OF GLOBAL VARS###
def main():
    
    # create logic: if email entered run send email function. elif null dont send email function
    # Create logic: if blank dont run text function
    

    response_API = requests.get(
        "https://api.bestbuy.com/v1/products/" + sku + ".json?apiKey=" + bb)
    print(response_API.status_code)
    data = response_API.json()
    print("foo")
    # print(data)
    # ^shows the entire json
    while data["onlineAvailability"] == False:
        print("OOS try again later")
        response_API = requests.get(
        "https://api.bestbuy.com/v1/products/" + sku + ".json?apiKey=" + bb)
        print("foobar" + sku)
        time.sleep(2)
    if data["onlineAvailability"] == True:
        print("its in stock")
        #send email
    
        if yourEmail != "":
            receiver = yourEmail
            body = "Add to cart!\n" + data["addToCartUrl"]
            yag.send(
            to=receiver,
            subject= data["name"] + " is in stock",
            contents=body,
)   
        #send text
        if yourNum !="":
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                to="+1"+yourNum,
                from_="+16802213523",
                body="Add to cart!\n" + data["addToCartUrl"] + "\n" + data["name"] + " is in stock")
            print(message.sid)
    #print(data["addToCartUrl"])
    #parse_json = json.loads(data)
    #headphones = parse_json['products']['']
    #test sku: 5901353 in stock | 6521517 sold out
main()
