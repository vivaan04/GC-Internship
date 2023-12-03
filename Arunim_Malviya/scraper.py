import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class GetSearchResults:
    
    def __init__(self,search_query: str,n_scrolls: int = 3) -> None:        
        # Initializing the class by setting up the Chrome WebDriver and initializing empty lists for storing data.
        self.driver = Chrome()
        self.search_urls = []
        self.search_descriptions = []
        self.search_titles = []
        self.driver.get(f'https://www.google.com/search?q={search_query}')
        
        for _ in range(n_scrolls):
            self._scroll_page()
        
        self._extract_info()
        
    def _scroll_page(self):
        body = self.driver.find_element(By.TAG_NAME,value="body")
        body.send_keys(Keys.END)
        time.sleep(2)

    def _extract_info(self):
        self.results = self.driver.find_element(By.ID, value='main')
        html_elements = self.results.find_elements(By.CLASS_NAME,value='MjjYud')
        
        for element in html_elements:
            try:
                heading = element.find_element(By.CSS_SELECTOR,value="h3.LC20lb.MBeuO.DKV0Md")
                des = element.find_element(By.CSS_SELECTOR,value="div.VwiC3b.yXK7lf.lyLwlc.yDYNvb.W8l4ac.lEBKkf")
                link = element.find_element(By.CSS_SELECTOR,value="a").get_attribute('href')
                self.search_titles.append(heading.text)
                self.search_descriptions.append(des.text)
                self.search_urls.append(link)

            except Exception as e:
                pass
            
        self.driver.quit()
            
    def to_csv(self,file_path):
        self.data_dict = {
            'search_titles': self.search_titles,
            'search_descriptions': self.search_descriptions,
            'search_urls': self.search_urls
        }
        dataframe = pd.DataFrame(data=self.data_dict)
        dataframe.to_csv(file_path,index=False)
        
if __name__ == '__main__':
    search_query = 'Internshala'
    obj = GetSearchResults(search_query)
    obj.to_csv('./search_reults.csv')
    
  