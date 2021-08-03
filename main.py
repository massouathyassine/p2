import requests
from bs4 import BeautifulSoup
import csv
from downloadImage import downloadImage


def scrapproduit(url,nomDeFichier):
   r = requests.get(url)
   html = r.text
   soup = BeautifulSoup(html, 'lxml')
   imgProduct = soup.find('div', {"class": "item active"})
   img = imgProduct.find('img')
   src = img.get('src')

   image_url = "https://books.toscrape.com/" + src
   titleProduct = soup.find('li', {"class": "active"}).get_text()
   descriptionProduct = soup.find('p',{"class": ""})
   if descriptionProduct:
      descriptionProduct = soup.find('p', {"class": ""}).get_text()
   else:
      descriptionProduct=""

   tableInfo = soup.find('table',{"class": "table table-striped"})
   rows=list()
   for row in tableInfo.findAll("tr"):
      rows.append(row)
   UPC = rows[0].find('td').get_text()
   price_including_tax=rows[3].find('td').get_text()
   price_excluding_tax=rows[2].find('td').get_text()
   number_available=rows[5].find('td').get_text()
   tableInfo1 = soup.find('ul',{"class": "breadcrumb"})
   aFind = tableInfo1.findAll('a')
   category = aFind[2].string
   with open(nomDeFichier+'.csv','a') as result:
   #result.write('product_page_url,upc,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url \n')
      result.write(url+','+UPC+','+titleProduct+','+price_including_tax+','+price_excluding_tax+','+number_available+','+descriptionProduct+','+category+','+'0'+','+image_url+'\n')
   downloadImage(image_url,titleProduct)
