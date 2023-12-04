import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Function to scroll the page n times
def scroll_page(driver, n_scrolls):
    for _ in range(n_scrolls):
        body = driver.find_element(By.TAG_NAME, value="body")
        body.send_keys(Keys.END)
        time.sleep(2)  

# Function to extract information from Google search results
def extract_info(driver, query, n_scrolls):
    url = []
    description = []
    title = []
    
    driver.get(f'https://www.google.com/search?q={query}')
    scroll_page(driver, n_scrolls)

    results = driver.find_element(By.ID, value='main')
    html_elements = results.find_elements(By.CLASS_NAME, value='MjjYud')

    for element in html_elements:
        try:
            heading = element.find_element(By.CSS_SELECTOR, value="h3.LC20lb.MBeuO.DKV0Md")
            des = element.find_element(By.CSS_SELECTOR, value="div.VwiC3b.yXK7lf.lyLwlc.yDYNvb.W8l4ac.lEBKkf")
            link = element.find_element(By.CSS_SELECTOR, value="a").get_attribute('href')
            title.append(heading.text)            # Append extracted information to respective lists
            description.append(des.text)
            url.append(link)
        except Exception as e:
            pass  

    return title, description, url

# Function to save extracted information to a CSV file
def save_to_csv(title, description, url, file_path):
    # Create a dictionary from extracted information
    data_dict = {
        'Title': title,
        'Description': description,
        'URL': url
    }
    # Convert the dictionary to a Pandas DataFrame
    dataframe = pd.DataFrame(data=data_dict)
    dataframe.to_csv(file_path, index=False)  

# Main function to perform the search, extract information, and save to CSV
def get_search_results(query, n_scrolls=6, file_path='./Amit_Acharekar/search_result.csv'):
    driver = Chrome()
    title, description, url = extract_info(driver, query, n_scrolls)
    save_to_csv(title, description, url, file_path)
    driver.quit()

if __name__ == '__main__':
    query = 'internshala'
    # Call the main function to get search results and save them to a CSV file
    get_search_results(query)
