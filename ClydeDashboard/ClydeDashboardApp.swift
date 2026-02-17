//
//  ClydeDashboardApp.swift
//  ClydeDashboard
//
//  iOS Version - Fixed for iPhone
//

import SwiftUI

struct ClydeDashboardApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .ignoresSafeArea(edges: .top)
        }
    }
}

struct ContentView: View {
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            DashboardView()
                .tabItem {
                    Label("Dashboard", systemImage: "chart.bar.fill")
                }
                .tag(0)
            
            GainiumView()
                .tabItem {
                    Label("Gainium", systemImage: "arrow.triangle.branch")
                }
                .tag(1)
            
            BotsView()
                .tabItem {
                    Label("Bots", systemImage: "brain")
                }
                .tag(2)
            
            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
                .tag(3)
        }
        .tint(.blue)
    }
}

struct DashboardView: View {
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // P&L Card
                    VStack(spacing: 8) {
                        Text("Total P&L")
                            .font(.title3)
                            .foregroundColor(.secondary)
                        Text("+$601.28")
                            .font(.system(size: 44, weight: .bold))
                            .foregroundColor(.green)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(30)
                    .background(Color(.systemBackground))
                    .cornerRadius(20)
                    .shadow(radius: 4)
                    
                    // Stats Grid
                    HStack(spacing: 16) {
                        StatCard(title: "Active Bots", value: "3", icon: "brain", color: .blue)
                        StatCard(title: "Bankroll", value: "59%", icon: "banknote", color: .orange)
                    }
                    
                    // Market Section
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Market")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)
                        
                        VStack(spacing: 0) {
                            MarketRow(coin: "BTC", price: "$68,377", change: "+2.1%")
                            Divider()
                            MarketRow(coin: "ETH", price: "$1,985", change: "+1.3%")
                            Divider()
                            MarketRow(coin: "SOL", price: "$86", change: "+0.8%")
                            Divider()
                            MarketRow(coin: "SPY", price: "$681.75", change: "-0.2%")
                            Divider()
                            MarketRow(coin: "TSLA", price: "$417.44", change: "-1.1%")
                        }
                        .background(Color(.systemBackground))
                        .cornerRadius(16)
                        .padding(.horizontal)
                    }
                }
                .padding(.top, 20)
            }
            .background(Color(.systemGroupedBackground))
            .navigationTitle("Clyde")
        }
    }
}

struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: icon)
                .font(.title)
                .foregroundColor(color)
            Text(value)
                .font(.title)
                .fontWeight(.bold)
            Text(title)
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding(20)
        .background(Color(.systemBackground))
        .cornerRadius(16)
        .shadow(radius: 2)
    }
}

struct MarketRow: View {
    let coin: String
    let price: String
    let change: String
    
    var isPositive: Bool {
        change.hasPrefix("+")
    }
    
    var body: some View {
        HStack {
            Text(coin)
                .font(.title3)
                .fontWeight(.semibold)
            Spacer()
            Text(price)
                .font(.title3)
            Text(change)
                .font(.subheadline)
                .fontWeight(.medium)
                .foregroundColor(isPositive ? .green : .red)
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(isPositive ? Color.green.opacity(0.15) : Color.red.opacity(0.15))
                .cornerRadius(10)
        }
        .padding(20)
    }
}

struct GainiumView: View {
    var body: some View {
        NavigationStack {
            List {
                BotCard(name: "Moccasin Tortoise", pair: "WLFI/USDC", pnl: "+$210.51", status: "Active")
                BotCard(name: "Bronze Crane", pair: "PENDLE", pnl: "+$146.36", status: "Closed")
                BotCard(name: "Green Chickadee", pair: "CVX", pnl: "+$244.41", status: "Error")
            }
            .navigationTitle("Gainium Bots")
        }
    }
}

struct BotCard: View {
    let name: String
    let pair: String
    let pnl: String
    let status: String
    
    var statusColor: Color {
        switch status {
        case "Active": return .green
        case "Closed": return .blue
        case "Error": return .red
        default: return .gray
        }
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text(name)
                    .font(.headline)
                Spacer()
                Text(status)
                    .font(.subheadline)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(statusColor)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
            
            HStack {
                Text(pair)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                Spacer()
                Text(pnl)
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.green)
            }
        }
        .padding(.vertical, 12)
        .listRowInsets(EdgeInsets(top: 8, leading: 16, bottom: 8, trailing: 16))
    }
}

struct BotsView: View {
    var body: some View {
        NavigationStack {
            List {
                Section("Trading") {
                    NavigationLink {
                        GainiumView()
                    } label: {
                        Label("Gainium Bots", systemImage: "arrow.triangle.branch")
                    }
                    
                    NavigationLink {
                        Text("Paper Trading")
                    } label: {
                        Label("Paper Trading", systemImage: "doc.text")
                    }
                }
                
                Section("Research") {
                    NavigationLink {
                        Text("Fragrance ROI")
                    } label: {
                        Label("Fragrance ROI", systemImage: "flame")
                    }
                }
            }
            .navigationTitle("Bots")
        }
    }
}

struct SettingsView: View {
    @State private var notifications = true
    @State private var autoRefresh = true
    
    var body: some View {
        NavigationStack {
            List {
                Toggle(isOn: $notifications) {
                    Label("Notifications", systemImage: "bell")
                }
                
                Toggle(isOn: $autoRefresh) {
                    Label("Auto Refresh", systemImage: "arrow.clockwise")
                }
                
                Section("Info") {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.secondary)
                    }
                    
                    HStack {
                        Text("Clyde")
                        Spacer()
                        Text("🐙")
                    }
                }
            }
            .navigationTitle("Settings")
        }
    }
}
