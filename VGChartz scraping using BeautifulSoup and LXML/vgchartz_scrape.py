#import necessary packages
from bs4 import BeautifulSoup
from lxml import etree
from requests.exceptions import ChunkedEncodingError
from tqdm import tqdm
import math
import pandas as pd
import requests
import time

per_page=200  #since we get 200 results per page

#url formatting
urL_before_page='https://www.vgchartz.com/games/games.php?page='
url_after_page='name=&keyword=&console=&region=All&developer=&publisher=&goty_year=&genre=&boxart=Both&banner=Both&ownership=Both&showmultiplat=Yes&results='+str(per_page)+'&order=Sales&showtotalsales=0&showtotalsales=1&showpublisher=0&showpublisher=1&showvgchartzscore=0&showvgchartzscore=1&shownasales=0&shownasales=1&showdeveloper=0&showdeveloper=1&showcriticscore=0&showcriticscore=1&showpalsales=0&showpalsales=1&showreleasedate=0&showreleasedate=1&showuserscore=0&showuserscore=1&showjapansales=0&showjapansales=1&showlastupdate=0&showlastupdate=1&showothersales=0&showothersales=1&showshipped=0&showshipped=1'

#to get the page numbers
initial_response=requests.get('https://www.vgchartz.com/gamedb/')
initial_soup=BeautifulSoup(initial_response.text, 'html.parser')
initial_tree=etree.HTML(str(initial_soup))
total_number=initial_tree.xpath('//*[(@id = "generalBody")]//tr[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]//th[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]')[0].text
total_number=int(total_number.split(':')[1].strip().replace("(", "").replace(")", "").replace(",", ""))  #to replace the ( , )
total_pages=math.ceil(total_number/per_page) #math.ceil to round to next integer

#total_number is the number of rows desirable data
#total_pages is the number of pages we have to crawl through

#creating a dataframe to store all the data
big_df=pd.DataFrame()

#crawling loop
for page in tqdm(range(0,total_pages), desc="Processing pages"):
	time.sleep(0.5)	#to avoid triggering the DDoS-prevention measures
	page+=1			#adding 1 to page number to start from 'page 1'

	#concating to get the full url
	full_url=urL_before_page+str(page)+url_after_page
	
	#error handling
	retries=0
	while retries<3: 
		try:
			response=requests.get(full_url)
			response.raise_for_status()  #bad response
			break
		except (requests.RequestException, ChunkedEncodingError) as e:
			retries+=1
			if retries==3:
				print(f'\nMaximum retries reached. Failed to retrieve data for the page number: {page}.')
			else:
				print(f'\nRetrying. Attempt no: {retries}')

	soup=BeautifulSoup(response.text,'html.parser')
	tr_all=soup.find_all('tr')
	body=[]
	for tr in tr_all:
		body.extend(tr.find_all('td'))
	df=pd.concat(pd.read_html(str(body)))
	index_number=((per_page*(page!=total_pages))+((total_number-((page-1)*per_page
			))*(page==total_pages)))+127  			#127 (23+104) is the total number of unwanted rows that gets crawled

	#setting index
	df.index=range(index_number)
	df.columns=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO']

	#replacing the substring ' Read the review' seen randomly in the column 'I'
	df['I'] = df['I'].str.replace(' Read the review', '')

	#dropping unwanted rows
	df.drop(index=range(0,23),inplace=True) 							#23 is the number of unwanted rows at the top
	df.drop(index=range(index_number-104,index_number),inplace=True)	#104 is the number of unwanted rows at the bottom

	#dropping unwanted columns
	df.drop(['A','B','C','D','E','F','G','H','J','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO'],axis=1,inplace=True)

	#concatinating to the primary dataframe
	big_df=pd.concat([big_df, df], ignore_index=False, sort=False)

#setting index
big_df.index=range(1,len(big_df.index)+1)
big_df.index.name='Rank Based on Total Shipped'

#setting column names
big_df.columns=['Game Name','Publisher','Developer','VGChartz Score','Critic Score','User Score','Total Shipped','Total Sales','NA Sales','PAL Sales','Japan Sales','Other Sales','Release Date','Last Update']

#saving the dataframe to a csv file
big_df.to_csv('./vgchartz_scrape_output.csv')
print(f'Saved {len(big_df.index)} rows.')