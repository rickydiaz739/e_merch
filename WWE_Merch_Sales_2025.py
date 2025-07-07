import requests
import pandas as pd
import json
import time 

def get_wwe_shop_products_json(page=1): 
    url = f"https://shop.wwe.com/collections/all-products.json?page={page}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    return response.json()

data = response.json()
products = data.get('products', [])

result = []

for product in products: 
    variant = product.get("variants", [{}])[0]

    result.append({
        "Title": product.get("title"),
        "Type": product.get("product_type"),
        "Vendor": product.get("vendor"),
        "Tags": ",".join(product.get("tags", [])),
        "Created Act": product.get("created_at"),
        "SKU": variant.get("sku"),
        "Available": variant.get("available"),
        "Price": float(variant.get("price")) / 100, # Convert cents to dollars
        "Compare at Price": float(variant.get("compare_at_price") or 0) / 100, # Convert cents to dollars
        "product URL": f"https://shop.wwe.com/products/{product.get('handle')}",
        "Image URL": product.get("featured_image", {}).get("src"),
    })

    return result

all_products = []
for pages in range(1,6):
    print(f"Scraping page {pages}...")
    all_products.extend(get_wwe_shop_products_json(pages))
    time.sleep(1)  # Be polite and wait a second between requests

df = pd.DataFrame(all_products)
df.to_csv("wwe_shop_products.csv", index=False)
print(f"\nSaved {len(df)} products to wwe_shop_products.csv")