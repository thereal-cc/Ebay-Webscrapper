from bs4 import BeautifulSoup
import requests
import re

search_term = input("Enter what you'd like to search for: ")
url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={search_term}&_sacat=0"
print("")

page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

#listings = doc.find_all(class_="s-item s-item__pl-on-bottom s-item--watch-at-corner")
div = doc.find(class_="srp-results srp-list clearfix")
items = div.find_all(text=re.compile(search_term))

items_found = {}

for item in items:
    first_parent = item.parent
    parent = first_parent.parent

    if parent.name != "a":
        continue
    
    link = parent['href']

    next_parent = item.find_parent(class_="s-item s-item__pl-on-bottom s-item--watch-at-corner")
    try:
        original_price = next_parent.find(class_="s-item__price").string
        size = len(original_price)
        price = original_price[1:size-3]

        items_found[item] = {"price": int(price.replace("$", "").replace(",", "")), "link": link}
    except:
        pass
    
sorted_items = sorted(items_found.items(), key=lambda x: x[1]["price"])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("-----------------------------------------------------")
