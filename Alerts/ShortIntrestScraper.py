from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import pytz
import re
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def main(tickers):
    # Use the specified ChromeDriver binary path
    service = Service(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("disable-infobars")
    driver = webdriver.Chrome(service=service, options=options)

    value_dict = {}
    for i in range(len(tickers)):
        print(tickers[i])
        driver.get(f"https://www.benzinga.com/quote/{tickers[i]}/short-interest")
        # print("scraping", tickers[i])
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                (By.XPATH, '//div[@class="card-value font-extrabold"]')))
            sleep(7)
            value = driver.find_elements(
                By.XPATH, '//div[@class="card-value font-extrabold"]')
        except TimeoutException:
            continue
        sleep(2)
        try:
            value_text = value[1].text
            print(value_text)
            value_string = value_text.strip("%")
            float_value = float(value_string)
            # print(type(float_value))
            if float_value >= 30:
                # print("done")
                value_dict[tickers[i]] = value[1].text
        except:
            continue
        # print(value_dict)
    return value_dict