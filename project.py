# Scraping amazon gift cards that sold above face value on ebay

# Import required libraries

from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import os
import re

# Downloading first ten pages from the target url

for i in range(1,11):
    url = "https://www.ebay.com/sch/i.html?_nkw=amazon+gift+card&LH_Sold=1&LH_Complete=1&_pgn="+str(i)
    user_agent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers = user_agent)
    with open(f"amazon_gift_card_{i:02}.htm", "w", encoding="utf-8") as file:
        file.write(response.text)
    time.sleep(10)

# Reading the downloaded pages

list_of_soups = []
for page in range(1,11):
    with open(f"amazon_gift_card_{page:02}.htm","r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, 'lxml')
        list_of_soups.append(soup)

# From each item in each page, extract gift card value, price and shipping cost

string = ""
page_count = 0
total_item_count = 0
print('Printing the title, price and shipping price for each amazon gift card in first 10 pages :\n')
for soup in list_of_soups:
    page_count += 1
    item_content = soup.select('#srp-river-results > ul > li > div > div.s-item__info.clearfix')
    for i in range(len(item_content)):
        index_str = str(i+1)+'->'
        
        title = item_content[i].select('a > div > span[role="heading"]')
        if title[0].find_all():
            t=[re.sub(any_tag.text,'',title[0].text) for any_tag in title[0].find_all()]
            title_str = t[0]
        else:
            title_str = title[0].text
        
        price = item_content[i].select('div.s-item__details.clearfix > div:nth-child(1) > span.s-item__price > span')
        price_str = price[len(price)-1].text
        
        shipping_list = item_content[i].select('div.s-item__details.clearfix > div > span.s-item__shipping.s-item__logisticsCost')
        shipping_str = 'NA' if not len(shipping_list) else shipping_list[0].text
        
        string = string + 'page_' + str(page_count) + ' item_' + index_str + ' TITLE: ' + title_str + ' PRICE: ' + price_str + ' SHIPPING: ' + shipping_str + '\n'
        total_item_count += 1
print(string)

# using regex to check if the gift card sold above face value

lines = string.split("\n")
count = 0
match_count = 0
print('Printing the title, price and shipping cost of gift cards which were sold above face value :\n')
for line in lines:
    match = re.search(".*? TITLE: .*?(\$.*?\d+|\d+\$|\d+ Dollars|\d+ USD|\d+ DOLLARS|CARD \d+|card \d+).*? PRICE: .*?\$([0-9]{1,3}.[0-9]{2}).*? SHIPPING: .*", line)
    if match:
        match_count += 1
        if "$" in match.group(1):
            value = int(match.group(1).replace("$", ""))
        elif " Dollars" in match.group(1):
            value = int(match.group(1).replace(" Dollars", ""))
        elif " USD" in match.group(1):
            value = int(match.group(1).replace(" USD", ""))
        elif " DOLLARS" in match.group(1):
            value = int(match.group(1).replace(" DOLLARS", ""))
        elif "CARD " in match.group(1):
            value = int(match.group(1).replace("CARD ", ""))
        elif "card " in match.group(1):
            value = int(match.group(1).replace("card ", ""))
            
        price = float(match.group(2))
        
        shipping_match = re.search(".*? SHIPPING: .*?\+\$([0-9]{1,2}.[0-9]{1,2}).*", line)
        if shipping_match:
            shipping = float(shipping_match.group(1))
        else:
            shipping = 0
        if value < price+shipping:
            print(line)
            count+= 1


# Print results

print('\nResults :\n')
print('success rate of extracting gift card value from title :', 100*match_count/total_item_count)
print('count of Amazon Gift Cards sold above face value :', count)
print('total items :', total_item_count)
print('\nFraction of Amazon gift cards sold above face value :', count/total_item_count)
print('\nPeople might buy gift cards above face value due to convenince, lack of alternatives or potentially for money laundering. ')
