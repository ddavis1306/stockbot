#!/usr/bin/env python3
"""DARRYL DAVIS | MAIN SCRIPT FOR STOCKBOT"""
from os import sys
import time
import requests
import yagmail
from twilio.rest import Client
from config import api_key,sender,gmail_pwd,auth_token,account_sid
###GLOBAL VARIABLES###
yag = yagmail.SMTP(sender, gmail_pwd)
print(__name__)
# make SKU and api_key global variables so they can be used in the while loop

###END OF GLOBAL VARS###
def main():
    """The main function| in future revisions I'll make this more modular"""
    def sku_input():
        """USER CREDS"""
        global SKU
    # enter SKU to monitor
        SKU = input("Please enter the SKU you want to monitor \n>")
        while len(SKU) !=7:
        # return(SKU)
            print(f"{len(SKU)} characters is not proper length of SKU 7 characters expected\n")
            main()

        return SKU
    # Use .replace to 'pop' out unneccesary characters for message func
    def num_input():
        global YOUR_NUM
        YOUR_NUM = input("Please enter your phone number ###-###-####.To opt out of text updates,"
        "leave blank. \n>").replace('-', '').replace('(', '').replace(')','')
        while len(YOUR_NUM) != 10 and len(YOUR_NUM) != 0:
            print(f"Please enter phone number in ###-###-#### format. {YOUR_NUM} not accpeted")
            num_input()
            
    def email_input():
        global YOUR_EMAIL
        YOUR_EMAIL = input("Please enter your email (Only accepting '.com' emails) To opt out of email updates, leave blank.\n>").lower()
        while YOUR_EMAIL.endswith(".com") is False and len(YOUR_EMAIL) != 0:
             email_input()
        if (YOUR_EMAIL == "") and (YOUR_NUM == "" ):
            print("You didn't provide an email or phone #")
            num_input()
            print(f"please enter valid email '{YOUR_EMAIL}' not accepted")
    def get_json():
        global JSON
        global RESPONSE_API
        RESPONSE_API = requests.get("https://api.bestbuy.com/v1/products/" + SKU + ".json?apiKey=" + api_key)
        print(RESPONSE_API.status_code)
        if RESPONSE_API.status_code == 400:
            print("invalid SKU, Please try again")
            sku_input()
        JSON = RESPONSE_API.json()
    # #print("foo")
    # # print(json)
    # # ^shows the entire json
    def ping_api():
        while not JSON["onlineAvailability"]:
            print("OOS still searching for " , JSON["name"])
            print(f"Will send msg to: \n#: {YOUR_NUM} \nEmail: {YOUR_EMAIL}")
            RESPONSE_API = requests.get("https://api.bestbuy.com/v1/products/" + SKU + ".json?apiKey=" + api_key)
            print("still searching for " + SKU)
            time.sleep(2)
            #5 queries per second/50,000 queries per day
            #ERROR CODE 429 if exceeded
            
  
        if JSON["onlineAvailability"]:
            print("its in stock")
    def send_email():
        if YOUR_EMAIL == "":
            send_txt()
        receiver = YOUR_EMAIL
        body = "Add to cart!\n" + JSON["addToCartUrl"]
        yag.send(
        to=receiver,
        subject= JSON["name"] + " is in stock",
        contents=body,
)
        print("email sent!")
    def send_txt():
        if YOUR_NUM == "":
            sys.exit()
        else:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                to="+1" + YOUR_NUM,
                from_="+16802213523",
                body="Add to cart!\n" + JSON["addToCartUrl"] + "\n" + JSON["name"] + " is in stock")
            print(message.sid)
            print(f"Txt sent to {YOUR_NUM}.\nGood Luck!")
            sys.exit()

    sku_input()
    num_input()
    email_input()
    get_json()
    ping_api()
    send_email()
    send_txt()
    # #test SKU: 5901353 in stock | 6521517 sold out
if __name__ == "__main__":
    main()

