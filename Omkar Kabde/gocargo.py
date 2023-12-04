import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import requests
from bs4 import BeautifulSoup
import pandas as pd

#Initialising Edge Driver
edgeService = Service(r"c:\\Users\\omkar\\Downloads\\msedgedriver.exe")
edgeDriver = webdriver.Edge(service=edgeService)

#Searching 'internshala' on google
edgeDriver.get('https://www.google.com')
search = edgeDriver.find_element("name", "q")
search.send_keys("internshala")
search.submit()
time.sleep(10)

#Creating empty pandas dataframe
df=pd.DataFrame({'Link':[],'Title':[],"Description":[]})

#Searching for all links in the webpage
wait = WebDriverWait(edgeDriver, 10)
links = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@href]')))
idx=0
#Looping through all links to get the link address, page title and page meta description
for i in links:
    link=i.get_attribute('href')
    title=i.text
    try:
        soup=BeautifulSoup(requests.get(link).content,"html.parser")
        desc=soup.find("meta", attrs={'name': 'description'}).get('content')
        # desc=soup.find("meta",property="og:description")['content']
    except:
        desc=''
    df.loc[idx]=[link,title,desc]
    idx+=1
edgeDriver.quit()

#Writing the dataframe to the csv file
df.to_csv("output.csv")

# meta[@name='description'/@content]

