import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

data = {}

with open('data.txt') as json_file:
    data = json.load(json_file)

linkFile = open('links.txt', 'r') 
Links = linkFile.readlines()

# Strips the newline character 
for link in Links:
    link = link.strip()
    print("\n")
    print("Verarbeite {}".format(link))
        
    result = requests.get(link)

    # print(result.headers)
    if result.status_code != 200:
        print("Bei {} ist ein Fehler aufgetreten".format(link))
        continue

    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    docDivs = soup.find_all("div", {"class": "productDetail"})

    if len(docDivs) != 1:
        print("Konnte Page nicht parsen")
        continue

    item = docDivs[0]

    res1 = re.search(r"(\d{1,}(\.\d{0,}){0,1})\.\–", str(item))

    price = 0

    if not res1:
        res2 = re.search(r"(\d{1,}(\.\d{0,}){0,1})<\/strong>", str(item))
        price = res2.group(1)
    else: 
        price = res1.group(1)

    name = soup.find("span", {"class": "productHeaderTitle__Name-gtvrqo-1"}).getText()
    manufacturer = soup.find("h1", {"class": "productHeaderTitle__Title-gtvrqo-0"}).find('strong').text


    print("Name: {}".format(name))
    print("Manufacturer: {}".format(manufacturer))
    print("Price: {}".format(price))

    if link not in data:
        data[link] = {
            "name": "None",
            "manufacturer": "None",
            "prices": []
        }
    
    data[link]['name'] = name
    data[link]['manufacturer'] = manufacturer

    data[link]['prices'].append({
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'price': price
    })
    
    # print("Preis: {}".format(m.group(2)))
    # print("===")
    # print(item)
    # print("===")
print("\n")

for i in data:
    for y in data[i]['prices']:
        if(datetime.strptime(y['date'], '%Y-%m-%d %H:%M') < (datetime.now() - timedelta(days=5))):
            print("DELETE {}".format(y))
            data[i]['prices'].remove(y)
        # else:
        #     print("OK {}".format(y))
        
    

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)