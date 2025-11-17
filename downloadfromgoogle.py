import requests
from bs4 import BeautifulSoup
import re

def download_first_google_image(query):
    url = "https://www.google.com/search?q=" + query.replace(" ", "+") + "&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    # Find the first image source from the script tag
    match = re.search(r'"ou":"(.*?)"', html)
    if not match:
        print("No image found or Google blocked the request.")
        return
    
    img_url = match.group(1)
    print("Image URL:", img_url)

    img_data = requests.get(img_url, headers=headers).content

    with open("image.jpg", "wb") as f:
        f.write(img_data)

    print("Downloaded: image.jpg")

download_first_google_image("beautiful mountains")