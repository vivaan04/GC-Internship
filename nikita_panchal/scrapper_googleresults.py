from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


driver.get("https://www.google.com")


search_bar = driver.find_element(By.NAME, "q")
search_query = "ChatGPT"
search_bar.send_keys(search_query)
search_bar.send_keys(Keys.RETURN)


time.sleep(3)


results = driver.find_elements(By.XPATH, '//h3')
for result in results:
    try:
        title = result.text
        link = result.find_element(By.XPATH, '..').get_attribute('href')
        print(f"Title: {title}\nLink: {link}\n")
    except Exception as e:
        print(f"Error: {e}")
driver.quit()
