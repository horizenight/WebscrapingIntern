from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
import time
import datetime
from selenium.webdriver.support.wait import WebDriverWait 

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options

import json
import os 
CHROMEDRIVER_PATH =  r'/usr/local/bin/chromedriver'
chrome_binary_path = '/usr/bin/google-chrome'

print(os.path.exists(CHROMEDRIVER_PATH))
WINDOW_SIZE = "1920,1080"
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "normal" 
options = webdriver.chrome.options.Options()
options.add_argument("--start-maximized");
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
options.add_argument("--window-size=%s" % WINDOW_SIZE)
options.add_argument('--no-sandbox')
chrome_driver_binary = chrome_binary_path
driver =  webdriver.Chrome(desired_capabilities=caps, executable_path=CHROMEDRIVER_PATH,chrome_options=options)
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

# setup Selenium Browser Above 



time.sleep(10)

with open('Links2018.json') as json_file:
       data = json.load(json_file)

print(data)


driver.get(data[0])
driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/div/p[2]/a[22]").click()
time.sleep(4)
driver.find_element(By.XPATH,"/html/body/div[3]/div[1]/ul[3]/li[1]/a").click()

time.sleep(10)
# driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/div[5]/div/ul[3]/li[3]/a").click()
time.sleep(4)

pages = driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div/div[2]/b[2]").text
pages = int(pages)

time.sleep(10)



title_list=[]
authors_list=[]
affilations_list=[]
session_list=[]
citation_list=[]
abstract_list=[]
conference_name="EULAR 2018"
conference_name_list=[]
for link in data:
        authors=[]
        affilations=[]
        conference_name_list.append(conference_name)
        driver.get(link)
        time.sleep(4)
    
        try:
            title = driver.find_element(By.CLASS_NAME,"title").text
        except Exception as e:
            title=""

        title_list.append(title)
        try:
            author = driver.find_element(By.CLASS_NAME,"authors").text
            
        except Exception as e:
            author=""
        authors.append(author)
        authors_list.append(authors)
        
        
        try:
            affilation=driver.find_element(By.CLASS_NAME,"affiliations").text
           
        except Exception as e:
            affilation=""
        affilations.append(affilation)
        affilations_list.append(affilations)
        
        
        try:
            citation = driver.find_element(By.CLASS_NAME,"citations_etc").text
            
        except Exception as e:
            citation=""
        citation_list.append(citation)
              
        
        try:
            session = driver.find_element(By.CLASS_NAME,"session").text
           
        except Exception as e:
            session=""
        
        session_list.append(session)

       
        try:
            abstract = driver.find_elements(By.CSS_SELECTOR,"#page-content-wrapper > div > div > div > div > p")
            abstract_text=[]
            for elem in abstract:
                    abstract_text.append(elem.text)
        except Exception as e:
             abstract_text=[]
        
        abstract_list.append(abstract_text)
       
                

d = {"links":data,"title":title_list,"session_list":session_list , 
                 "authors_list":authors_list,"affilation_list":affilations_list,"conference_name_list":conference_name_list,"abstract_list": abstract_list,"citation_list":citation_list
                  }
# d = {"title":len(title_list),"session_list":len(session_list) , 
#                  "authors_list":len(authors_list),"affilation_list":len(affilations_list),"conference_name_list":len(conference_name_list),"abstract_list": len(abstract_list),"citation_list":len(citation_list)
#                   }
          
    
with open(f"Data2018.json", "w") as f:
            json.dump(d,f)


df = pd.DataFrame.from_dict(d)
print(df)


df.to_excel('EULAR_2018.xlsx', index=False)
            

            
print("Done Scraping")
time.sleep(10)
driver.close()