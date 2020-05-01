#Connect mysql untuk insert data covid
import mysql.connector

mydb= mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="",
    database='testdb'
)
print(mydb)
mycursor = mydb.cursor()

#Import urllib
from urllib.request import urlopen
html = urlopen("https://www.kompas.com/covid-19").read()
print(type(html))
#print url html
print(html[1:100])

#import bs4
from bs4 import BeautifulSoup
soup = BeautifulSoup(html , "lxml")
print(type(soup))
print(soup.prettify()[1:100])

class_ = soup.find_all("div" , "covid__row")

#print data dalam tag class_
for p in class_:
    print(p.find("div" , "covid__prov").get_text())
    print(p.find("span" , "-odp").get_text())
    print(p.find("span" , "-gone").get_text())


#import pandas
import pandas as pd
covid_dict={}

for p in class_:

    provinsi = p.find("div" , "covid__prov").get_text()
    terkonfirmasi = p.find("span" , "-odp").get_text().replace(' ','').replace('Terkonfirmasi','').replace(':','')
    meninggal = p.find("span" , "-gone").get_text().replace(' ','').replace('Meninggal','').replace(':','')
    sembuh = p.find("span" , "-health").get_text().replace(' ','').replace('Sembuh','').replace(':','')
    
    #insert data covid ke sql
    sql = "INSERT INTO covid_data (provinsi , terkonfirmasi , meninggal , sembuh ) VALUES (%s, %s, %s, %s)"
    exec_ = [(provinsi,terkonfirmasi,meninggal,sembuh)]
    mycursor.executemany(sql, exec_)
    mydb.commit()
    
   
    
    






