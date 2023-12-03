import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Function to scrape search results and save them to a CSV file


def scrape_google(keyword):
   chrome_options = Options()
   chrome_options.add_argument("--headless")

   # Initialize Chrome webdriver
   driver = webdriver.Chrome(options=chrome_options)

   driver.get("https://www.google.com")

   # Find the search bar, input the keyword, and perform the search
   search_bar = driver.find_element(By.NAME, "q")
   search_bar.send_keys(keyword)
   search_bar.submit()

   # Wait for the search results to load
   time.sleep(5)

   # Extract search results
   search_results = driver.find_element(By.ID, value='main')
   html_elements = search_results.find_elements(By.CLASS_NAME, value='MjjYud')

   # Store the results in a list of dictionaries
   results_list = []
   for result in html_elements:
      try:
            url = result.find_element(
               By.CSS_SELECTOR, value="a").get_attribute('href')
            title = result.find_element(
               By.CSS_SELECTOR, value="h3.LC20lb.MBeuO.DKV0Md").text
            description = result.find_element(
               By.CSS_SELECTOR, value="div.VwiC3b.yXK7lf.lyLwlc.yDYNvb.W8l4ac.lEBKkf").text
            # Append details to the results list as a dictionary
            results_list.append(
               {"Title": title, "URL": url, "Description": description})
      except Exception as e:
            print(e)
            continue

   # Save results to a CSV file using Pandas
   df = pd.DataFrame(results_list)
   current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
   file_name = f"search_results_{current_time}.csv"
   df.to_csv(file_name, index=False)

   driver.quit()


scrape_google("Internshala")
