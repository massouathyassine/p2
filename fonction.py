import os
import requests
from bs4 import BeautifulSoup


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
   if not os.path.isdir('csv'):
        os.mkdir('csv')
   with open('csv/'+nomDeFichier+'.csv','a') as result:
   #result.write('product_page_url,upc,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url \n')
      result.write(url+','+UPC+','+titleProduct+','+price_including_tax+','+price_excluding_tax+','+number_available+','+descriptionProduct+','+category+','+'0'+','+image_url+'\n')
   downloadImage(image_url,titleProduct,nomDeFichier)

def downloadImage(urlImage,NomProduit,catgorie):

    image_url = urlImage
    if not os.path.isdir(catgorie+'Images'):
        os.mkdir(catgorie+'Images')
    path = catgorie+'Images'+'/'+NomProduit+".jpg"
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

def scarpProduitParCategorie(urlCat,NomDeCSV):
    r = requests.get(urlCat)
    html = r.text
    soup = BeautifulSoup(html)
    NbrDelivre = soup.find('form', {"class": "form-horizontal"}).find('strong').get_text()
    nomfichier = NomDeCSV

    if int(NbrDelivre) <= 20:
        linkProduit = soup.find_all('div', {"class": "image_container"})
        for i in linkProduit:
            linkp = i.find('a').get('href')
            linkp1 = "https://books.toscrape.com/catalogue/" + linkp[9:len(linkp)]
            scrapproduit(linkp1,nomfichier)
    else:
        codePage = soup.find_all('li', {"class": "current"})
        textNbredePage = codePage[0].get_text()
        nombreDepage = int(textNbredePage.lstrip()[10:11])
        for j in range(1, nombreDepage + 1):
            j1 = str(j)
            url2 = urlCat + "page-" + j1 + ".html"
            r1 = requests.get(url2)
            html1 = r1.text
            soup2 = BeautifulSoup(html1)
            linkProduit2 = soup2.find_all('div', {"class": "image_container"})
            for i1 in linkProduit2:
                link = i1.find('a').get('href')
                linkProduitdePlusieurPage = "https://books.toscrape.com/catalogue/" + link[9:len(link)]
                scrapproduit(linkProduitdePlusieurPage,nomfichier)