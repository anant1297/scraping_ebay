# scraping_ebay
Scraping ebay.com to find what fraction of amazon gift cards sold above face value.

The code makes 10 requests to the eBay website for the search "amazon gift card" and saved the responses in 10 files named "amazon_gift_card_01.htm" to "amazon_gift_card_10.htm". Then it loads each saved HTML file into BeautifulSoup, and loops through each of the 10 BeautifulSoup objects, extracting information about the gift cards including the title, price, and shipping cost. Finally, it matches each line of the extracted information with a regular expression to check if the price of the gift card is higher than its face value and, if so, it prints the title, price, and shipping cost of the gift card.
