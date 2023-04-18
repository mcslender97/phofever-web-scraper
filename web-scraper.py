# Webscraper for building pho stores list from Phofever.com
import time
import csv
import requests
import bs4



with open('Pho_fever.tsv','w',encoding="utf-8") as file:
    writer = csv.writer(file,delimiter='\t')

    for row in range(1,5000):
        res = requests.get(f"http://www.phofever.com/restaurants.php?rid={str(row).zfill(4)}",allow_redirects=False)
        #loop through potential store ids, stored in 4 digits from 0001
        #ignore redirects since website will redirect to home page if no such store has that id
        if res.status_code!=200: 
            continue    
        soup = bs4.BeautifulSoup(res.text,"html.parser")

        business_name=soup.h1.getText() # extract store name
        print(business_name)
        listing=soup.find("div",{"id":"listing"}).getText("\n") # get store information in listing div
        info=listing.strip().split("\n")
        print(f"row: {row}")
        print(info)
        
        if len(info)>3: # info: store name, address (street, city, state), phone number, website
            writer.writerow([business_name,info[0]+","+info[1],info[2],info[3]])
        elif len(info)==3: # info: store name, address (street, city, state), phone number
            writer.writerow([business_name,info[0]+","+info[1],info[2],'N/A'])
        else: # info: store name, address (city, state)
            writer.writerow([business_name,info[0],info[1],'N/A'])
        
        time.sleep(2.5) # space out requests so not to trigger DDOS protection
