from selenium import webdriver
from selenium.webdriver.safari.service import Service # Change this to the appropriate driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os
import math
from datetime import datetime
import logging

class PropertyScraper:
    def __init__(self, base_url, api_key, pagination_url, num_pages=None):
        self.base_url = base_url
        self.api_key = api_key
        self.pagination_url = pagination_url
        self.num_pages = num_pages
        self.all_property_dict_link = {}
        self.driver = webdriver.Safari(service=Service()) # Change this to the appropriate driver


    def create_url(self, url=None):
        if url is None:
            parsed_url = f'{self.base_url}?api_key={self.api_key}&url={self.pagination_url}&country=us'
        else:
            parsed_url = f'{self.base_url}?api_key={self.api_key}&url={url}&country=us'
        return parsed_url
    

    def fetch_total_pages(self):
        try:
            logging.info(f"Fetching total number of pages")
            self.driver.get(self.create_url())
            properties_found_xpath = "//span[@class='search-results-listings-header__properties-found__number']"
            wait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, properties_found_xpath)))
            properties_found = self.driver.find_element(By.XPATH, properties_found_xpath)
            total_properties = float(properties_found.text.strip())
            self.num_pages = math.ceil(total_properties / 11.0)
            
            logging.info(f"Total number of properties: {total_properties}")
            logging.info(f"Calculated number of pages: {self.num_pages}")
        except Exception as e:
            logging.error(f"An error occurred in fetch_total_pages: {str(e)}")
        
    
    def scrape_pagination_links(self):
        try:
            for page_number in range(1, self.num_pages + 1): 
                try:
                    url = f'{self.pagination_url}?search=true&regions%5B0%5D=8&regions%5B1%5D=1&regions%5B2%5D=17&regions%5B3%5D=114&regions%5B4%5D=12&regions%5B5%5D=9&regions%5B6%5D=5&regions%5B7%5D=11&regions%5B8%5D=14&regions%5B9%5D=15&regions%5B10%5D=13&regions%5B11%5D=4&regions%5B12%5D=6&regions%5B13%5D=16&regions%5B14%5D=31&regions%5B15%5D=10&regions%5B16%5D=7&regions%5B17%5D=115&regions%5B18%5D=3&regions%5B19%5D=2&regions%5B20%5D=257&parent=1&pageNumber={page_number}'
                    
                    visit_url = self.create_url(url)
                    self.driver.get(visit_url)
                    ul_element_xpath = "//ul[@class='search-results-listings-list']"
                    wait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, ul_element_xpath)))
                    ul_element = self.driver.find_element(By.XPATH, ul_element_xpath)
                    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
                    for li_element in li_elements:
                        try:
                            a_element = li_element.find_element(By.TAG_NAME, 'a')
                            self.all_property_dict_link[li_element.get_attribute('id')] = a_element.get_attribute('href')
                        except NoSuchElementException:
                            logging.info(f'No <a> tag found within <li> element.')
                except Exception as e:
                    logging.error(f'Could not retreive the page {self.create_url(url)} successfully in link extraction. Error: {str(e)}')
        except Exception as e:
            logging.error(f"An error occurred in scrape_pagination_links: {str(e)}")
    
    def scrape_property_details(self):
        try:
            columns = ['URL', 'Date', 'Type', 'Street Address', 'City', 'Region', 'Phone Numbers', 'Solicitation Message', 'Asking Price', 'Municipal Assessment']
            df = pd.DataFrame(columns=columns)
            for listing_id, url in self.all_property_dict_link.items():
                try:
                    visit_url = self.create_url(url)
                    logging.info(f"Visiting {listing_id} - {visit_url}")
                    phoneNumbers = solicitation_message = asking_price = municipal_assessment = type = street = city = region = None
                    date = datetime.now()
                    
                    self.driver.get(visit_url)
                    
                    type_xpath = "//h3[@class='listing-location__title']"
                    address_xpath = "//div[@class='listing-location__address']"
                    
                    wait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, type_xpath)))
                    type = self.driver.find_element(By.XPATH, type_xpath).text.strip()
                    try:
                        address_element = self.driver.find_element(By.XPATH, address_xpath)
                        street_address = address_element.find_element(By.TAG_NAME, 'h1').text.strip()
                        street  = street_address
                        span_element = address_element.find_element(By.TAG_NAME, 'h2')
                        city_element, region_element = span_element.find_elements(By.TAG_NAME, 'span')
                        city = city_element.text.strip()
                        region = region_element.text.strip()
                    except NoSuchElementException:
                        logging.info('Address element not found.')
                    
                    phone_numbers_xpath = "//a[@class='gtm-listing-link-contact-owner-phone']"
                    
                    phone_numbers = [phone_number_element.find_element(By.TAG_NAME, 'span').text.strip() for phone_number_element in self.driver.find_elements(By.XPATH, phone_numbers_xpath)]
                    phone_numbers = list(set(phone_numbers))
                    phoneNumbers = ', '.join(phone_numbers)
                    
                    message_xpath = "//p[@class='listing-contact__no-solicitations-body']"
                    try:
                        message = self.driver.find_element(By.XPATH, message_xpath)
                        solicitation_message = 'y'
                    except NoSuchElementException:
                        solicitation_message = 'n'
                    
                    characteristics_viewports_xpath = "//div[@class='listing-list-characteristics__viewport']"
                    characteristics_viewports = self.driver.find_elements(By.XPATH, characteristics_viewports_xpath)
                    
                    for viewport in characteristics_viewports:
                        # Find all the listing-box__dotted-row elements within the current viewport
                        dotted_row_xpath = "//div[@class='listing-box__dotted-row']"
                        dotted_rows = viewport.find_elements(By.XPATH, dotted_row_xpath)
                        
                        for dotted_row in dotted_rows:
                            # Extract the text content of the first div (characteristic name)
                            characteristic_name = dotted_row.find_element(By.TAG_NAME, 'div').text.strip()

                            # Extract the text content of the third div (characteristic value)
                            characteristic_value = dotted_row.find_elements(By.TAG_NAME, 'div')[2].text.strip()
                            
                            # Check if the characteristic name is "Asking Price" or "Municipal Assessment"
                            if characteristic_name == 'Asking Price':
                                asking_price1 = characteristic_value
                                asking_price = asking_price1
                            elif characteristic_name == 'Municipal Assessment':
                                municipal_assessment1 = characteristic_value
                                municipal_assessment = municipal_assessment1
                    
                    df = pd.concat([df, pd.DataFrame([{
                        'URL': url,
                        'Date': date,
                        'Type': type,
                        'Street Address': street,
                        'City': city,
                        'Region': region,
                        'Phone Numbers': phoneNumbers,
                        'Solicitation Message': solicitation_message,
                        'Asking Price': asking_price,
                        'Municipal Assessment': municipal_assessment
                    }])], ignore_index=True)
    
                except Exception as e:
                    logging.error(f'Could not retreive the page {self.create_url(url)} successfully in propery_details. Error: {str(e)}')
            
            return df
    
        except Exception as e:
            logging.error(f"An error occurred in scrape_property_details: {str(e)}")
         
    def saveToCSV(self, df):
        df.to_csv('output.csv', index=False)
        logging.info(f"CSV file saved successfully")
        
# if __name__ == '__main__':
#     try:
#         # Create a scraper instance without specifying the num_pages
#         scraper = PropertyScraper(base_url, api_key, pagination_url, num_pages=None)

#         # Fetch total number of pages and set it to the scraper instance
#         scraper.fetch_total_pages()

#         # Check if total pages fetched successfully
#         if scraper.num_pages is not None:
#             # Now we generate the link for each page after having the updated num_pages and store the page links in a dictionary
#             scraper.scrape_pagination_links()

#             # Now you can use the scraper to iterate all the links inside the dictionary and fetch the required fields
#             property_df = scraper.scrape_property_details()

#             # Convert the DataFrame to a JSON response
#             # property_json = property_df.to_json(orient='records')

#             logging.info({"property_details": property_df})
#         else:
#             logging.error({"error": "Failed to fetch total number of pages."})
#     except Exception as e:
#         logging.error({"error": f"An error occurred: {str(e)}"})