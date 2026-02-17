//
//  ClydeDashboardApp.swift
//  ClydeDashboard
//
//  iOS Version - Fixed Scaling
//

import SwiftUI

// MARK: - Design System
struct GlassDesign {
    static let primary = Color(red: 0, green: 122/255, blue: 1)
    static let green = Color(red: 52/255, green: 199/255, blue: 89/255)
    static let red = Color(red: 1, green: 59/255, blue: 48/255)
    static let orange = Color(red: 1, green: 149/255, blue: 0)
    static let purple = Color(red: 88/255, green: 86/255, blue: 214/255)
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
        .tint(GlassDesign.primary)
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
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        Text("+$601.28")
                            .font(.system(size: 36, weight: .bold))
                            .foregroundColor(.green)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color(.systemBackground))
                    .cornerRadius(16)
                    .shadow(radius: 2)
                    
                    // Stats Grid
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 16) {
                        StatCard(title: "Active Bots", value: "3", icon: "brain", color: .blue)
                        StatCard(title: "Bankroll Used", value: "59%", icon: "banknote", color: .orange)
                    }
                    
                    // Market Section
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Market")
                            .font(.headline)
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
                        .cornerRadius(12)
                    }
                }
                .padding()
            }
            .background(Color(.systemGroupedBackground))
            .navigationTitle("Clyde Dashboard")
        }
    }
}

struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)
            Text(value)
                .font(.title2)
                .fontWeight(.bold)
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(radius: 2)
    }
}

struct MarketRow: View {
    let coin: String
    let price: String
    let change: String
    
    var body: some View {
        HStack {
            Text(coin)
                .font(.headline)
            Spacer()
            Text(price)
                .font(.subheadline)
            Text(change)
                .font(.caption)
                .foregroundColor(change.hasPrefix("+") ? .green : .red)
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background((change.hasPrefix("+") ? Color.green : Color.red).opacity(0.1))
                .cornerRadius(8)
        }
        .padding()
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
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(name)
                    .font(.headline)
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
                Text(pair)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                Spacer()
                Text(pnl)
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(.green)
            }
        }
        .padding(.vertical, 8)
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

@main
struct ClydeDashboardApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
