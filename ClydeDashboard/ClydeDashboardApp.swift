//
//  ClydeDashboardApp.swift
//  ClydeDashboard
//
//  Simple working version
//

import SwiftUI

@main
struct ClydeDashboardApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    var body: some View {
        TabView {
            DashboardTab()
                .tabItem { Label("Home", systemImage: "house") }
            
            GainiumTab()
                .tabItem { Label("Gainium", systemImage: "chart.line.uptrend.xyaxis") }
            
            BotsTab()
                .tabItem { Label("Bots", systemImage: "brain") }
            
            SettingsTab()
                .tabItem { Label("Settings", systemImage: "gear") }
        }
    }
}

struct DashboardTab: View {
    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                VStack {
                    Text("Total P&L")
                        .font(.title3)
                        .foregroundColor(.secondary)
                    Text("+$601.28")
                        .font(.system(size: 50, weight: .bold))
                        .foregroundColor(.green)
                }
                .padding(30)
                .background(Color.gray.opacity(0.1))
                .cornerRadius(20)
                
                HStack(spacing: 20) {
                    VStack {
                        Image(systemName: "brain")
                            .font(.largeTitle)
                        Text("3")
                            .font(.title)
                        Text("Bots")
                            .font(.caption)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(20)
                    .background(Color.blue.opacity(0.1))
                    .cornerRadius(15)
                    
                    VStack {
                        Image(systemName: "banknote")
                            .font(.largeTitle)
                        Text("59%")
                            .font(.title)
                        Text("Used")
                            .font(.caption)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(20)
                    .background(Color.orange.opacity(0.1))
                    .cornerRadius(15)
                }
                
                VStack(alignment: .leading, spacing: 10) {
                    Text("Market")
                        .font(.title2)
                        .fontWeight(.bold)
                    
                    MarketRow(coin: "BTC", price: "$68,377", up: true)
                    MarketRow(coin: "ETH", price: "$1,985", up: true)
                    MarketRow(coin: "SOL", price: "$86", up: true)
                    MarketRow(coin: "SPY", price: "$681.75", up: false)
                    MarketRow(coin: "TSLA", price: "$417.44", up: false)
                }
                .padding()
                .background(Color.gray.opacity(0.1))
                .cornerRadius(15)
                
                Spacer()
            }
            .padding()
            .navigationTitle("Clyde")
        }
    }
}

struct MarketRow: View {
    let coin: String
    let price: String
    let up: Bool
    
    var body: some View {
        HStack {
            Text(coin)
                .font(.headline)
            Spacer()
            Text(price)
                .font(.subheadline)
            Image(systemName: up ? "arrow.up.right" : "arrow.down.right")
                .foregroundColor(up ? .green : .red)
        }
    }
}

struct GainiumTab: View {
    var body: some View {
        NavigationStack {
            List {
                BotRow(name: "Moccasin Tortoise", pair: "WLFI/USDC", pnl: "+$210.51", status: "Active")
                BotRow(name: "Bronze Crane", pair: "PENDLE", pnl: "+$146.36", status: "Closed")
                BotRow(name: "Green Chickadee", pair: "CVX", pnl: "+$244.41", status: "Error")
            }
            .navigationTitle("Gainium")
        }
    }
}

struct BotRow: View {
    let name: String
    let pair: String
    let pnl: String
    let status: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(name).font(.headline)
                Spacer()
                Text(status)
                    .font(.caption)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 4)
                    .background(statusColor)
                    .foregroundColor(.white)
                    .cornerRadius(8)
            }
            HStack {
                Text(pair).foregroundColor(.secondary)
                Spacer()
                Text(pnl).font(.title3).fontWeight(.bold).foregroundColor(.green)
            }
        }
        .padding(.vertical, 5)
    }
    
    var statusColor: Color {
        switch status {
        case "Active": return .green
        case "Closed": return .blue
        case "Error": return .red
        default: return .gray
        }
    }
}

struct BotsTab: View {
    var body: some View {
        NavigationStack {
            List {
                Section("Trading") {
                    Label("Gainium Bots", systemImage: "chart.line.uptrend.xyaxis")
                    Label("Paper Trading", systemImage: "doc.text")
                }
                Section("Research") {
                    Label("Fragrance ROI", systemImage: "flame")
                    Label("eBay Data", systemImage: "magnifyingglass")
                }
            }
            .navigationTitle("Bots")
        }
    }
}

struct SettingsTab: View {
    var body: some View {
        NavigationStack {
            List {
                Toggle("Notifications", isOn: .constant(true))
                Toggle("Auto Refresh", isOn: .constant(true))
                
                Section("About") {
                    HStack { Text("Version"); Spacer(); Text("1.0.0") }
                    HStack { Text("Clyde"); Spacer(); Text("🐙") }
                }
            }
            .navigationTitle("Settings")
        }
    }
}
