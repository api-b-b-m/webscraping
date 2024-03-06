#importing necessary packages
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

#creating a list 'data_list' for adding the scraped data
data_list=[]

#to loop through the first 10 pages
for i in range (0,10):
	params = {
		'sid': '6bo,b5g',
		'page': str(i+1),
	}
	time.sleep(1) #to avoid triggering the DDoS-prevention measures
	response = requests.get('https://www.flipkart.com/laptops/pr', params=params)
	soup=BeautifulSoup(response.text,'html.parser')
	main_box=soup.find_all("a",{"class":"_1fQZEK"})

	# if we don't get any information
	if len(main_box) == 0:
		print(f'Stopped crawling after {i} pages')
		break
	
	else:
		print(f'Getting page: {i+1}')
		for box in main_box:
			#creating a temporary dictionary 'temp_dict'
			temp_dict={}

			temp_dict['TITLE']=box.find("div",{"class":"_4rR01T"}).text.strip()
			temp_dict['BRAND NAME']=box.find("div",{"class":"_4rR01T"}).text.strip().split(" ", 1)[0].title()
			try:
				temp_dict['DISCOUNT PRICE']=box.find("div",{"class":"_30jeq3 _1_WHN1"}).text.replace('₹','').strip()
			except AttributeError as e:
				temp_dict['DISCOUNT PRICE']='Not Available'
			try:    
				temp_dict['TRUE PRICE']=box.find("div",{"class":"_3I9_wc _27UcVY"}).text.replace('₹','').strip()
			except AttributeError as e:
				temp_dict['TRUE PRICE']='Not Available'
			try:
				temp_dict['DISCOUNT PERCENTAGE']=box.find("div",{"class":"_3Ay6Sb"}).text.replace(' off','').strip()
			except AttributeError as e:
				temp_dict['DISCOUNT PERCENTAGE']='Not Available'
			try:
				temp_dict['RATING']=box.find("div",{"class":"_3LWZlK"}).text.strip()
			except AttributeError as e:
				temp_dict['RATING']='Not Available'

			data_list.append(temp_dict)

#create a new dataframe 'flipkart_df' to store the list
flipkart_df=pd.DataFrame(data_list)

#saving the dataframe to a csv file
flipkart_df.to_csv('flipkart_scraping_output.csv',index=False)