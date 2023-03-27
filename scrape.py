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


try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"


caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "normal" 
options = webdriver.chrome.options.Options()
options.add_argument("--start-maximized");
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver =  webdriver.Chrome(desired_capabilities=caps, executable_path=r'/usr/local/bin/chromedriver',chrome_options=options)
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

conference_name = "ASN 2022"


with open('LinksPub.json') as json_file:
       data = json.load(json_file)


title_list = []
time_list=[]
date_list=[]
location_list=[]
category_list=[]
abstract_list=[]
authors_list=[]
funding_list=[]
conference_name_list=[]
conference_name="ASN 2022"

for url in data:
        conference_name_list.append(conference_name)
        driver.get(url)
        print(url)
        try:
                title = driver.find_element(By.CSS_SELECTOR,"#content > div.abstract_content > h3").text
        except Exception as e :
                title=""
        title_list.append(title)

        try:
            input_str= driver.find_element(By.CSS_SELECTOR,"#content > div.abstract_content > ul.list.list1.abstract_session > li > span").text
            date_str = input_str.split("|")[0].strip()
      

            # Extract location
            location_str = input_str.split("|")[1].split("\n")[0].replace("Location:", "").strip()

            # Extract start and end times
            time_range_str = input_str.split("\n")[-1].strip()
        except Exception as e:
            input_str=""
            date_str=""
            location_str=""
            time_range_str=""
   
        time_list.append(time_range_str)
        date_list.append(date_str)
        location_list.append(location_str)
        
        try: 
            category= driver.find_element(By.CSS_SELECTOR,"#content > div.abstract_content > h4:nth-child(6)").text
        except Exception as e:
            category=""

        category_list.append(category)
         
        try:
            abstract = driver.find_elements(By.CSS_SELECTOR,"#content > div.abstract_content > p")
            abstract_data=[]
            for elem in abstract:
                    abstract_data.append(elem.text)
        except Exception as e:
              abstract_data=[]
        abstract_list.append(abstract_data)

        try:
            authors = driver.find_elements(By.CSS_SELECTOR,"#content > div.abstract_content > ul:nth-child(9) > li")
            authors_data=[]
            for elem in authors:
                authors_data.append(elem.text)
        except Exception as e:
              authors_data=[]
        authors_list.append(authors_data)

       

        try:
             funding = driver.find_element(By.XPATH,"/html/body/div[1]/section[2]/div/div/div[2]/div/div[4]/ul[5]/li").text
        except Exception as e:
              funding=""
        funding_list.append(funding)

   
d = {"title":title_list,"url":data,"session_list":category_list , 
                 "authors_list":authors_list,"location_list":location_list,"time_list":time_list,"date_list":date_list,"conference_name_list":conference_name_list,"abstract_list": abstract_list,"funding_list":funding_list
                  }
# d = {"title":len(title_list),"session_list":len(session_list) , 
#                  "authors_list":len(authors_list),"affilation_list":len(affilations_list),"conference_name_list":len(conference_name_list),"abstract_list": len(abstract_list),"citation_list":len(citation_list)
#         
# 
#           }

driver.close()

with open(f"data2022.json", "w") as f:
                json.dump(d,f)

          

df = pd.DataFrame.from_dict(d)
print(df)


df.to_excel('ASN_2022.xlsx',index=False)


