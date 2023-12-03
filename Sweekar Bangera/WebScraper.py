import pandas as pd
from selenium.webdriver import Edge  # Import Edge instead of Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import logging

class GetSearchResults:

    def __init__(self, query: str, n_scrolls: int = 3, output_file: str = './search_result.csv') -> None:
        self.driver = Edge()  # Use Edge instead of Chrome
        self.url = []
        self.description = []
        self.title = []
        self.query = query
        self.n_scrolls = n_scrolls
        self.output_file = output_file

        try:
            self._search_google()
            self._extract_info()
            self.to_csv()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
        finally:
            self._close_connection()

    def _search_google(self):
        logging.info(f"Searching Google for: {self.query}")
        self.driver.get(f'https://www.google.com/search?q={self.query}')

        for _ in range(self.n_scrolls):
            self._scroll_page()

    def _scroll_page(self):
        body = self.driver.find_element(By.TAG_NAME, value="body")
        body.send_keys(Keys.END)
        time.sleep(5)

    def _extract_info(self):
        self.results = self.driver.find_element(By.ID, value='main')
        html_elements = self.results.find_elements(By.CLASS_NAME, value='MjjYud')

        for element in html_elements:
            try:
                heading = element.find_element(By.CSS_SELECTOR, value="h3.LC20lb.MBeuO.DKV0Md")
                des = element.find_element(By.CSS_SELECTOR, value="div.VwiC3b.yXK7lf.lyLwlc.yDYNvb.W8l4ac.lEBKkf")
                link = element.find_element(By.CSS_SELECTOR, value="a").get_attribute('href')
                self.title.append(heading.text)
                self.description.append(des.text)
                self.url.append(link)
            except Exception as e:
                logging.warning(f"Failed to extract information from an element: {str(e)}")

        logging.info('Information extracted successfully')

    def to_csv(self):
        data_dict = {
            'Title': self.title,
            'Description': self.description,
            'URL': self.url
        }
        dataframe = pd.DataFrame(data=data_dict)
        dataframe.to_csv(self.output_file, index=False)
        logging.info(f'CSV file created: {self.output_file}')

    def _close_connection(self):
        self.driver.quit()
        logging.info('Closing connection')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    query = 'internshala'
    obj = GetSearchResults(query, n_scrolls=3, output_file='./search_result.csv')
