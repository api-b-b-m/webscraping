#importing necessary packages
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

#creating a list 'data' for adding the scraped data
data_list=[]

#for loop to repeat for the first 10 pages
for i in range (1,10):
    params = {
        'sid': '6bo,b5g',
        'page': str(i),
    }
    #to avoid triggering the ddos-prevention measures
    time.sleep(1)
    response = requests.get('https://www.flipkart.com/laptops/pr', params=params)
    soup=BeautifulSoup(response.text,'html.parser')
    main_box=soup.find_all("a",{"class":"_1fQZEK"})
    # if we don't get any information
    if len(main_box) == 0:
        print(f'Stopped crawling after {i-1} pages')
        break
    
    else:
        print(f'Getting page: {i}')
        for box in main_box:
            #creating a temporary dictionary
            temp_dict={}
            title=box.find("div",{"class":"_4rR01T"}).text.strip()
            temp_dict['TITLE']=title
            temp_dict['DISCOUNT PRICE']=box.find("div",{"class":"_30jeq3 _1_WHN1"}).text.replace('₹','').strip()
            temp_dict['TRUE PRICE']=box.find("div",{"class":"_3I9_wc _27UcVY"}).text.replace('₹','').strip()
            temp_dict['DISCOUNT PERCENTAGE']=box.find("div",{"class":"_3Ay6Sb"}).text.replace(' off','').strip()
            if (box.find("div",{"class":"_3LWZlK"})) is not None:
                temp_dict['RATING']=box.find("div",{"class":"_3LWZlK"}).text.strip()
            else:
                temp_dict['RATING']=None
            data_list.append(temp_dict)

#to save the list into a new dataframe
df=pd.DataFrame(data_list)

#saving the dataframe to a csv file
df.to_csv('flipkart_scraping.csv',index=False)