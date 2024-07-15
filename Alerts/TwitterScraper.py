import time
import re
import sched
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import sys
import pytz
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv


load_dotenv()

def TimeZone(time):
    timestamp = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    timestamp_utc = timestamp.replace(tzinfo=pytz.utc)
    
    cairo_timezone = pytz.timezone('UTC')

    timestamp_cairo = timestamp_utc.astimezone(cairo_timezone)
   
    current_time_cairo = datetime.now(cairo_timezone)

    time_difference = current_time_cairo - timestamp_cairo

    day_difference = float(time_difference.total_seconds() / 86400)
    return day_difference

def scrape_ticker_mentions(driver, TickerCount, tickers):
    time.sleep(2)  # wait for page to load
    try:
        text = driver.find_element(
                    By.XPATH, '//div[@data-testid="tweetText"]').text
        print(text)
        for i in range(len(tickers)):
                ticker_patterns = []
                ticker_pattern = re.escape(tickers[i])
                ticker_patterns.append(r'\b[$#]?' + r'(["\{\[])?' + ticker_pattern + r'(["\}\]])?\b')

                pattern = re.compile('|'.join(ticker_patterns), re.IGNORECASE)
                if re.search(pattern, text):
                    print("FOUND", tickers[i])
                    TickerCount[i] += 1
    except:
        pass

def scrolltilltime(time_frame):
        while True:
            posts = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
            # print(posts)
            try:
                LatestPost = posts[-1]
                TimePosted = LatestPost.find_element(By.XPATH, ".//time").get_attribute('datetime')
                TimeInDays = TimeZone(TimePosted)
                print("time in days", TimeInDays, "timeframe", time_frame)
                if TimeInDays < time_frame:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    WebDriverWait(driver, 15).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                else:
                    break
            except:
                continue

def login():
    driver.get("https://x.com/i/flow/login")
    time.sleep(5)
    try:
        username_input = driver.find_element(By.XPATH, '//input[@autocomplete="username"]')
        print("inputing username")
        username_input.send_keys(os.getenv("twitter_user"))
        username_input.send_keys(Keys.ENTER)
    except NoSuchElementException:
        sys.exit("could not log in")
        
    time.sleep(3)

    try:
        driver.find_element(By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]')
        print("inputing username again")

        username_input = driver.find_element(By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]')
        username_input.send_keys(os.getenv("twitter_user"))
        username_input.send_keys(Keys.ENTER)
        time.sleep(3)
    except NoSuchElementException:
        pass
        
        
        

    password_input = driver.find_element(By.XPATH, '//input[@name="password"]')
    print(os.getenv("twitter_pass"))
    password_input.send_keys("Polo_1991")
    password_input.send_keys(Keys.ENTER)
    try:    
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]')))
    except TimeoutException:
        pass

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

def main(twitter_accounts, tickers, time_frame):
    TickerCount = [0]*len(tickers)
    login()
    #iterate over each account
    for account in twitter_accounts:
        print("Now scraping", account)
        driver.get(f"https://x.com/{account}")
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]')))
        except TimeoutException:
            print("timed out while waiting for tweets to load for", account)
            continue
        time.sleep(3) 
        scrolltilltime(time_frame)
        posts = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        original_window = driver.current_window_handle

        for post in posts:
            # if not CheckTime(post):
            #     break
            try:
                article = post.find_element(By.CSS_SELECTOR, 'div.css-175oi2r.r-18u37iz.r-1q142lx > a')
                href = article.get_attribute("href")
                driver.execute_script("window.open(arguments[0]);", href)

                print("swithching to article")
                driver.switch_to.window(driver.window_handles[-1]) 
                scrape_ticker_mentions(driver, TickerCount, tickers)

                driver.close()
                driver.switch_to.window(original_window)            
            except:
                print("something happened while opening post")

    for i in range(len(tickers)):
        print(f"The ticker '{tickers[i]}' appears {TickerCount[i]} time(s)")

        tickerdict = {}
    for i in range(len(tickers)):
        if TickerCount[i] >= 5:
            tickerdict[tickers[i]] = TickerCount[i]

    return tickerdict



def CheckTime(post):
    TimePosted = post.find_element(By.XPATH, ".//time").get_attribute('datetime')
    TimeInDays = TimeZone(TimePosted)
    if TimeInDays < time_frame:
        return True
    else:
        return False


time_frame = .25
