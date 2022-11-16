"""automate flight ticket search"""
from selenium import webdriver
import requests
import time
import json
import os

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_status(url):
    #check is the status code is 200
    response = requests.get(url)
    if response.ok:
        return True
    return "the status code's not 200"

def get_url(url, driver):
    # open the web page at the indicated url 
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)

def Accept_button(driver):
    #click on "Accepter" button    
    try:
        all_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
        accepted_button = [btn for btn in all_buttons if btn.text == 'Accepter']

        for btn in accepted_button:
            btn.click()
    except:
        driver.quit()

def get_datas(url, driver):
    flight_info = {}
    for i in range(3):
    #get destinations buttons and click on each button
        try:
            all_buttons = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_TS'))) 

            for btn in all_buttons:
                if btn.text == btn.text:
                    all_buttons.remove(btn)

            if all_buttons:
                all_buttons[i].click()

        except:
            driver.quit()
            
        try:
            #get the link to flight info
            link_page = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@role='link']")))
            link = link_page.get_attribute('href')

            #get city's name
            city_name = driver.find_element(By.CLASS_NAME, "last-crumb").text    
            get_url(link, driver)

            datas = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mainInfo')))
            prices = driver.find_elements(By.CLASS_NAME, 'right-alignment')
            compagnies = driver.find_elements(By.CLASS_NAME, 'codeshares-airline-names')
            for i in range(4):
            #get flight infos and ad them to a dict   
                price = prices[i].text.replace("\n","")
                real_price = "".join([number for number in price[2:5]])
                data = datas[i].text.replace('\n', ' ')
                flight_info[city_name]= {compagnies[i].text : f"{data} prix: {real_price.replace(' ', '')}€"}

            get_url(url, driver)
            
        except:
            driver.quit()
    print(flight_info)
    save(flight_info)

def save(dict):
    CUR_DIR = os.path.dirname(__file__)
    file_path = os.path.join(CUR_DIR, "scrapping_flights.json")

    with open(file_path, 'w') as f:
        json.dump(dict, f, indent=4)

def scrapp_and_send(url, driver):
    get_url(url, driver)
    Accept_button(driver)
    get_datas(url, driver)


if __name__ == "__main__":
    url = 'https://www.kayak.fr/explore/PAR-anywhere/20221125,20221127'
    driver_service = Service(executable_path='chromedriver')
    driver = webdriver.Chrome(service=driver_service)

    if check_status(url):
        scrapp_and_send(url,driver)