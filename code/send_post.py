#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

import re

from time import sleep

# Read logins file
with open("logins.json", "r") as f:
    data = json.loads(f.read())
    
    username = data[0]["username"]
    password = data[0]["password"]

driver = webdriver.Chrome()
driver.get("https://instagram.com")


# Find accept cookies button
while 1:
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if button.text == "Only allow essential cookies":
                break
        break
    except:
        sleep(1)
# Click the cookies button
button.click()

sleep(1)
# Find all input boxes
while 1:
    try:
        for input_box in driver.find_elements(By.TAG_NAME, "input"):
            if input_box.get_attribute("name") == "username":
                input_box.send_keys(username)
            if input_box.get_attribute("name") == "password":
                input_box.send_keys(password)
        break
    except:
        sleep(1)
        
