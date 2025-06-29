import requests
from bs4 import BeautifulSoup
import pandas as pd    
import time 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
} 

BASE_URL = "https://shop.wwe.com/collections/best-sellers" 
def scrape_wwe_products(page_url):
    response = requests.get(page_url, header=HEADERS)
    if response.status_code != 200:
        print("Failed to retrieve page:", response.status_code)
        return[]

    soup = BeautifulSoup(response.content, "html.parser")
    product_cards = soup.find_all("div", class_="product-title")

    product_data = []

    for product in product_cards:
        try:
            title = product.find("p", class_="product-title").text.strip()
            price = product.find("span", class_="product-sales-price").text.strip()
            url = product.find("a", class_="thumb-link")["href"]
            full_url = f"https://shop.wwe.com{url}" 

            product_data.append ({ 
                "Product Name": title,
                "Price": price,
                "URL": full_url,
            })
        except Exception as e:
            print("Error parsing product:", e)
            continue

    return product_data 

df = pd.DataFrame(products)
df.to_csv("wwe_merchandise_data.csv", index=False)

print(f"Scraped {len(df)} products and saved to wwe_merchandise_data.csv") 
