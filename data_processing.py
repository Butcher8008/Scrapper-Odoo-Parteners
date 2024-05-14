import csv
data=[]

with open('partners_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for i, row in enumerate(csv_reader):

        if i>0: ##skipping heading and "all countries" row
            data.append(row)

with open("processed_partners_data.csv", "w") as fp:
    writer = csv.writer(fp, delimiter=",")
    writer.writerow(["Name","Website","Email","Telephone","Street Address","Country Name","Odoo URL"])
    # writer.writerow(["your", "header", "foo"])  # write header
    for partner_data in data:
        name, website, email_column, telephone, street, country, odoo_url = partner_data
        emails=[]
        for email in email_column.split(';'):
            for splited_email in email.split(' '):
                for i in splited_email.split('\t'):
                    for j in i.split("/"):
                        if j !="":
                            emails.append(j)
        if not emails:
            writer.writerow([name, website, "", telephone, street, country, odoo_url])
            continue
        
        for email in emails:

            writer.writerow([name, website, email, telephone, street, country, odoo_url])


