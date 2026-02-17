//
//  ClydeDashboardApp.swift
//  ClydeDashboard
//
//  Working iOS App - Big UI
//

import SwiftUI

@main
struct ClydeDashboardApp: App {
    var body: some Scene {
        WindowGroup {
            MainView()
        }
    }
}

struct MainView: View {
    var body: some View {
        GeometryReader { geo in
            VStack(spacing: 0) {
                // Header
                ZStack {
                    LinearGradient(colors: [Color.blue, Color.blue.opacity(0.8)], startPoint: .topLeading, endPoint: .bottomTrailing)
                    VStack {
                        Spacer()
                        Text("Clyde Dashboard")
                            .font(.system(size: 28, weight: .bold))
                            .foregroundColor(.white)
                        Spacer()
                    }
                    .padding(.top, 60)
                }
                .frame(height: 120)
                
                // Content
                ScrollView {
                    VStack(spacing: 20) {
                        // P&L Card
                        VStack(spacing: 10) {
                            Text("Total P&L")
                                .font(.title3)
                                .foregroundColor(.secondary)
                            Text("+$601.28")
                                .font(.system(size: 44, weight: .bold))
                                .foregroundColor(.green)
                        }
                        .frame(maxWidth: .infinity)
                        .padding(30)
                        .background(Color.white)
                        .cornerRadius(20)
                        .shadow(color: .black.opacity(0.1), radius: 10, x: 0, y: 5)
                        
                        // Stats Row
                        HStack(spacing: 15) {
                            StatBox(title: "Bots", value: "3", icon: "brain.fill", color: .blue)
                            StatBox(title: "Used", value: "59%", icon: "banknote.fill", color: .orange)
                        }
                        
                        // Market Section
                        VStack(alignment: .leading, spacing: 0) {
                            Text("Market")
                                .font(.title3)
                                .fontWeight(.bold)
                                .padding()
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .background(Color.white)
                            
                            Divider()
                            
                            MarketItem(coin: "BTC", price: "$68,377", change: "+2.1%", up: true)
                            Divider().padding(.leading)
                            MarketItem(coin: "ETH", price: "$1,985", change: "+1.3%", up: true)
                            Divider().padding(.leading)
                            MarketItem(coin: "SOL", price: "$86", change: "+0.8%", up: true)
                            Divider().padding(.leading)
                            MarketItem(coin: "SPY", price: "$681.75", change: "-0.2%", up: false)
                            Divider().padding(.leading)
                            MarketItem(coin: "TSLA", price: "$417.44", change: "-1.1%", up: false)
                        }
                        .background(Color.white)
                        .cornerRadius(20)
                        .shadow(color: .black.opacity(0.1), radius: 10, x: 0, y: 5)
                        
                        // Bots Section
                        VStack(alignment: .leading, spacing: 0) {
                            Text("Gainium Bots")
                                .font(.title3)
                                .fontWeight(.bold)
                                .padding()
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .background(Color.white)
                            
                            Divider()
                            
                            BotItem(name: "Moccasin Tortoise", pair: "WLFI/USDC", pnl: "+$210.51", status: "Active")
                            Divider().padding(.leading)
                            BotItem(name: "Bronze Crane", pair: "PENDLE", pnl: "+$146.36", status: "Closed")
                            Divider().padding(.leading)
                            BotItem(name: "Green Chickadee", pair: "CVX", pnl: "+$244.41", status: "Error")
                        }
                        .background(Color.white)
                        .cornerRadius(20)
                        .shadow(color: .black.opacity(0.1), radius: 10, x: 0, y: 5)
                    }
                    .padding(20)
                }
                .background(Color(UIColor.systemGroupedBackground))
            }
        }
    }
}

struct StatBox: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.title)
                .foregroundColor(color)
            Text(value)
                .font(.title2)
                .fontWeight(.bold)
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding(20)
        .background(Color.white)
        .cornerRadius(15)
        .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

struct MarketItem: View {
    let coin: String
    let price: String
    let change: String
    let up: Bool
    
    var body: some View {
        HStack {
            Text(coin)
                .font(.headline)
            Spacer()
            Text(price)
                .font(.subheadline)
            Text(change)
                .font(.caption)
                .fontWeight(.semibold)
                .foregroundColor(up ? .green : .red)
                .padding(.horizontal, 10)
                .padding(.vertical, 5)
                .background((up ? Color.green : Color.red).opacity(0.1))
                .cornerRadius(8)
        }
        .padding()
    }
}

struct BotItem: View {
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
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(name)
                    .font(.headline)
                Spacer()
                Text(status)
                    .font(.caption)
                    .fontWeight(.medium)
                    .foregroundColor(.white)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 4)
                    .background(statusColor)
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
        .padding()
    }
}
