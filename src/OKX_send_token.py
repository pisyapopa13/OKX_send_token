import requests
import time
import random
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



min_value = 0.29
max_value = 0.31
driver = "C:\\you\\personal\\path\\to\\chromedriver-win-x64.exe"
req_url = f'http://localhost:3001/v1.0/browser_profiles/70849565/start?automation=1'
okx_url = f"https://www.okx.com/balance/withdrawal/avax-chain"


with open("config\\Adeesses_rotated.txt", "r") as file:
    addresses = [line.strip() for line in file.readlines()]
min_delay = float(input("Enter the minimum delay duration in seconds: "))
max_delay = float(input("Enter the maximum delay duration in seconds: "))
def click_if_exists(driver, xpath):
    try:
        elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        if elements:
            elements[0].click()
            time.sleep(random.uniform(0.5, 1.5))
            return True
    except TimeoutException:
        pass
def find_and_click_select(address):
    rows = driver.find_elements(By.CSS_SELECTOR, 'tr.okui-table-row.address-table-row')
    for index, row in enumerate(rows, start=1):
        address_cell = row.find_element(By.CSS_SELECTOR, 'td.okui-table-cell:nth-child(3) div')
        if address_cell.text == address:
            select_button = row.find_element(By.CSS_SELECTOR, 'td.okui-table-cell:nth-child(5) div.actions span.action')
            select_button.click()
            break
def main_loop(address, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            driver.get(okx_url)
            time.sleep(10)
            click_if_exists(driver, bottom)
            time.sleep(random.uniform(1, 3))
            click_if_exists(driver, bottom2)
            specific_address = address
            time.sleep(10)
            find_and_click_select(specific_address)
            time.sleep(7)

            random_value = random.uniform(min_value, max_value)
            formatted_value = f"{random_value:.8f}"

            input_element = driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/input')
            input_element.clear()
            input_element.send_keys(formatted_value)
            click_if_exists(driver, confirm)
            click_if_exists(driver, confirm2)
            next_delay = random.uniform(min_delay, max_delay)
            print(
                f"Sent {formatted_value} to address {specific_address}. Waiting {next_delay:.2f} seconds before the next operation.")
            return next_delay
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt == max_attempts - 1:
                print("All attempts failed. Exiting.")
                return None
            else:
                retry_delay = random.uniform(10, 15)
                print(f"Waiting {retry_delay:.2f} seconds before retrying.")
                time.sleep(retry_delay)


chrome_driver_path = Service(driver)
bottom = '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[3]/div[2]/div/button'
bottom2 = '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[2]/button'
select_network = '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]'
arb = '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div[3]'
input_1 = '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/input'
confirm = '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[7]/button'
confirm2 = '/html/body/div[10]/div/div[3]/div/button'
response = requests.get(req_url)
response_json = response.json()
print(response_json)
port = str(response_json['automation']['port'])
options = webdriver.ChromeOptions()
options.debugger_address = f'127.0.0.1:{port}'
driver = webdriver.Chrome(service=chrome_driver_path, options=options)
for address in addresses:
    next_delay = main_loop(address)
    time.sleep(next_delay)