 
import time  
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from lxml import etree
import pandas as pd
#driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

#reddit url
base_url="https://www.imdb.com/feature/genre/?ref_=nv_ch_gr"
#driver.get(base_url)
time.sleep(5)

#driver.get(str(base_url)+str(search_url))
data={'Moviename':[],'rating':[],'genre':[],'director':[],'cast':[],'writer':[],'summary':[]}

#header file
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
url=requests.get(base_url,headers=headers)
content=url.content
soup = BeautifulSoup(content,"html.parser")
dom = etree.HTML(str(soup))
title=list(zip(dom.xpath('//div[@class="article"]//div[@class="ab_ninja"]//div[@class="image"]/a/@href'),dom.xpath('//div[@class="article"]//div[@class="ab_ninja"]//div[@class="image"]/a/img/@title')))
import re

for t in title:
    
    url=requests.get(t[0],headers=headers)
    content=url.content
    soup = BeautifulSoup(content,"html.parser")
    page_links=[]
    page_links.append(t[0].replace('https://www.imdb.com',""))
    
    i=0
    while i < 1:
        
        met=soup.find(class_="lister-page-next next-page",href=True)['href']
        url=requests.get('https://www.imdb.com'+met,headers=headers)
        content=url.content
        soup = BeautifulSoup(content,"html.parser")
        page_links.append(met)
        i=i+1   
    print(str(t[1])+' genre')
    for li in page_links:
        
        url=requests.get('https://www.imdb.com'+li,headers=headers)
        content=url.content
        
        soup = BeautifulSoup(content,"html.parser")
    
        
        g_data = soup.find_all(class_= "lister-item mode-advanced")

     #   dom = etree.HTML(str(soup))
        for i in g_data:


                    try:
                        try:
                            
                        
                            title=i.find(class_="lister-item-header").find('a')
                            if title is not None:
                                title=title.text
                            else:
                                dirs='NA'
                       
                        except:
                            title='NA'
                        
                        try:
                            
                            ratings=i.find(class_= "inline-block ratings-imdb-rating").find('strong')                 
                            if ratings is not None:
                                ratings=ratings.text
                            else:
                                ratings='NA'
                       
                        except:
                            ratings='NA'
                            
                        try:
                            
                            genre=i.find(class_="genre")
                            if genre is not None:
                                genre=genre.text
                            else:
                                genre='NA'
                       
                        except:
                            genre='NA'
                        meta_link=i.find(class_="lister-item-header").find('a',href=True)
                        ml="https://www.imdb.com"+meta_link['href']
                        url=requests.get(ml,headers=headers)
                        content=url.content
                        soup = BeautifulSoup(content,"html.parser")
                        try:
                            
                            
                            dirs=soup.find(text=re.compile('Director')).parent.parent.find_all(class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link") 
                            if dirs is not None:
                                dirs=[dirss.text for dirss in dirs]
                            else:
                                dirs='NA'
                        except:
                            dirs='NA'
                        try:
                            stars=soup.find(text=re.compile('Stars')).parent.parent.find_all(class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
                            
                            if stars is not None:
                                stars=[star.text for star in stars]
                            else:
                                stars='NA'
                       
                        except:
                             stars='NA'
                        try:
                            
                            writer=soup.find(text=re.compile('Writer')).parent.parent.find_all(class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
                            if writer is not None:
                                writer=[writers.text for writers in writer]
                            else:
                                writer='NA'
                       
                        except:
                             writer= 'NA'
                        try:
                            
                            summary=soup.find(class_='ipc-html-content ipc-html-content--base').find('div')
                            if summary is not None:
                                summary=summary.text
                            else:
                                summary='NA'
                                            
                        except:
                            
                            summary='NA'
                        data['Moviename'].append(title)
                        data['rating'].append(ratings)
                        data['genre'].append(genre)
                        data['director'].append(dirs)
                        data['cast'].append(stars)
                        data['writer'].append(writer)
                        data['summary'].append(summary) 
                    except Exception as e:
                            print(traceback.format_exc())
    #  print(data['Moviename'],data['rating'],data['genre'],data['director'],data['cast'],data['writer'],data['summary'])
    df = pd.DataFrame(data)
    df.to_csv(str(t[1])+'_genre_imdb_scrapped.csv')
