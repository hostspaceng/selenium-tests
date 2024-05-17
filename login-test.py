import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
url = os.getenv("URL")
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_notification(message):
    payload = {
        "text": message
    }
    try:
        response = requests.post(slack_webhook_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Failed to send Slack notification - {}".format(str(e)))

driver = webdriver.Chrome()
driver.get(url)

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
    # password_input.send_keys(password)
    submit_button.click()
    
    WebDriverWait(driver, 10).until(EC.title_contains("Patients | Helium Health"))
    logging.info("Login successful - Redirected to patients.")
except Exception as e:
    error_message = f"Login Unsuccessful - {url}"
    logging.error(error_message)
    send_slack_notification(error_message)
finally:
    driver.quit()
