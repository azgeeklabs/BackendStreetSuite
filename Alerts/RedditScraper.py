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


def TimeZone(time):
    timestamp = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    timestamp_utc = timestamp.replace(tzinfo=pytz.utc)
    
    cairo_timezone = pytz.timezone('UTC')

    timestamp_cairo = timestamp_utc.astimezone(cairo_timezone)
   
    current_time_cairo = datetime.now(cairo_timezone)

    time_difference = current_time_cairo - timestamp_cairo

    day_difference = float(time_difference.total_seconds() / 86400)
    return day_difference

def ScrolllingTillTimeMeet(time_frame, driver):
    try:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, "//article[@class='w-full m-0']")))
    except:
        return
    while True:
        posts = driver.find_elements(By.XPATH, "//article[@class='w-full m-0']")
        try:
            LatestPost = posts[-1]
            TimePosted = LatestPost.find_element(By.XPATH, ".//time").get_attribute('datetime')
            TimeInDays = TimeZone(TimePosted)
            print("time in days", TimeInDays, "timeframe", time_frame)
            if TimeInDays < time_frame:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, 10).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            else:
                break
        except:
            continue
    print(f"total Posts in the account = {len(posts)}")

def CheckTime(post, time_frame):
    TimePosted = post.find_element(By.XPATH, ".//time").get_attribute('datetime')
    TimeInDays = TimeZone(TimePosted)
    if TimeInDays < time_frame:
        return True
    else:
        return False

def CheckFlair(post):
    FlairClass = post.find_element(By.XPATH, ".//shreddit-post-flair")
    if "Meme" in FlairClass.text or "MEME" in FlairClass.text or "meme" in FlairClass.text:
        return True
    else:
        return False
    
def PostDetail(driver, AttachedPosts, TickerCount, TickerList):
    try:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//div[@class="text-neutral-content"]')))
        text =  driver.find_element(By.XPATH, '//h1[@slot="title"]').text
        text = text + " " + driver.find_element(By.XPATH, '//div[@class="text-neutral-content"]').text
        print(text)

        for i in range(len(TickerList)):
            ticker_patterns = []
            ticker_pattern = re.escape(TickerList[i])
            ticker_patterns.append(r'[$#]?' + r'(["\{\[])?' + ticker_pattern + r'(["\}\]])?\b')

            pattern = re.compile('|'.join(ticker_patterns))
            if re.search(pattern, text):
                TickerCount[i] = TickerCount[i] + 1

        AttachedPosts = AttachedPosts + 1
    except TimeoutException:
        pass

def PostComments(driver, TickerCommentCount, TickerList):
    comments = driver.find_elements(By.XPATH, '//*[@id="comment-tree"]/shreddit-comment/div[@slot="comment"]')
    for i in range(len(comments)):
        CommentText = comments[i].text
        for i in range(len(TickerList)):
            pattern = fr'\b{re.escape(TickerList[i])}\b'
            if re.search(pattern, CommentText):
                TickerCommentCount[i] = TickerCommentCount[i] + 1
        


def main(RedditAccounts, TickerList, time_frame):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    print("set reddit driver settings")
    driver = webdriver.Chrome(service=service, options=options)
    print("opened driver")

    TickerCount = [0]*len(TickerList)
    TickerCommentCount = [0]*len(TickerList)



    for account in RedditAccounts:
        print("inside", account)
        driver.get(f"https://www.reddit.com/" + account + "/new/")
        sleep(5)

        print("check point")
        ScrolllingTillTimeMeet(time_frame, driver)
        print("check point 2")
        AttachedPosts = 0
        print("collecting posts")
        posts = driver.find_elements(By.XPATH, "//article[@class='w-full m-0']")
        original_window = driver.current_window_handle
        for post in posts:
            print("inside", post)
            if CheckTime(post, time_frame):
                if CheckFlair(post):
                    continue
                else:
                    article = post.find_element(By.XPATH, ".//shreddit-post/a")
                    href = article.get_attribute("href")

                    print("link", href)
    
                    driver.execute_script("window.open(arguments[0]);", href)

                    print("swithching to article")
                    driver.switch_to.window(driver.window_handles[-1]) 
                    PostDetail(driver, AttachedPosts, TickerCount, TickerList)
                    PostComments(driver, TickerCommentCount, TickerList)
                    driver.close()
                    driver.switch_to.window(original_window)
            else:
                break

    tickerdict = {}
    for i in range(len(TickerList)):
        total = TickerCount[i] + TickerCommentCount[i]
        if total >= 5:
            tickerdict[TickerList[i]] = total 
    driver.quit()
    return tickerdict

    