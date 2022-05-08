#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding=utf-8
import re
import os
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from misc.etymology_helper import EtymologyHelper
from selenium.webdriver.chrome.options import Options


def make_selenium_insta_post(output_video_path, caption_text):    
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=/home/j/.config/google-chrome/Person 1")
    
    driver = webdriver.Chrome(options=options)
    
    # Read logins file
    with open("logins.json", "r") as f:
        data = json.loads(f.read())
        
        username = data[0]["username"]
        password = data[0]["password"]
    
    # driver = webdriver.Chrome()
    driver.get("https://instagram.com")
    
    # Wait for page to load
    # I assume that page is loaded instagram icon becomes visible
    valid = False
    while not valid:
        try:
            logos = driver.find_elements(By.TAG_NAME, "img")
            for logo in logos:
                if logo.get_attribute("alt") == "Instagram":
                    valid = True
        except:
            sleep(1)
    
    # Check if login button is visible
    buttons = driver.find_elements(By.TAG_NAME, "button")
    
    for button in buttons:
        button_text = button.text
        
        if "Continue as " in button_text:
            button.click()
            valid = True
            print("Need to log back in :(")
    
    # Check if can see the new post button
    buttons = driver.find_elements(By.TAG_NAME, "button")
    make_post_button = None
    for button in buttons:
        svgs = button.find_elements(By.TAG_NAME, "svg")
        for svg in svgs:
            if not svg.get_attribute("aria-label") is None:
                if svg.get_attribute("aria-label") == "New Post":
                    make_post_button = button
    
    if make_post_button is None:
        # On login page
        print("not logged in")
        # Raise an issue
        pass
    else:
        # Home page
        print("logged in")
        pass
    
    make_post_button.click()
    
    # Find an input field
    inputs = driver.find_elements(By.TAG_NAME, "input")
    for fileinput in inputs:
        fileinput.send_keys(output_video_path)
        
    
    valid = False
    while not valid:
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                button_text = button.text
                if button_text == "Next":
                    button.click()
                    valid = True
        except:
            sleep(1)
            
    valid = False
    while not valid:
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                button_text = button.text
                if button_text == "Next":
                    button.click()
                    valid = True
        except:
            sleep(1)
            
    # Search for text input box
    valid = False
    while not valid:
        try:
            text_areas = driver.find_elements(By.TAG_NAME, "textarea")
            for text_area in text_areas:
                field_text = text_area.get_attribute("placeholder")
                if field_text == "Write a caption...":
                    caption_full = caption_text
                    capt_split = caption_full.replace("\t","").split("\n")
                    for caption in capt_split:
                        text_area.send_keys(caption)
                        text_area.send_keys(Keys.RETURN)
                    valid = True
        except:
            sleep(1)
    
    valid = False
    while not valid:
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                button_text = button.text
                if button_text == "Share":
                    button.click()
                    valid = True
        except:
            sleep(1)
