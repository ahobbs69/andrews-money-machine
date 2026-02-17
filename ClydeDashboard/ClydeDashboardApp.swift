//
//  ClydeDashboardApp.swift
//  ClydeDashboard
//
//  iOS Version - Simple Dashboard
//

import SwiftUI

// MARK: - Simple Design System
struct GlassDesign {
    static let primary = Color(red: 0, green: 122/255, blue: 1)
    static let green = Color(red: 52/255, green: 199/255, blue: 89/255)
    static let red = Color(red: 1, green: 59/255, blue: 48/255)
    static let orange = Color(red: 1, green: 149/255, blue: 0)
    static let purple = Color(red: 88/255, green: 86/255, blue: 214/255)
    
    static let glassBackground = Color.gray.opacity(0.2)
}

struct ContentView: View {
    @State private var selectedTab: Int = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            DashboardView()
                .tabItem { Label("Dashboard", systemImage: "chart.bar.fill") }
                .tag(0)
            
            GainiumView()
                .tabItem { Label("Gainium", systemImage: "arrow.triangle.branch") }
                .tag(1)
            
            BotsView()
                .tabItem { Label("Bots", systemImage: "brain") }
                .tag(2)
            
            SettingsView()
                .tabItem { Label("Settings", systemImage: "gear") }
                .tag(3)
        }
        .tint(GlassDesign.primary)
    }
}

struct DashboardView: View {
    var body: some View {
        NavigationStack {
            List {
                Section("Trading") {
                    HStack {
                        Image(systemName: "chart.line.uptrend.xyaxis")
                            .foregroundColor(.green)
                        Text("P&L")
                        Spacer()
                        Text("+$601.28")
                            .foregroundColor(.green)
                            .fontWeight(.bold)
                    }
                    
                    HStack {
                        Image(systemName: "dollarsign.circle")
                        Text("Active Bots")
                        Spacer()
                        Text("3")
                    }
                    
                    HStack {
                        Image(systemName: "banknote")
                        Text("Bankroll Used")
                        Spacer()
                        Text("59%")
                    }
                }
                
                Section("Market") {
                    HStack { Text("BTC"); Spacer(); Text("$68,377") }
                    HStack { Text("ETH"); Spacer(); Text("$1,985") }
                    HStack { Text("SOL"); Spacer(); Text("$86") }
                    HStack { Text("SPY"); Spacer(); Text("$681.75") }
                    HStack { Text("TSLA"); Spacer(); Text("$417.44") }
                }
            }
            .navigationTitle("Clyde Dashboard")
        }
    }
}

struct GainiumView: View {
    var body: some View {
        NavigationStack {
            List {
                Section("Bots") {
                    BotRow(name: "Moccasin Tortoise", pair: "WLFI/USDC", pnl: "+$210.51", status: "Active")
                    BotRow(name: "Bronze Crane", pair: "PENDLE", pnl: "+$146.36", status: "Closed")
                    BotRow(name: "Green Chickadee", pair: "CVX", pnl: "+$244.41", status: "Error")
                }
            }
            .navigationTitle("Gainium Bots")
        }
    }
}

struct BotRow: View {
    let name: String
    let pair: String
    let pnl: String
    let status: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(name).font(.headline)
            Text(pair).font(.caption).foregroundColor(.gray)
            HStack {
                Text(pnl).foregroundColor(.green)
                Spacer()
                Text(status).font(.caption).padding(.horizontal, 8).background(status == "Error" ? Color.red.opacity(0.2) : Color.green.opacity(0.2)).cornerRadius(4)
            }
        }
        .padding(.vertical, 4)
    }
}

struct BotsView: View {
    var body: some View {
        NavigationStack {
            List {
                Section("Trading") {
                    NavigationLink("Gainium Bots") { GainiumView() }
                    NavigationLink("Paper Trading") { Text("Paper Trading") }
                }
                
                Section("Research") {
                    NavigationLink("Fragrance ROI") { Text("Fragrance Analysis") }
                    NavigationLink("eBay Research") { Text("eBay Data") }
                }
            }
            .navigationTitle("Bots & Research")
        }
    }
}

struct SettingsView: View {
    @State private var notifications = true
    @State private var autoRefresh = true
    
    var body: some View {
        NavigationStack {
            List {
                Toggle("Notifications", isOn: $notifications)
                Toggle("Auto Refresh", isOn: $autoRefresh)
                
                Section("About") {
                    HStack { Text("Version"); Spacer(); Text("1.0.0") }
                    HStack { Text("Clyde"); Spacer(); Text("🐙") }
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
