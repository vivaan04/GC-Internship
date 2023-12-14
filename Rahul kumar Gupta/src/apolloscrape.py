from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import log_info, log_error
from fastapi import FastAPI
from fastapi.responses import FileResponse
import time
import pandas as pd
import os
from pydantic import BaseModel
import logging
import requests
import re
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import io

app=FastAPI()

class ScrapeRequest(BaseModel):
    "Validate that requested data is in correct format"
    # file_name: str
    link: str

class ApolloScrapeAutomation:    
    def __init__(self, driver_path):
        """
        Initialize the class with the driver path and create a DataFrame attribute.
        
        Parameters:
        - driver_path (str): The path to the Chrome driver executable.
        """
        # Create an empty DataFrame attribute
        self.df = pd.DataFrame()

        # Create ChromeOptions object with headless options
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # Create a Service object with the specified driver path
        service = Service(driver_path)
        
        # Create a Chrome driver with the ChromeOptions and Service objects
        self.driver = Chrome(options=chrome_options, service=service)

        # Maximize the window of the Chrome driver
        self.driver.maximize_window()
    
    def Login(self):
        self.driver.get("https://app.apollo.io/#/login")
       
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//input[contains(@name, "email")]')))
        self.driver.find_element(By.XPATH, '//input[contains(@name, "email")]').send_keys("grahulkumar2002@gmail.com")
     
        self.driver.find_element(By.XPATH, '//input[contains(@name, "password")]').send_keys("Rahul@123456")
 
        self.driver.find_element(By.XPATH, '//button[.= "Log In"]').click()

    def upload_csv(self,container_name,filename,df,connection_string):
        # Initialize a BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container_name, filename)
        # Convert the Pandas DataFrame to a CSV string
        csv_content = df.to_csv(index=False)
        
        # Convert the CSV content to bytes
        csv_bytes = io.BytesIO(csv_content.encode())
        
        # Upload the CSV content as the blob
        blob_client.upload_blob(csv_bytes, blob_type="BlockBlob", overwrite=True)


    def get_email(self, df):
        """
        Retrieve email and contact information from a DataFrame and save it to a CSV file.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            campaign_name (str): The name of the campaign.

        Returns:
            None
        """
        log_info("Retrieving email and contact information...")
        for index, row in df.iterrows():
            name_url = row['Name_url']
            self.driver.get(name_url)

            #wait 5 seconds to load
            time.sleep(5)
            # Click the button
            try:
                button_xpath = "/button[contains(@class, 'zp-button') and contains(@class, 'zp_zUY3r') and contains(@class, 'zp_n9QPr') and contains(@class, 'zp_rhXT_')]"
                self.driver.find_element(By.XPATH, button_xpath).click()
            except Exception:
                pass

            # Retrieve email
            try:
                email_xpath = "//div[contains(@class, 'zp_jcL6a')]//a[contains(@class, 'zp-link') and contains(@class, 'zp_OotKe') and contains(@class, 'zp_dAPkM') and contains(@class, 'zp_Iu6Pf')]"
                # email_cls = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, email_xpath)))
                email_cls = self.driver.find_element(By.XPATH, email_xpath)
                email = email_cls.text
            except:
                email = ''

            # Retrieve contact number
            time.sleep(2)
            try:
                contact_xpath = "//div[contains(@class, 'zp_NGej_')]//a[contains(@class, 'zp-link') and contains(@class, 'zp_OotKe') and contains(@class, 'zp_lmMY6')]/span"
                # contact_cls = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, contact_xpath)))
                contact_cls= self.driver.find_element(By.XPATH, contact_xpath)
                contact_number = contact_cls.text
            except:
                contact_number = ''

            # Update the DataFrame
            df.at[index,"Email"] = email
            df.at[index, 'Contact'] = contact_number

        return df


    # def get_next_page(self):
    #     """
    #     This function finds and clicks the next button on a page.
        
    #     Returns:
    #         next_button (WebElement): The next button element if found, otherwise None.
    #     """
    #     try:
    #         # Find the next button element using XPATH
    #         next_button = self.driver.find_element(By.XPATH, "//button[@class='zp-button zp_zUY3r zp_MCSwB zp_xCVC8' and @aria-label='right-arrow']")
            
    #         # Click the next button
    #         next_button.click()
            
    #         # Add a sleep to allow the page to load (replace this with WebDriverWait if possible)
    #         time.sleep(5)
    #     except Exception as e:
    #         # If an exception occurs, set next_button to None
    #         next_button = None
        
    #     # Return the next button element
    #     return next_button
        

    def scrape_url(self):
        """
        Scrapes data from a web page and returns a DataFrame.
        """
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@data-cy-loaded="true"]')))
        table = self.driver.find_elements(By.XPATH, '//div[@data-cy-loaded="true"]')
        rows = self.driver.find_elements(By.TAG_NAME, 'tr')
        temp_df = pd.DataFrame() 

        try:
            for index, row in enumerate(rows[1:]):
                try:
                    # Extract first name and last name from the name element
                    name = row.find_element(By.XPATH, './/div[@class="zp_xVJ20"]/a').text
                    first_name, last_name = name.split(" ")
                    temp_df.at[index, "First Name"] = first_name
                    temp_df.at[index, "Last Name"] = last_name
                    temp_df.at[index, "Name"] = name

                except Exception:
                    pass

                try:
                    # Extract name URL from the name element
                    name_url = row.find_element(By.XPATH, './/div[@class="zp_xVJ20"]/a').get_attribute("href")
                    temp_df.at[index, "Name_url"] = name_url
                except Exception:
                    pass

                try:
                    # Extract LinkedIn URL from the LinkedIn element
                    linkedin_url = row.find_element(By.XPATH, './/div[@class="zp_I1ps2"]/span/a').get_attribute("href")
                    temp_df.at[index, "Linkedin"] = linkedin_url
                except Exception:
                    pass         

                try:
                    # Extract title from the title element
                    title = row.find_element(By.XPATH, './/td[@class="zp_aBhrx"][2]//span[@class="zp_Y6y8d"]').text
                    temp_df.at[index, "Title"] = title
                except Exception:
                    pass

                try:
                    # Extract company name and company URL from the company element
                    company = row.find_element(By.XPATH, './/a[@class="zp_WM8e5 zp_kTaD7"]').text
                    temp_df.at[index, "Company"] = company
                    company_url = row.find_element(By.XPATH, './/td[@class="zp_aBhrx"][3]//div[@class="zp_I1ps2"]//a[@class="zp-link zp_OotKe"][1]').get_attribute("href")
                    temp_df.at[index, "Company_Url"] = company_url
                except Exception:
                    pass

                try:
                    # Extract address from the address element
                    caddress = row.find_element(By.XPATH, './/td[@class="zp_aBhrx"][5]//span[@class="zp_Y6y8d"]').text
                    temp_df.at[index, "Address"] = caddress
                except Exception:
                    pass 

                try:
                    # Extract employee count from the employee count element
                    employeecount = row.find_element(By.XPATH, './/td[@class="zp_aBhrx"][6]/span[@class="zp_Y6y8d"]').text
                    temp_df.at[index, "Employee Count"] = employeecount
                except Exception:
                    pass

                try:
                    # Extract industry from the industry element
                    industry = row.find_element(By.XPATH, './/td[@class="zp_aBhrx"][8]//span[@class="zp_lm1kV"]/div/span').text
                    temp_df.at[index, "Industry"] = industry
                except Exception:
                    pass

        except Exception as e:
            log_error(f"Exception occurred: {str(e)}")
        # Check if next button is available
        # if self.get_next_page():
        #     log_info("Next button found")
        #     self.df=pd.concat([self.df,temp_df],ignore_index=True)
        #     self.scrape_url()
        self.df=pd.concat([self.df,temp_df],ignore_index=True)
        return self.df
    
    def run_scraper(self, link):
        """
        Run the web scraper on the given URLs.

        Args:
            dic_urls (dict): A dictionary where the key is the campaign name and the value is the URL.

        Returns:
            None
        """
        # # Iterate over each campaign name and URL
        # for campaign_name, url in dic_urls.items():
        time.sleep(10)  # Wait for 10 seconds
        try:
            self.driver.get(link)  # Open the URL in the web driver
            time.sleep(10)  # Wait for 10 seconds
            df = self.scrape_url()  # Scrape the URL and get a DataFrame
            
            data= self.get_email(df)  # Get the email from the DataFrame
            self.driver.quit()  # Quit the web driver
            return data

        except Exception as e:
            self.driver.quit()  # Quit the web driver
            log_error(f"Exception occurred while scraping : {str(e)}")

            
    def send_email(self,recipient_email,email_body,file_content=None):
            # SMTP server settings for Gmail
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = "tttk6663@gmail.com"
            smtp_password = "evbpesdgjpefnxpy"
            sender_email = "tttk6663@gmail.com"
            # Create an instance of MIMEMultipart
            msg = MIMEMultipart()

            # Email subject
            msg['Subject'] = "Scraped Results"
            msg.attach(MIMEText(email_body, 'plain'))
            if file_content:
                attachment = MIMEApplication(file_content, _subtype="csv")
                attachment.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename="scraped_data.csv"
                )
                msg.attach(attachment)
                
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Start TLS (Transport Layer Security)
                server.login(smtp_username, smtp_password)  # Login to the SMTP server

                # Send the email
                server.sendmail(sender_email, recipient_email, msg.as_string())
        
        

