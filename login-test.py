import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging

logging.basicConfig(level=logging.INFO)

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
url = os.getenv("URL")


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
    password_input.send_keys(password)
    submit_button.click()
    
    WebDriverWait(driver, 10).until(EC.title_contains("Patients | Helium Health"))
    logging.info("Login successful - Redirected to patients.")
except Exception as e:
    logging.error("Login Unsuccessful - {}".format(str(e)))
finally:
    driver.quit()
