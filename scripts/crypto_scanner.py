#!/usr/bin/env python3
"""
Crypto Market Scanner - Scans for arbitrage opportunities across exchanges
Created by Clyde for Andrew's trading operations
"""

import json
import urllib.request
import urllib.error
from datetime import datetime

# CoinGecko API (free, no key needed)
COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_coin_prices(coin_ids):
    """Fetch prices from CoinGecko"""
    url = f"{COINGECKO_API}/simple/price"
    params = {
        'ids': ','.join(coin_ids),
        'vs_currencies': 'usd',
        'include_24hr_change': 'true'
    }
    
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    
    try:
        with urllib.request.urlopen(f"{url}?{query_string}", timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return {}

def calculate_arbitrage_opportunity(price_data):
    """Analyze price data for potential opportunities"""
    opportunities = []
    
    # Check 24h change patterns
    for coin, data in price_data.items():
        change = data.get('usd_24h_change', 0)
        
        # Look for significant moves that might indicate opportunities
        if abs(change) > 5:
            opportunities.append({
                'coin': coin,
                'price': data.get('usd', 0),
                'change_24h': change,
                'signal': 'HIGH VOLATILITY' if abs(change) > 10 else 'MODERATE'
            })
    
    return opportunities

def get_top_coins():
    """Get top cryptocurrencies by market cap"""
    url = f"{COINGECKO_API}/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': '20',
        'page': '1',
        'sparkline': 'false'
    }
    
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    
    try:
        with urllib.request.urlopen(f"{url}?{query_string}", timeout=10) as response:
            data = json.loads(response.read().decode())
            return [{
                'name': c['name'],
                'symbol': c['symbol'].upper(),
                'price': c['current_price'],
                'change_24h': c['price_change_percentage_24h'],
                'market_cap': c['market_cap']
            } for c in data[:10]]
    except Exception as e:
        print(f"Error fetching top coins: {e}")
        return []

def scan_for_opportunities():
    """Main scanning function"""
    print("=" * 60)
    print(f"🚀 CRYPTO MARKET SCANNER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Get top coins
    print("\n📊 TOP 10 CRYPTOS BY MARKET CAP:")
    print("-" * 60)
    
    top_coins = get_top_coins()
    for i, coin in enumerate(top_coins, 1):
        change_emoji = "🟢" if coin['change_24h'] > 0 else "🔴"
        print(f"{i:2}. {coin['symbol']:8} ${coin['price']:>10.2f}  {change_emoji} {coin['change_24h']:+.2f}%")
    
    # Key coins to watch
    watchlist = ['bitcoin', 'ethereum', 'solana', 'cardano', 'polkadot', 'avalanche-2', 'chainlink']
    
    print("\n🎯 WATCHLIST PRICES:")
    print("-" * 60)
    
    prices = get_coin_prices(watchlist)
    for coin_id, data in prices.items():
        change = data.get('usd_24h_change', 0)
        change_emoji = "🟢" if change > 0 else "🔴"
        print(f"{coin_id:20} ${data['usd']:>10.2f}  {change_emoji} {change:+.2f}%")
    
    # Find opportunities
    print("\n💡 POTENTIAL OPPORTUNITIES:")
    print("-" * 60)
    
    opportunities = calculate_arbitrage_opportunity(prices)
    
    if opportunities:
        # Sort by absolute change
        opportunities.sort(key=lambda x: abs(x['change_24h']), reverse=True)
        
        for opp in opportunities[:5]:
            print(f"  {opp['coin']:20} {opp['signal']:15} {opp['change_24h']:+.2f}%")
    else:
        print("  No major opportunities detected (market may be calm)")
    
    print("\n" + "=" * 60)
    print("📈 Market scan complete!")
    print("=" * 60)
    
    return top_coins, prices

if __name__ == "__main__":
    scan_for_opportunities()
