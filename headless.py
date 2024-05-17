import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
url = os.getenv("URL")


options = Options()
options.add_argument('--headless=new')
options.add_argument('--window-size=1920,1080')  # Adjust as necessary
options.add_argument('--enable-logging')
options.add_argument('--v=1')

options.add_argument('--disable-gpu')  # GPU is not used in headless mode
options.add_argument('--no-sandbox')  # Bypass OS security model, necessary for Docker
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
options.add_argument('--remote-debugging-port=9222')  # Remote debugging
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")  # open Browser in maximized mode
# options.add_argument("--no-sandbox")  # bypass OS security model
# options.add_argument("--disable-dev-shm-usage")  #

# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# driver = webdriver.Chrome()
driver.get(url)

print(url, password, 'and', email )
try:
    driver.save_screenshot('loginpage.png')
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
    driver.save_screenshot('pre-sub.png')
    submit_button.click()
    
    WebDriverWait(driver, 10).until(EC.title_contains("Patients | Helium Health"))
    logging.info("Login successful - Redirected to patients.")
except Exception as e:
    driver.save_screenshot('failure.png')
    logging.error("Login Unsuccessful - {}".format(str(e)))
finally:
    driver.quit()
