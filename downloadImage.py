import requests


def downloadImage(urlImage,NomProduit):

    image_url = urlImage
    path = NomProduit+".jpg"
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
