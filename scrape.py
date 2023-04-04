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

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "normal" 
options = webdriver.chrome.options.Options()
options.add_argument("--start-maximized");
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver =  webdriver.Chrome(desired_capabilities=caps, executable_path=r'C:\Development\chromedriver.exe',chrome_options=options)
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

conference_name = "ASN 2021"


with open('LinksPub.json',encoding='utf-8') as json_file:
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
conference_name="ASH 2021"

for i in range(0,len(data)):
        url = data[i]
        conference_name_list.append(conference_name)
        driver.get(url)
        print(url)
        time.sleep(5)

        try:    
                title = driver.find_element(By.CLASS_NAME,"article-title-main").text 
                print(title)           
        except Exception as e :
                
                title=""
        title_list.append(title)

      
        try:
            date_str = driver.find_element(By.CLASS_NAME,"article-date").text
           
            date_obj =datetime.datetime.strptime(date_str, "%B %d, %Y")
           
            formatted_date_str = date_obj.strftime("%d-%m-%Y")
            
          
            date_str = formatted_date_str
          

        
      

            # Extract location
           

            # Extract start and end times
            
        except Exception as e:
            print(e)
            date_str=""
          
   
       
        date_list.append(date_str)
      
        

        try: 
            category= driver.find_element(By.CLASS_NAME,"article-client_type").text
        except Exception as e:
            category=""

        category_list.append(category)
         
       
        try:
            abstract = driver.find_element(By.ID,"ContentTab").text
            
            
        except Exception as e:
              abstract=""

        abstract_list.append(abstract)

        try:
            authors = driver.find_element(By.CLASS_NAME,"al-authors-list").text
            print(authors)
            # authors_data=[]
            # for elem in authors:
            #     authors_data.append(elem.text.split(','))
        except Exception as e:
              authors=""
        authors_list.append(authors)

       


        
        d = {"title":title_list,"url":data[0:i],"session_list":category_list , 
                        "authors_list":authors_list,"location_list":location_list,"time_list":time_list,"date_list":date_list,"conference_name_list":conference_name_list,"abstract_list": abstract_list,"funding_list":funding_list
                        }
        
        with open(f"data2021_2.json", "w") as f:
                        json.dump(d,f)
    


d = {"url":data,"title":title_list,"Session Type":category_list , 
                        "Authors":authors_list,"Date":date_list,"Conference":conference_name_list,"Abstracts": abstract_list
                        }


driver.close()

with open(f"data2021_3.json", "w") as f:
                json.dump(d,f)

          

df = pd.DataFrame.from_dict(d)
print(df)


df.to_excel('ASN_2021_3.xlsx',index=False)


