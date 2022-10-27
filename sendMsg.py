#!/usr/bin/env python3
from twilio.rest import Client
from config import account_sid
from config import auth_token
import main
def instock():
     client = Client(account_sid, auth_token)

     message = client.messages.create(
         to="+12064783243", 
         from_="+16802213523",
        body="add to cart!" + "addToCartUrl" + "<name of item> is in stock")

     print(message.sid)
instock()
