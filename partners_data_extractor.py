import csv
import requests
from bs4 import BeautifulSoup
import time


url_list=[]
print("#########reading partners URLs from CSV##############")
with open('partners_urls.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for i, row in enumerate(csv_reader):

        if i>0: ##skipping heading and "all countries" row
            url_list.append(row)

item_props_to_read=['website','email','telephone','streetAddress']
partners_data=[]

print("#########Scrapping Partners Data From URLs##############")
for url,country_name in url_list:
    response_success=False
    while(not response_success):
        try:
            print(url)
            response_success=True
            response = requests.get(url)
        except:
            print("Error in request. Trying again in 2 seconds")
            time.sleep(2)
            response_success=False

        
    soup = BeautifulSoup(response.content, "html.parser")
    titles=soup.find_all("h1", {"id": "partner_name"})
    partner_data=[]
    name=""
    for title in titles:
        name=title.text
        break

    partner_data.append(name)
    for prop in item_props_to_read:
        spans=soup.find_all("span", {"itemprop": prop})
        value=""
        for span in spans:
            value=span.text.split(',')
            value=' '.join(value)
        partner_data.append(value)
    partner_data.append(country_name)
    partner_data.append(url)

    partners_data.append(partner_data)
    print(partner_data)


print("#########Writing partners data to CSV file##############")
with open("partners_data.csv", "w") as fp:
    writer = csv.writer(fp, delimiter=",")
    writer.writerow(["Name","Website","Email","Telephone","Street Address","Country Name","Odoo URL"])
    # writer.writerow(["your", "header", "foo"])  # write header
    for partner_data in partners_data:
        writer.writerow(partner_data)
        