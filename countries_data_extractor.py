import requests
from bs4 import BeautifulSoup
from string import digits
import csv
url = "https://www.odoo.com/partners"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
partner_countries_list=soup.find_all("div", {"class": "dropdown-menu"})
countries_data=[]
for partner_countries in partner_countries_list:
    coutries=partner_countries.find_all("a", {"class": "dropdown-item"})
    for a in coutries:
        href=a['href']
        number_of_partners=0
        for badge in a.find_all('span', {"class": "badge"}):
            number_of_partners=badge.text
        country_name=a.text
        country_name=country_name.replace('\n','')
        remove_digits = str.maketrans('', '', digits)
        country_name = country_name.translate(remove_digits)
        country_name=country_name.strip()
        country_id=href.split('/')[-1]
        url_country_name=country_name.replace(' ','-').lower()
        url='https://www.odoo.com/partners/country/'+url_country_name+"-"+country_id
        countries_data.append((country_name,number_of_partners,href,url))
        print(countries_data)

with open("countries_data.csv", "w") as fp:
    writer = csv.writer(fp, delimiter=",")
    writer.writerow(["Country Name", "Number Of Partners", "href","URL"])
    for coutry_data in countries_data:
        writer.writerow(coutry_data)
        
