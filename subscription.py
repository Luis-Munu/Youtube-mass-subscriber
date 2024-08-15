import getpass
import json
import logging
import time
from contextlib import contextmanager

#import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

# Change the language here, Spanish (es) or English (en)
language = "es"

logging.basicConfig(filename='config/subscription.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

elements = json.load(open("config/elements.json", "r"))

@contextmanager
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-web-security')
    options.add_argument(f'--lang={language}')
    
    #chromedriver_autoinstaller.install() 
    #driver = webdriver.Chrome(executable_path='config/chromedriver.exe', options=options)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        yield driver
    finally:
        driver.quit()

def get_user_credentials():
    username = input("Enter your YouTube email: ")
    password = getpass.getpass("Enter your YouTube password: ")
    return username, password

def read_channel_urls(filename):
    with open(filename, "r") as f:
        channel_urls = f.read().splitlines()
    return channel_urls

def subscription_loop(username, password):
    with get_driver() as driver:
        driver.implicitly_wait(10)
        driver.get('https://www.youtube.com')

        decline_cookies(driver)
        sign_in(driver, username, password)

        for url in read_channel_urls("config/urls.txt"):
            channel_subscription(driver, url)
            time.sleep(2)

def decline_cookies(driver):
    driver.find_element(By.XPATH, elements["locators"]["reject_cookies"][language]).click()

def sign_in(driver, username, password):
    driver.find_element(By.XPATH, elements["locators"]["sign_in"][language]).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'identifierId'))).send_keys(username, Keys.RETURN)
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="password"]'))).send_keys(password, Keys.RETURN)
    time.sleep(4)

def channel_subscription(driver, url):
    driver.get(url)
    try:
        #subscribe_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "subscribe-button")))
        subscribe_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".yt-spec-button-shape-next.yt-spec-button-shape-next--filled.yt-spec-button-shape-next--mono")
            )
        )
        if subscribe_button.text == elements["labels"]["subscribe_button"][language]:
            subscribe_button.click()
            logging.info("Subscribed to channel: " + url)
        else:
            logging.info("Already subscribed to channel: " + url)
    except:
        logging.error("Could not subscribe to channel: " + url)

def main():
    username, password = get_user_credentials()
    subscription_loop(username, password)

if __name__ == "__main__":
    main()