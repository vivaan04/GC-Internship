from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import pandas as pd
import time

def initialize_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)

def perform_google_search(driver, query):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query, Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g")))

def scrape_search_results(driver, max_results=10):
    results_list = []

    # Scroll down to load more search results dynamically
    for _ in range(max_results // 10):  # Assuming 10 results per scroll
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep duration as needed
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g")))

    search_results = driver.find_element(By.ID, value='main')
    html_elements = search_results.find_elements(By.CLASS_NAME, value='MjjYud')

    for result in html_elements:
        try:
            url = result.find_element(By.CSS_SELECTOR, value="a").get_attribute('href')
            title = result.find_element(By.CSS_SELECTOR, value="h3.LC20lb.MBeuO.DKV0Md").text
            description = result.find_element(By.CSS_SELECTOR, value="div.VwiC3b.yXK7lf.lyLwlc.yDYNvb.W8l4ac.lEBKkf").text
            results_list.append({"Title": title, "URL": url, "Description": description})
        except Exception as e:
            print(e)
            continue

    return results_list

def save_to_csv(results_list, csv_file):
    fieldnames = ['Title', 'URL', 'Description']
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results_list:
            writer.writerow(result)

def main():
    csv_file = 'search_results.csv'
    query = "Internshala"
    max_results = 30  # Set the desired number of search results

    driver = initialize_driver()
    try:
        perform_google_search(driver, query)
        results_list = scrape_search_results(driver, max_results)
        save_to_csv(results_list, csv_file)
        print(f"Search results saved to {csv_file}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
