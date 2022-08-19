from selenium import webdriver  
import time  
import random
from selenium.webdriver.common.keys import Keys  
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from newspaper import Article
from lxml import etree
import pandas as pd
import re
#'union bank nxt','moj lite','BYJUS – The Learning App','Hotstar','KFC Online Order and Food Delivery','Paytm for Business','Snapseed','snap chat','messenger','Telegram X','Gmail','Firefox Fast & Private Browser','Google Chat','imo-International Calls & Chat','spotify','VLC for Android','ZEE5:Movies, Web Series & more','Microsoft Word','Google Keep','InColor: Coloring & Drawing','Gallery - Hide Photos & Videos','UMANG','Uber - Request a ride','OYO','Tata CLiQ Shopping App India','Unacademy Learner App',
keywords=['Amazon','Amazon Alexa','Google Fit']
                
for k in keywords:

                driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
                #reddit url
                base_url="https://play.google.com/store/apps"
                driver.get(base_url)

                #sending tag words to the search bar
                driver.find_element_by_xpath("//button[@class='VfPpkd-Bz112c-LgbsSe yHy1rc eT1oJ DiOXab']").click()
                driver.find_element(By.XPATH,"//input[@class='HWAcU']").send_keys(k)
                driver.find_element(By.XPATH,"//input[@class='HWAcU']").send_keys(Keys.ENTER)
                time.sleep(5)
                driver.find_element(By.XPATH,"//div[@class='ipRz4']").click()
                time.sleep(5)
                driver.find_element_by_xpath("//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d qfvgSe aLey0c']").click()

                element = driver.find_element_by_xpath("//div[@class='fysCi']")



                time.sleep(5)
                print(f'Reviews Collecting from {k}')
                for i in tqdm(range(300)):
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
                    
                time.sleep(50)
                reviews_texts=[review.text for review in driver.find_elements_by_xpath("//div[@class='odk6He']//div[@class='RHo1pe']//div[@class='h3YV2d']")]

                print(len(reviews_texts))
                review_dates=[review.text for review in driver.find_elements_by_xpath("//div[@class='odk6He']//div[@class='RHo1pe']//header[@class='c1bOId']//span[@class='bp9Aid']")]
                review_stars=[re.findall(r'\d+', str(review.get_attribute('aria-label')))[0] for review in driver.find_elements_by_xpath("//div[@class='odk6He']//div[@class='RHo1pe']//header[@class='c1bOId']//div[@class='iXRFPc']")]
                #review_names=[review.text for review in driver.find_elements_by_xpath("//div[@class='odk6He']//div[@class='RHo1pe']//header[@class='c1bOId']//div[@class='gSGphe']//div[@class='X5PpBb']")]


                df = pd.DataFrame(
                    {'app_name': [k]*len(reviews_texts),
                     'review_text': reviews_texts,
                     'review_dates': review_dates,
                'no_stars':review_stars})
                df['review_dates']=pd.to_datetime(df['review_dates'])
                df.to_csv(f'{k}_reviews.csv')

                driver.close()
