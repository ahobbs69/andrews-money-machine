#!/usr/bin/env python3
"""
Home Depot Clearance Scraper
Finds 0.01 items and deal community posts
"""

import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

# Storage file
DEALS_FILE = os.path.expanduser("~/.openclaw/homedepot_deals.json")

def load_seen():
    if os.path.exists(DEALS_FILE):
        with open(DEALS_FILE) as f:
            return set(json.load(f))
    return set()

def save_seen(deals):
    with open(DEALS_FILE, 'w') as f:
        json.dump(list(deals), f)

def scrape_homedepot_clearance():
    """Scrape Home Depot deals page"""
    url = "https://www.homedepot.com/s/3/0-0-0-0-1/0-0-0-0-1?catStyle=Range&Ns=New&so=StartTime%20desc"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        items = []
        # Look for items in the product grid
        for product in soup.select('.product-card')[:20]:
            try:
                title = product.select_one('.product-title')
                price = product.select_one('.price')
                if title and price:
                    price_text = price.get_text().strip()
                    if '0.01' in price_text or '$0.01' in price_text.lower():
                        link = product.select_one('a')
                        items.append({
                            'title': title.get_text().strip(),
                            'price': price_text,
                            'link': 'https://www.homedepot.com' + link.get('href', '') if link else ''
                        })
            except:
                continue
        return items
    except Exception as e:
        print(f"Error scraping Home Depot: {e}")
        return []

def check_slickdeals():
    """Check Slickdeals for Home Depot deals"""
    url = "https://slickdeals.net/newsearch.php?forum[]=9&forum[]=10&forum[]=62&search=&sort=newsearch&searchfield=title"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        deals = []
        for deal in soup.select('.resultRow')[:10]:
            try:
                title = deal.select_one('.thread-title')
                if title and 'home depot' in title.get_text().lower():
                    link = deal.select_one('a')
                    deals.append({
                        'title': title.get_text().strip(),
                        'link': 'https://slickdeals.net' + link.get('href', '') if link else ''
                    })
            except:
                continue
        return deals
    except Exception as e:
        print(f"Error checking Slickdeals: {e}")
        return []

def check_deals():
    """Main check function"""
    print(f"\n🔍 Checking deals at {datetime.now().strftime('%I:%M %p')}...")
    
    seen = load_seen()
    new_deals = []
    
    # Check Home Depot
    hd_deals = scrape_homedepot_clearance()
    for deal in hd_deals:
        key = f"hd:{deal['title']}"
        if key not in seen:
            seen.add(key)
            new_deals.append(f"🏠 Home Depot: {deal['title']} - {deal['price']}")
            if deal.get('link'):
                new_deals.append(f"   🔗 {deal['link']}")
    
    # Check Slickdeals
    sd_deals = check_slickdeals()
    for deal in sd_deals:
        key = f"sd:{deal['title']}"
        if key not in seen:
            seen.add(key)
            new_deals.append(f"💰 Slickdeals: {deal['title']}")
            if deal.get('link'):
                new_deals.append(f"   🔗 {deal['link']}")
    
    # Save updated seen deals
    save_seen(seen)
    
    if new_deals:
        print(f"✅ Found {len(new_deals)} new deals!")
        return new_deals
    else:
        print("❌ No new deals found")
        return []

if __name__ == "__main__":
    check_deals()
