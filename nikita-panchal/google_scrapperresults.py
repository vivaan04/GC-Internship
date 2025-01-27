from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

chromedriver_path = 'path_to_your_chromedriver'


options = webdriver.ChromeOptions()
options.headless = False  

driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

driver.get('https://www.google.com')

search_query = "GOOGLE"
search_box = driver.find_element("name", "q")
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)


time.sleep(2)
results = driver.find_elements("css selector", "h3")


for result in results:
    print(result.text)


driver.quit()
