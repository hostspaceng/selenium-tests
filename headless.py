import os
import requests
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
url = os.getenv("URL")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

# Install the correct version of ChromeDriver
chromedriver_autoinstaller.install()

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
options.add_argument('--disable-software-rasterizer')

driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome()
driver.get(url)

def send_slack_notification(message):
    payload = {
        "text": message
    }
    try:
        response = requests.post(slack_webhook_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Failed to send Slack notification - {}".format(str(e)))

try:
    WebDriverWait(driver, 10).until(EC.title_is("Sign in | Helium Health"))
    logging.info("Login page loaded successfully.")
    
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "emailOrPhone"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    submit_button = driver.find_element(by=By.CLASS_NAME, value="LoginCredentialsForm__submit")
    
    email_input.send_keys(email)
    password_input.send_keys(password)
    submit_button.click()
    
    WebDriverWait(driver, 10).until(EC.title_contains("Patients | Helium Health"))
    logging.info("Login successful - Redirected to patients.")
except Exception as e:
    logging.error("Login Unsuccessful - {}".format(str(e)))
    send_slack_notification(f"Login Unsuccessful - {url}")
finally:
    driver.quit()
