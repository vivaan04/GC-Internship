from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
def google_search(query):
    driver = webdriver.Chrome()  
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    results = driver.find_elements(By.CSS_SELECTOR, "h3")
    for index, result in enumerate(results[:10], start=1):
        print(f"{index}. {result.text}")

    driver.quit()
search_query = input("Enter search query: ")
google_search(search_query)
