from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Setup the webdriver
driver = webdriver.Chrome()

# Open Google
driver.get('https://www.google.com')

# Find the search bar and input search query
search_box = driver.find_element('name', 'q')
search_box.send_keys('Selenium Python tutorial')
search_box.send_keys(Keys.RETURN)

# Wait for results to load
time.sleep(2)

# Scrape the titles and URLs of search results
results = driver.find_elements('css selector', 'h3')
for result in results:
    print(result.text)
    print(result.find_element('xpath', '..').get_attribute('href'))

# Close the browser
driver.quit()
