#importing necessary packages
import requests
import re
import time
from tqdm import tqdm
from lxml import etree
import math
import pandas as pd
from bs4 import BeautifulSoup

#creating a list 'data_list' for adding the scraped data
data_list=[]

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,kn;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
}

#get page number
params = {
	'sid': '6bo,b5g',
	'sort': 'popularity',
	'page': str(1)
}
response = requests.get('https://www.flipkart.com/laptops/pr', params=params, headers=headers)
soup=BeautifulSoup(response.text,'html.parser')
page_box=soup.find_all("span",{"class":"_2tDckM"})
initial_tree=etree.HTML(str(page_box))
initial_tree=initial_tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_2tDckM", " " ))]')[0].text
per_page=int(initial_tree.split(' ')[3].strip().replace("(", "").replace(")", "").replace(",", ""))
total_number=int(initial_tree.split(' ')[6].strip().replace("(", "").replace(")", "").replace(",", ""))
total_pages=math.ceil(total_number/per_page)
#to loop through the first 10 pages
rank=0
for i in tqdm(range(0,total_pages), desc="Processing pages"):
	params = {
		'sid': '6bo,b5g',
    	'sort': 'popularity',
		'page': str(i+1)
	}
	#to avoid triggering the DDoS-prevention measures
	time.sleep(1)
	response = requests.get('https://www.flipkart.com/laptops/pr', params=params, headers=headers)
	soup=BeautifulSoup(response.text,'html.parser')
	main_box=soup.find_all("a",{"class":"_1fQZEK"})
	# if we don't get any information
	if len(main_box) == 0:
		print(f'\nData stops after {i} pages...you can check at: https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g&sort=popularity&page={i+1}')
		break
	else:
		for box in main_box:
			#creating a temporary dictionary 'temp_dict'
			temp_dict={}
			rank+=1
			temp_dict['RANK']=rank
			temp_dict['TITLE']=box.find("div",{"class":"_4rR01T"}).text.strip()
			temp_dict['BRAND NAME']=box.find("div",{"class":"_4rR01T"}).text.strip().split(" ", 1)[0].title()
			try:
				discount_price=box.find("div",{"class":"_30jeq3 _1_WHN1"}).text.replace('₹','').strip()
				discount_price=discount_price.replace(',', '')
				temp_dict['DISCOUNT PRICE']=discount_price	
			except AttributeError as e:
				temp_dict['DISCOUNT PRICE']=None
			try:    
				true_price=box.find("div",{"class":"_3I9_wc _27UcVY"}).text.replace('₹','').strip()
				true_price=true_price.replace(',', '')
				temp_dict['TRUE PRICE']=true_price
			except AttributeError as e:
				temp_dict['TRUE PRICE']=None
			try:
				discount_percentage=box.find("div",{"class":"_3Ay6Sb"}).text.replace('% off','').strip()
				temp_dict['DISCOUNT PERCENTAGE']=discount_percentage
			except AttributeError as e:
				temp_dict['DISCOUNT PERCENTAGE']=None
			try:
				temp_dict['RATING']=box.find("div",{"class":"_3LWZlK"}).text.strip()
			except AttributeError as e:
				temp_dict['RATING']=None
			try:
				ul_tag=box.find('ul', class_='_1xgFaf')
				details=[li_tag.text for li_tag in ul_tag.find_all('li', class_='rgWa7D')]
				temp_dict['DETAILS'] = details[0] + '\n' + '\n'.join(details[1:])
			except AttributeError as e:
				temp_dict['DETAILS']=None		
			try:
				rating_number=box.select_one('._2_R_DZ > span > span:first-child').text
				rating_number=rating_number.replace(',', '')
				rating_count=re.search(r'\d+', rating_number).group()
				temp_dict['RATING COUNT']=rating_count
			except AttributeError as e:
				temp_dict['RATING COUNT']=None		
			try:
				review_number=box.select_one('._2_R_DZ > span > span:nth-child(3)').text
				review_number=review_number.replace(',', '')
				review_count=re.search(r'\d+', review_number).group()
				temp_dict['REVIEW COUNT']=review_count
			except AttributeError as e:
				temp_dict['REVIEW COUNT']=None
			url=box.get('href')
			url=url.split('?')[0]
			temp_dict['URL']=str('https://www.flipkart.com')+str(url)
			data_list.append(temp_dict)

#create a new dataframe 'flipkart_df' to store the list
flipkart_df=pd.DataFrame(data_list)

#saving the dataframe to a csv file
flipkart_df.to_csv('flipkart_scraping_output.csv',index=False)