import csv
import sys
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

def scrape_md_computers(search_term):
    base_url = "https://mdcomputers.in/index.php?route=product/search"
    search_url = f"{base_url}&search={quote_plus(search_term)}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    print(f"Fetching results for: '{search_term}'...")
    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to MDComputers: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', class_='product-layout')
    
    if not products:
        print("No products found or the page structure has changed.")
        return

    extracted_data = []
    
    for product in products:
        title_tag = product.find('h4')
        if title_tag and title_tag.find('a'):
            title = title_tag.find('a').get_text(strip=True)
            link = title_tag.find('a')['href']
        else:
            continue
            
        price_tag = product.find('p', class_='price')
        price = "N/A"
        if price_tag:
            new_price = price_tag.find('span', class_='price-new')
            if new_price:
                price = new_price.get_text(strip=True)
            else:
                price = price_tag.get_text(strip=True).split('\n')[0]

        extracted_data.append({
            "Title": title,
            "Price": price,
            "Link": link
        })

    filename = f"md_results_{search_term.replace(' ', '_')}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Price", "Link"])
        writer.writeheader()
        writer.writerows(extracted_data)
        
    print(f"Successfully scraped {len(extracted_data)} items. Saved to {filename}")

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "external harddrive"
    scrape_md_computers(query)
