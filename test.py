from bs4 import BeautifulSoup
import requests
from main import scrapproduit


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

scarpProduitParCategorie("https://books.toscrape.com/catalogue/category/books/travel_2/index.html",'Ss')