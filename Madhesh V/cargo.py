#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install selenium


# In[ ]:





# In[24]:


import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Set up the Chrome webdriver (you need to have chromedriver installed)
driver = webdriver.Chrome()

# Open Google
driver.get("https://www.google.com")

# Find the search input box and enter the keyword "Internshala"
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Internshala")
search_box.send_keys(Keys.RETURN)

# Wait for the search results to load
driver.implicitly_wait(5)

# Extract search results
search_results = driver.find_elements(By.XPATH, "//div[@class='tF2Cxc']")

# Create a CSV file to store the results
csv_file_path = r"S:\google_search_results.csv"

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "URL", "Description"])

    # Write search results to CSV
    for result in search_results:
        try:
            title_element = result.find_element(By.XPATH, ".//h3")
            url_element = result.find_element(By.XPATH, ".//a[@href]")
            description_element = result.find_element(By.XPATH, ".//span[contains(@class, 'aCOpRe')]")

            title = title_element.text.strip()
            url = url_element.get_attribute("href")
            description = description_element.text.strip()

            writer.writerow([title, url, description])

        except Exception as e:
            print(f"Error processing result: {e}")

# Close the browser
driver.quit()

print(f"Search results exported to: {csv_file_path}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




