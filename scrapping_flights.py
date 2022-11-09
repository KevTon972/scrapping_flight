"""automate flight ticket search"""
from selenium import webdriver
import requests
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def check_status(url):
    #check is the status code is 200
    response = requests.get(url)
    if response.ok:
        return True
    return "the status code's not 200"

def scrapp_and_send(url, driver):
    get_url(url, driver)
    Accept_button(driver)
    get_datas(driver)

def get_url(url, driver):
    # open the web page at the indicated url 
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)

def Accept_button(driver):
    #click on "Accepter" button    
    all_buttons = driver.find_elements(By.TAG_NAME, 'button')
    accepted_button = [btn for btn in all_buttons if btn.text == 'Accepter']
    
    for btn in accepted_button:
        btn.click()
        time.sleep(2)

def get_datas(driver):
    all_buttons = driver.find_elements(By.CLASS_NAME, "_TS")

    for btn in all_buttons:
        btn.click()
        time.sleep(2)
        link = driver.find_element(By.XPATH, "//a[@role='link']")
        lien = link.get_attribute('href')
        get_url(lien, driver)
        datas = driver.find_elements(By.CLASS_NAME, 'container')
        for data in datas[:5]:
            print(data.text)
            print("-"*20)
        break

    
if __name__ == "__main__":
    url = 'https://www.kayak.fr/explore/PAR-anywhere/20221125,20221127'
    driver_service = Service(executable_path='chromedriver')
    driver = webdriver.Chrome(service=driver_service)

    if check_status(url):
        scrapp_and_send(url,driver)