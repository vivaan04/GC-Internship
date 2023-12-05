#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scroll_page(driver):
    body = driver.find_element(By.TAG_NAME, value="body")
    body.send_keys(Keys.END)
    time.sleep(2)

def extract_info(driver, query, num_scrolls=5):
    driver.get(f'https://www.google.com/search?q={query}')

    for _ in range(num_scrolls):
        scroll_page(driver)

    search_results_container = driver.find_element(By.ID, value='main')
    result_elements = search_results_container.find_elements(By.CLASS_NAME, value='MjjYud')

    title_list = []
    description_list = []
    url_list = []

    for result_element in result_elements:
        try:
            title_element = result_element.find_element(By.CSS_SELECTOR, value="h3.LC20lb.MBeuO.DKV0Md")
            description_element = result_element.find_element(By.CSS_SELECTOR, value="div.VwiC3b.yXK7lf.lyLwlc.yDYNvb.W8l4ac.lEBKkf")
            link_element = result_element.find_element(By.CSS_SELECTOR, value="a")

            title = title_element.text
            description = description_element.text
            link = link_element.get_attribute('href')

            title_list.append(title)
            description_list.append(description)
            url_list.append(link)

        except Exception as e:
            pass

    driver.quit()

    return title_list, description_list, url_list

def to_csv(title_list, description_list, url_list, file_path):
    data_dict = {
        'Title': title_list,
        'Description': description_list,
        'URL': url_list
    }
    dataframe = pd.DataFrame(data=data_dict)
    dataframe.to_csv(file_path, index=False)

if __name__ == '__main__':
    search_query = 'Internshala'
    edge_driver = Edge()  # Use Microsoft Edge WebDriver
    titles, descriptions, urls = extract_info(edge_driver, search_query)
    to_csv(titles, descriptions, urls, './search_results.csv')


# In[ ]:




