#!/usr/bin/env python3
"""DARRYL DAVIS | MAIN SCRIPT FOR STOCKBOT"""

import time
from os import sys
import requests
import yagmail
from twilio.rest import Client
from config import api_key
from config import account_sid
from config import auth_token
from config import gmail_pwd
from config import sender
###GLOBAL VARIABLES###
yag = yagmail.SMTP(sender, gmail_pwd)
BBY_KEY = api_key
# make sku and api_key global variables so they can be used in the while loop
    # enter sku to monitor
sku = input("Please enter the sku you want to monitor \n>")
    # Use .replace to 'pop' out unneccesary characters for message func
yourNum = input("Please enter your phone number ###-###-####.To opt out of text updates,"
"leave blank. \n>").replace('-', '').replace('(', '').replace(')','')
yourEmail = input("Please enter your email. To opt out of email updates, leave blank.\n>")
###END OF GLOBAL VARS###
def main():
    """The main function| in future revisions I'll make this more modular"""
    # create logic: if email entered run send email function. elif null dont send email function
    # Create logic: if blank dont run text function
    while (yourEmail == "") and (yourNum == "" ):
        print("You didn't provide an email or phone #")
        sys.exit()
    response_api = requests.get(
        "https://api.bestbuy.com/v1/products/" + sku + ".json?apiKey=" + BBY_KEY)
    #print(response_api.status_code)
    if response_api.status_code == 400:
        print("invalid Sku, Please try again")
        sys.exit()
    data = response_api.json()
    #print("foo")
    # print(data)
    # ^shows the entire json
    while not data["onlineAvailability"]:
        print("OOS still searching.....")
        response_api = requests.get(
        "https://api.bestbuy.com/v1/products/" + sku + ".json?apiKey=" + BBY_KEY)
        print("still searching for " + sku)
        time.sleep(2)
    if data["onlineAvailability"]:
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

    #test sku: 5901353 in stock | 6521517 sold out
if __name__ == "__main__":
    main()
