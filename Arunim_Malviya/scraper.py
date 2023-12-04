import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class GetSearchResults:
    def __init__(self, search_query: str, n_scrolls: int = 2) -> None:
        # Initializing the class by setting up the Chrome WebDriver and initializing empty lists for storing data.
        self.driver = Chrome()
        self.search_urls = []
        self.search_descriptions = []
        self.search_titles = []
        
        # Navigating to Google search results page based on the search_query provided.
        self.driver.get(f'https://www.google.com/search?q={search_query}')
        
        # Scrolling the page a specified number of times (default: 2) to load more search results.
        for _ in range(n_scrolls):
            self._scroll_page()
        
        # Extracting information from the loaded search results.
        self._extract_info()
        
    def _scroll_page(self):
        # Method to scroll down the page by simulating the END key press and waiting for page content to load.
        body = self.driver.find_element(By.TAG_NAME, value="body")
        body.send_keys(Keys.END)
        time.sleep(2)

    def _extract_info(self):
        # Extracting relevant information (titles, descriptions, and URLs) from the search results.
        self.results = self.driver.find_element(By.ID, value='main')
        html_elements = self.results.find_elements(By.CLASS_NAME, value='MjjYud')
        
        # Looping through each search result element to extract required data.
        for element in html_elements:
            try:
                # Finding and extracting the title, description, and URL elements.
                heading = element.find_element(By.CSS_SELECTOR, value="h3.LC20lb.MBeuO.DKV0Md")
                des = element.find_element(By.CSS_SELECTOR, value="div.VwiC3b.yXK7lf.lyLwlc.yDYNvb.W8l4ac.lEBKkf")
                link = element.find_element(By.CSS_SELECTOR, value="a").get_attribute('href')
                
                # Storing extracted data into respective lists.
                self.search_titles.append(heading.text)
                self.search_descriptions.append(des.text)
                self.search_urls.append(link)

            except Exception as e:
                # Handling exceptions that might occur during extraction, allowing the loop to continue.
                pass
            
        # Closing the WebDriver once data extraction is completed.
        self.driver.quit()
            
    def to_csv(self, file_path):
        # Saving extracted data into a CSV file using Pandas DataFrame.
        self.data_dict = {
            'search_titles': self.search_titles,
            'search_descriptions': self.search_descriptions,
            'search_urls': self.search_urls
        }
        dataframe = pd.DataFrame(data=self.data_dict)
        dataframe.to_csv(file_path, index=False)
        
# Running the code if executed directly, performing a search and saving results to a CSV file.
if __name__ == '__main__':
    search_query = 'Internshala'  # Define the search query
    obj = GetSearchResults(search_query)  # Creating an instance of GetSearchResults
    obj.to_csv('./search_result.csv')  # Saving the search results into a CSV file