@app.post('/scrape')
async def start(request: ScrapeRequest):
    log_info("Scraper running...")
    apolloio = ApolloScrapeAutomation("/home/rahuldevs/chromedriver_linux64/chromedriver")
    apolloio.Login()
    data=apolloio.run_scraper(request.link)

    # Define your Azure Blob Storage connection string
    connection_string = "DefaultEndpointsProtocol=https;AccountName=gmaps9f62;AccountKey=+d1hzstmPLCewuYgsiCbSc7aucpycZdNXjTpzHJH2bab8rNySNRy9fHycu+LywPdp8VuCzdbWQCH+ASt6KaUOA==;EndpointSuffix=core.windows.net"
    container_name = "test"
    blob_name = "scraped_data.csv"
    # Upload the CSV file to Azure Blob Storage
    apolloio.upload_csv(container_name, blob_name, data,connection_string)

    # Get the current directory
    curr_dir=os.getcwd()

    # Save the DataFrame to a CSV file
    csv_file="scraped_data.csv"
    data.to_csv(csv_file, index=False)

    #generating full path
    full_path = os.path.join(curr_dir, csv_file)
    
    #Email generation
    email_body="The Scraped Data has been added to the blob. Please check it."
    recipient_email="agneynalapat123@gmail.com"
    with open(full_path, 'rb') as file:
            file_content = file.read()
            apolloio.send_email(recipient_email,email_body,file_content=file_content)
    
    log_info("Scraper completed!")
    return FileResponse(csv_file, media_type="text/csv", filename="scraped_data.csv")
    