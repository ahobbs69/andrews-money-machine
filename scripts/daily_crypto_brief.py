#!/usr/bin/env python3
"""
Andrew's Daily Crypto Brief - Automated Morning Report
Generates a daily crypto market report with key metrics and opportunities
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
import os

# Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_prices(coin_ids):
    url = f"{COINGECKO_API}/simple/price"
    params = {
        'ids': ','.join(coin_ids),
        'vs_currencies': 'usd',
        'include_24hr_change': 'true',
        'include_24hr_vol': 'true',
        'include_market_cap': 'true'
    }
    
    try:
        with urllib.request.urlopen(f"{url}?{'&'.join([f'{k}={v}' for k,v in params.items()])}", timeout=10) as response:
            return json.loads(response.read().decode())
    except:
        return {}

def get_top_coins():
    url = f"{COINGECKO_API}/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode())
    except:
        return []

def generate_report():
    coins = get_top_coins()
    watchlist = ['bitcoin', 'ethereum', 'solana', 'cardano', 'polkadot', 'chainlink', 'avalanche-2']
    prices = get_prices(watchlist)
    
    report = f"📊 *DAILY CRYPTO BRIEF* - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    report += "🔥 *TOP 10 BY MARKET CAP*\n"
    for i, c in enumerate(coins, 1):
        arrow = "🟢" if c['price_change_percentage_24h'] > 0 else "🔴"
        report += f"{i}. {c['symbol'].upper()} ${c['current_price']:,.2f} {arrow} {c['price_change_percentage_24h']:+.2f}%\n"
    
    report += "\n🎯 *WATCHLIST*\n"
    for coin_id, data in prices.items():
        arrow = "🟢" if data.get('usd_24h_change', 0) > 0 else "🔴"
        report += f"• {coin_id}: ${data['usd']:,.2f} {arrow} {data.get('usd_24h_change', 0):+.2f}%\n"
    
    # Simple signals
    report += "\n📈 *QUICK SIGNALS*\n"
    opportunities = []
    for coin_id, data in prices.items():
        change = data.get('usd_24h_change', 0)
        if change > 5:
            opportunities.append(f"🟢 {coin_id}: +{change:.1f}% (potential breakout)")
        elif change < -5:
            opportunities.append(f"🔴 {coin_id}: {change:.1f}% (dip opportunity?)")
    
    if opportunities:
        report += "\n".join(opportunities)
    else:
        report += "No major signals today - market is calm"
    
    return report

def send_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram not configured. Showing report:")
        print(message)
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"Failed to send Telegram: {e}")
        return False

if __name__ == "__main__":
    report = generate_report()
    send_telegram(report)
    print("Report generated!")
