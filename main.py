#!/usr/bin/env python3
"""DARRYL DAVIS | MAIN SCRIPT FOR STOCKBOT"""
from os import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import yagmail
from twilio.rest import Client
from config import api_key,sender,gmail_pwd,auth_token,account_sid
yag = yagmail.SMTP(sender, gmail_pwd)

def main():
    """The main function| in future revisions I'll make this more modular"""
    def sku_input():
        """sku input function"""
        global SKU
    # enter SKU to monitor
        SKU = input("Please enter the SKU you want to monitor \n>")
        while len(SKU) !=7:
            print(f"{len(SKU)} characters is not proper length of SKU 7 characters expected\n")
            main()

        return SKU
    def num_input():
        """phone number input function"""
        global YOUR_NUM
        YOUR_NUM = input("Please enter your phone number ###-###-####.\nTo opt out of text updates,"
        "leave blank. \n>").replace('-', '').replace('(', '').replace(')','')
        while len(YOUR_NUM) != 10 and len(YOUR_NUM) != 0:
            print(f"Please enter phone number in ###-###-#### format. {YOUR_NUM} not accpeted")
            num_input()

    def email_input():
        """email input function"""
        global YOUR_EMAIL
        YOUR_EMAIL = input("Please enter your email (Only accepting '.com' emails)\nTo opt out of email updates, leave blank.\n>").lower()
        while YOUR_EMAIL.endswith(".com") is False and len(YOUR_EMAIL) != 0:
            print(f"please enter valid email '{YOUR_EMAIL}' not accepted")
            email_input()
        if (YOUR_EMAIL == '') and (YOUR_NUM == '' ):
            print("You didn't provide an email or phone #\n")
            num_input()

    def get_json():
        """json GET request"""
        global JSON
        global RESPONSE_API
        RESPONSE_API = requests.get("https://api.bestbuy.com/v1/products/"
         + SKU + ".json?apiKey=" + api_key)
        print(RESPONSE_API.status_code)
        if RESPONSE_API.status_code == 400:
            print("invalid SKU, Please try again")
            sku_input()
        JSON = RESPONSE_API.json()
        # print(json)
        # ^shows the entire json
    def ping_api():
        """api loop ping"""
        while not JSON["onlineAvailability"]:
            print("OOS still searching for " , JSON["name"])
            print(f"Will send msg to: \n#: {YOUR_NUM} \nEmail: {YOUR_EMAIL}")
            RESPONSE_API = requests.get("https://api.bestbuy.com/v1/products/"
             + SKU + ".json?apiKey=" + api_key)
            print(f"still searching for {SKU}\n\n")
        
            time.sleep(2)
            #5 queries per second/50,000 queries per day
            #ERROR CODE 429 if exceeded

        if JSON["onlineAvailability"]:
            print("it's in stock")
    def send_email():
        """send email function"""
        if YOUR_EMAIL == '':
            send_txt()
        else:
            receiver = YOUR_EMAIL
            body = "Add to cart!\n" + JSON["addToCartUrl"]
            yag.send(
            to=receiver,
            subject= JSON["name"] + " is in stock",
            contents=body,
)
        print("email sent!")
    def send_txt():
        """send txt function"""
        if YOUR_NUM == '':
            checkout()
        else:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                to="+1" + YOUR_NUM,
                from_="+16802213523",
                body="Add to cart!\n" + JSON["addToCartUrl"] + "\n" + JSON["name"] + " is in stock")
            print(message.sid)
            print(f"Txt sent to {YOUR_NUM}.\nGood Luck!")
    def checkout():
        """adds to cart and checksout of webpage"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')

        # Provide the path of chromedriver.
        #bypass BBY bot detection
        driver = webdriver.Chrome(executable_path="chromedriver", options = options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver.maximize_window()

        # Send a get request to the url
        driver.get(JSON["addToCartUrl"])
        title = driver.title
        print(title)
        driver.implicitly_wait(5)
        checkout_button = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div[2]/div[1]/div/div[2]/div[1]/section[2]/div/div/div[4]/div/div[1]/button')
        checkout_button.click()
        driver.implicitly_wait(5)
        guest_checkout_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div[4]/div/div[2]/button')
        guest_checkout_button.click()
        ##time to fill out input fields
        firstname_input = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[1]/section/div[1]/div[2]/div/div/form/div[1]/div/input')
        firstname_input.send_keys("Darryl")
        lastname_input = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[1]/section/div[1]/div[2]/div/div/form/div[2]/div/input')
        lastname_input.send_keys("Davis")
        addr_input = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[1]/section/div[1]/div[2]/div/div/form/div[3]/div[2]/div/div/input')
        addr_input.send_keys("4327 Lake Wa BLVD NE Kirkland WA")
        ciy_input = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[1]/section/div[1]/div[2]/div/div/form/div[5]/div[1]/div/input')
        ciy_input.send_keys("Kirkland")
        state_input = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[1]/section/div[1]/div[2]/div/div/form/div[5]/div[2]/div/div/select')
        state_input.click()
        zip_input = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[1]/section/div[1]/div[2]/div/div/form/div[6]/div/div[1]/div/input')
        zip_input.send_keys("98033")
        select = Select(driver.find_element(By.ID,('state')))
        # select by visible text
        select.select_by_visible_text('WA')
        # select by value 
        select.select_by_value('WA')
        expand_apt = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[1]/section/div[1]/div[2]/div/div/form/div[4]/button/span')
        expand_apt.click()
        apt_input = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[1]/section/div[1]/div[2]/div/div/form/div[4]/div/input')
        apt_input.send_keys("apt 6111")
        driver.implicitly_wait(5)
        submit_shipping = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[1]/section/div[1]/div[2]/div/div/div[2]/button/span')
        submit_shipping.click()
        contact_email = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[1]/section/div[2]/section/section/div[1]/label/div/input')
        contact_email.send_keys(YOUR_EMAIL)
        driver.implicitly_wait(5)
        contact_num = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[2]/section/div[2]/section/section/div[2]/label/div/input')
        contact_num.send_keys(YOUR_NUM)
        driver.implicitly_wait(5)
        # cont_payment = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[3]/div[2]/section/div[2]/section/div/div/button/span')
        # cont_payment.click()
        time.sleep(600)
        # driver.quit()
        print("Done")

    sku_input()
    num_input()
    email_input()
    get_json()
    ping_api()
    send_email()
    send_txt()
    checkout()
    # #test SKU: 5901353 in stock | 6521430 sold out
if __name__ == "__main__":
    main()
