import email
import imaplib
import sys
# setting path to GoCargo Folder
sys.path.append(r'/home/azureuser/')
from goCargo import common_functions as gc
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import time
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import pandas as pd
import numpy
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1920, 1080))
display.start()

####CONFIG VARIABLES######################################
filters='&auctionTitle=Eastern%20Canada%20Auction'
url='https://app.eblock.com/pending/in-if-bid'
logfile='ifBids247.log'
book_name='IF-BID-Eblock'
sheet_name='IF-BID-2'
####CONFIG VARIABLES######################################
log=gc.setLogs(logfile)
sheet=gc.gSheets_Setup(book_name,sheet_name)

urlz=[]

while True:
    now=datetime.today().strftime('%Y-%m-%d')
    try:
        df_db=gc.GetSheet(sheet)
        log.info("Successfully Read Google Sheet. Length of DataFrame: %s",len(df_db))
    except Exception as e:
        continue
    y=0
    df=pd.DataFrame()
    #time.sleep(360)
    try:
        driver,action=gc.setupWebdriver(profile_path='/home/azureuser/goCargo/Eblock_Profile_4')
        header=gc.LoginEblock(driver,action,filters,url)
        log.info("Successfully logged in. Page Header: %s",header)
    except Exception as e:
        continue
    while True:
        #First Try
        try:
            rows=gc.wait_for_elements(driver,"//li[@data-testid='list-item']")
            #First For
            for row in rows:
                try:
                    textstring=""
                    log.info("NEext ROw")
                    gc.nextRow(row,action)
                    vin=WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'titleContainer')]//p//strong"))).text
                    log.info(vin)
                    if vin in df_db['VIN'].to_list():
                        index = df_db['VIN'].to_list().index(vin)
                        if df_db['Status'].to_list()[index]!="":
                            log.info("Duplicate")
                            continue
                    try:
                        skipFlag,message,bid=gc.skipCheck(driver,row)
                        if skipFlag==1:
                            log.info("Skipped Listing: %s",message)
                            continue
                        else:
                            df.at[y,"Reserve Price"]=bid
                    except Exception as e:
                        log.info("Skip Listings Error: %s",e)
                        pass
                    
                    df.at[y,"VIN"]=vin
                    decl=gc.checkTags(driver)
                    df.at[y,'Tags']=", ".join([d for d in decl])
                    try:
                        seller=driver.find_element(By.XPATH,'//dt[contains(.,"Seller")]/following::dd').text
                        df.at[y,"Seller"]=seller
                    except Exception as e:
                        pass
                    try:
                        link=row.find_element(By.XPATH,".//a").get_attribute('href')
                        df.at[y,"Link"]=link
                    except Exception as e:
                        pass
                    
                    
                    
                    try:
                        a_date=driver.find_element(By.XPATH,'//dt[contains(.,"Date Ran")]/following::dd').text
                        auction_date=gc.checkDate(a_date)
                        df.at[y,'Auction Date']=auction_date
                    except Exception as e:
                        print("IF-BID has no Auction Date",e)
                        pass            
                    try:
                        countered = gc.CounterPrice(driver,y)
                        df.at[y,"Countered Price"]=countered
                    except Exception as e:
                        print("COunter Error,e")
                        df.at[y,"Countered Price"]="-"
                        pass
                    try:
                        
                        share=driver.find_element(By.XPATH,'//button[.="Share"]')
                        try:
                            action.move_to_element(share).perform()
                            print("Scrolled to share")
                        except Exception as e:
                            #print("movetoError",e)
                            pass
                        time.sleep(2)
                        share.click()
                        print("Clicked Share")
                        time.sleep(3)
                        
                        try:
                            driver.find_element(By.XPATH,"//button[@data-testid='slideOut-close-button']").click()
                        except Exception as e:
                            pass
                        try:
                            slink=driver.find_element(By.XPATH,"//input[contains(@value,'.com/share')]").get_attribute('value')
                        except Exception as e:
                            driver.find_element(By.XPATH,"//body").send_keys(Keys.ESCAPE)
                            print("Slink Error",e)
                            pass
                        driver.find_element(By.XPATH,"//button[@title='Close']").click()
                        features=driver.find_elements(By.XPATH,'//ul[contains(@class,"featureList")]//button')
                    except Exception as e:
                        log.info("Share Error %s",e)
                        pass
                    try:
                        cfamt=driver.find_element(By.XPATH,"//button[@data-testid='carfax-ca-button']//*[local-name()='svg']//following::span").text
                        df.at[y,"CARFAX Amount"]=cfamt
                    except Exception as e:
                        df.at[y,"CARFAX Amount"]=''
                        print("CFamt error",e)
                        pass
                    try:
                        vscore=driver.find_element(By.XPATH,"//button[@data-testid='score-button']//span").text
                        df.at[y,"Vehicle Score"]=vscore
                    except Exception as e:
                        df.at[y,"Vehicle Score"]=''
                        print("Vscore error",e)
                        pass
                    for f in features[:6]:
                        try:
                            action.move_to_element(f).perform()
                        except Exception as e:
                            pass
                        text=f.find_elements(By.XPATH,".//p")
                        df.at[y,text[0].text]=text[1].text
                        textstring=textstring+text[1].text+" "
                    try:
                        textstring=textstring+vin+" "+slink
                        print(textstring)
                        loc=driver.find_element(By.XPATH,"//div[contains(@data-testid,'pickupLocation-deta')]//div[contains(@class,'details')]//div[2]").text
                        df.at[y,'Location']=loc.split(",")[-1]
                    except Exception as e:
                        pass
                    
                    df.at[y,"String"]=textstring
                    df.at[y,"Date"]=now
                    y=y+1
                    print(y)
                    try:
                        save_and_close()
                    except Exception as e:

                        pass
                    
                except Exception as e:
                    pass
                try:
                    last_row=gc.clean_data(df)
                    last_row=last_row[~last_row['VIN'].isin(df[:-1]['VIN'])]
       
                    is_in_db = last_row[last_row['VIN'].isin(df_db['VIN'])]
                    #print("\n\nIs In DB?",len(is_in_db))
                    if len(is_in_db) > 0:
                        matching_indices = df_db[df_db['VIN'] == last_row['VIN'].values[0]].index.tolist()
                        if df_db['Status'].iloc[matching_indices[0]] == '':
                            # Exclude the row from last_row
                            last_row = None
                            log.info("Skipping Listing: Duplicate")
                    if last_row is not None:
                        last_row=last_row.fillna("")
                        last_row=last_row[['Link','Date',"Auction Date","Tags","Location",'VIN','Year','Make','Model','Trim','Mileage','Reserve Price','Countered Price','Seller','Whatsapp',"CARFAX Amount","Vehicle Score"]]
                        last_row=last_row.values.tolist()
                    #print("Type:",last_row,type(last_row))
                        if len(last_row)>0:
                            #print(last_row)
                            sheet.append_rows(last_row)
                            log.info("Appended Row")
                except Exception as e:
                    log.info("Data Writing Error %s",e)
                    pass
                
            try:
                nexts=driver.find_element(By.XPATH,'//a[contains(.,"Next")]')
                action.move_to_element(nexts).click().perform()
                count=driver.find_element(By.XPATH,'//span[contains(.,"results")]').text.replace("Showing ","").replace(" results",'').split(" out of ")
                left=count[0].split("-")[-1].strip()
                right=count[1]
                if left==right:
                    print("Left=Right, Breaking")
                    break
                log.info("\n\nNExt PAGE\n\n")
                log.info(driver.current_url)
                urlz.append(driver.current_url)
                time.sleep(5)
                try:
                    c,message_next=manual_next_ifbid(urlz)
                    log.info("Getting next Page: %s",message)
                    driver.get(c)
                    log.info("Getting c")
                    time.sleep(5)
                except Exception as e:
                    pass
            except Exception as e:
                print("Next Error",e)
                #driver.quit()
                break
            time.sleep(5)
        except Exception as e:
            print(e)
            #driver.quit()
            break
        driver.quit()
display.stop()
