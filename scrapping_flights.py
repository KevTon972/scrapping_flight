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

def get_url(url):
    # open the web page at the indicated url and click on "Accepter" button
    driver_service = Service(executable_path='chromedriver')
    driver = webdriver.Chrome(service=driver_service)
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)

    all_buttons = driver.find_elements(By.TAG_NAME, 'button')
    accepted_button = [btn for btn in all_buttons if btn.text == 'Accepter']
    
    for btn in accepted_button:
        btn.click()

    see_more(driver)

def see_more(driver):
    #click on 'Voir plus de destinations' button everytime there is 1
    see_more_button = True
    while see_more_button:
        #get all buttons
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        #select 'Voir plus de destinations' button and click on it
        see_more_button = [btn for btn in buttons if btn.text == 'Voir plus de destinations']

        if see_more_button:
            for btn in see_more_button:
                btn.click()
                time.sleep(2)
        else:
            see_more_button = False

if __name__ == "__main__":
    url = 'https://www.kayak.fr/explore/PAR-anywhere/20221125,20221127'
    if check_status(url):
        get_url(url)
