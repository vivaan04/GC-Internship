from selenium import webdriver
from selenium.webdriver.safari.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import numpy as np


def main():
    driver = webdriver.Safari(service=Service())
    driver.get("https://www.google.com/")

    search_class = "gLFyf"

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, search_class))
    )

    print("Searching...")

    search_box = driver.find_element(By.CLASS_NAME, search_class)
    search_box.clear()
    time.sleep(2)

    search_term = "Internshala"
    search_box.send_keys(search_term + Keys.ENTER)

    titles_xpath = "//div[@class='MjjYud']/div/div/div/div/div/span/a/h3"
    links_xpath = "//div[@class='MjjYud']/div/div/div/div/div/span/a"
    source_xpath = "//div[@class='MjjYud']/div/div/div/div/div/span/a/div/div/span"
    description_xpath = "//div[@class='MjjYud']/div/div/div[2]/div[@class='VwiC3b yXK7lf lyLwlc yDYNvb W8l4ac lEBKkf']"

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, titles_xpath))
    )

    print("Scrolling...")

    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        try:
            next_button = driver.find_element(By.CLASS_NAME, "RVQdVd") 
            next_button.click()
        except Exception:
            pass

    titles = driver.find_elements(By.XPATH, titles_xpath)
    links = driver.find_elements(By.XPATH, links_xpath)
    source = driver.find_elements(By.XPATH, source_xpath)
    description = driver.find_elements(By.XPATH, description_xpath)

    print(f"Found {len(description)} results")

    print("Extracting Data...")

    data = []
    for i in range(len(description)):
        data.append({"Title": titles[i].text, "Source": source[i].text, "Description": description[i].text, "URL": links[i].get_attribute("href")})

    pd.DataFrame(data).to_csv("internshala.csv")
    print("Done extracting data...")

    time.sleep(2)
