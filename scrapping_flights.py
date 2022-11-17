"""automate flight ticket search"""
import requests
import time
import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_status(url):
    #check is the status code is 200
    response = requests.get(url)
    if response.ok:
        return True
    return False

def get_url(url, driver):
    # open the web page at the indicated url 
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

def Accept_button(driver):
    #click on "Accepter" button    
    try:
        all_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
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
            all_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_TS'))) 

            for btn in all_buttons:
                if btn.text == btn.text:
                    all_buttons.remove(btn)

            if all_buttons:
                all_buttons[i].click()

        except:
            driver.quit()
            
        try:
            #get the link to flight info
            link_page = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@role='link']")))
            link = link_page.get_attribute('href')

            #get city's name   
            city_name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'last-crumb'))).text    
            get_url(link, driver)

            #get flight infos(main info, flights price, compagnies names, link to reservation) and add them to a dict  
            raw_datas = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mainInfo')))
            clean_datas = [data.text.replace("\n", " ") for data in raw_datas]
            prices = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'right-alignment')))
            compagnies = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'codeshares-airline-names')))
            link_flights_tickets = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'booking-link ')))  

            for i in range(3):
                price = prices[i].text.replace("\n","")
                real_price = "".join([number for number in price[2:5]]).replace(" ","")
                compagny = [comp.text for comp in compagnies]
                link_flight_ticket = link_flights_tickets[i].get_attribute('href')
                flight_info[f"{city_name},{i}"]= f"{compagny[i]} {clean_datas[i]} prix: {real_price}€, Reservez: {link_flight_ticket}"

            get_url(url, driver)
            
        except:
            driver.quit()
    
    save(flight_info)

def save(dict):
    #create a json file and save dict in it
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