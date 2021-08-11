from fonction import scarpProduitParCategorie
import requests
from bs4 import BeautifulSoup

url1="https://books.toscrape.com/"
r1 = requests.get(url1)
html1 = r1.text
soup1 = BeautifulSoup(html1, 'lxml')
linkCat = soup1.find('ul', {"class": "nav nav-list"}).findAll('a')
for j in linkCat:
    if j.get('href') != "catalogue/category/books_1/index.html":
        print(url1+j.get('href'))
        scarpProduitParCategorie(url1+j.get('href'),j.text.strip())
