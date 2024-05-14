import csv
import requests
from bs4 import BeautifulSoup
import time
countries_data=[]


print("#########reading Countries Data from CSV##############")
with open('countries_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for i, row in enumerate(csv_reader):
        if i>1: ##skipping heading and "all countries" row
            countries_data.append(row)

url_list=[]
urls_only=[]
print("#########Scrapping Partners URLs For Countries##############")
for country_data in countries_data:
    print(country_data[0])
    # if int(country_data[1])<103:
    #     continue
    duplication_detected=False
    url = country_data[3]
    for page in (1,2,3,4,5):
        if page!=1:
            page_url=url+"/page/"+str(page)
        else:
            page_url=url
        response_success=False
        while(not response_success):
            try:
                print(page_url)
                response_success=True
                response = requests.get(page_url)
            except:
                print("Error in request. Trying again in 2 seconds")
                time.sleep(2)
                response_success=False

        soup = BeautifulSoup(response.content, "html.parser")
        partners_list=soup.find_all("div", {"class": "card"})
        
        for partner in partners_list:
            a_tags=partner.find_all("a",{"class":"text-decoration-none"})
            partner_url=""
            for a in a_tags:
                partner_url=a['href']
                break
                

            partner_complete_url="https://www.odoo.com"+partner_url
            if partner_complete_url in urls_only:

                duplication_detected=True
                break
            url_list.append((partner_complete_url,country_data[0]))
            urls_only.append(partner_complete_url)

        if duplication_detected:
            break
print("#########Writing partners urls to CSV file##############")
with open("partners_urls.csv", "w") as fp:
    writer = csv.writer(fp, delimiter=",")
    writer.writerow(["Odoo URL","Country Name"])
    # writer.writerow(["your", "header", "foo"])  # write header
    for partner_data in url_list:
        writer.writerow(partner_data)
        
