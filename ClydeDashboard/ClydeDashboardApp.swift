//
//  ClydeDashboardApp.swift
//  ClydeDashboard
//
//  Liquid Glass Design - Fixed Safe Areas
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
        ZStack {
            // Background
            LinearGradient(
                colors: [Color.purple.opacity(0.5), Color.blue.opacity(0.4), Color.cyan.opacity(0.3)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Header
                VStack(spacing: 4) {
                    Text("Clyde")
                        .font(.system(size: 44, weight: .bold))
                        .foregroundStyle(.white)
                    Text("Dashboard")
                        .font(.system(size: 20, weight: .medium))
                        .foregroundStyle(.white.opacity(0.8))
                }
                .padding(.top, 60)
                .padding(.bottom, 20)
                .frame(maxWidth: .infinity)
                .background(.ultraThinMaterial)
                
                // Scroll Content
                ScrollView {
                    VStack(spacing: 25) {
                        // P&L Card
                        VStack(spacing: 10) {
                            Text("Total P&L")
                                .font(.system(size: 24))
                                .foregroundStyle(.secondary)
                            Text("+$601.28")
                                .font(.system(size: 60, weight: .bold))
                                .foregroundStyle(.green)
                        }
                        .frame(maxWidth: .infinity)
                        .padding(35)
                        .background {
                            RoundedRectangle(cornerRadius: 30)
                                .fill(.ultraThinMaterial)
                                .overlay {
                                    RoundedRectangle(cornerRadius: 30)
                                        .stroke(.white.opacity(0.4), lineWidth: 1.5)
                                }
                        }
                        .padding(.horizontal)
                        
                        // Stats
                        HStack(spacing: 20) {
                            VStack(spacing: 10) {
                                Image(systemName: "brain.fill")
                                    .font(.system(size: 40))
                                    .foregroundStyle(.blue)
                                Text("3")
                                    .font(.system(size: 40, weight: .bold))
                                Text("Bots")
                                    .font(.system(size: 16))
                                    .foregroundStyle(.secondary)
                            }
                            .frame(maxWidth: .infinity)
                            .padding(25)
                            .background {
                                RoundedRectangle(cornerRadius: 20)
                                    .fill(.ultraThinMaterial)
                            }
                            
                            VStack(spacing: 10) {
                                Image(systemName: "banknote.fill")
                                    .font(.system(size: 40))
                                    .foregroundStyle(.orange)
                                Text("59%")
                                    .font(.system(size: 40, weight: .bold))
                                Text("Used")
                                    .font(.system(size: 16))
                                    .foregroundStyle(.secondary)
                            }
                            .frame(maxWidth: .infinity)
                            .padding(25)
                            .background {
                                RoundedRectangle(cornerRadius: 20)
                                    .fill(.ultraThinMaterial)
                            }
                        }
                        .padding(.horizontal)
                        
                        // Market
                        VStack(alignment: .leading, spacing: 15) {
                            Text("Market")
                                .font(.system(size: 26, weight: .bold))
                                .foregroundStyle(.white)
                                .padding(.horizontal)
                            
                            VStack(spacing: 0) {
                                MarketRow(coin: "BTC", price: "$68,377", change: "+2.1%", up: true)
                                Divider().background(Color.white.opacity(0.2))
                                MarketRow(coin: "ETH", price: "$1,985", change: "+1.3%", up: true)
                                Divider().background(Color.white.opacity(0.2))
                                MarketRow(coin: "SOL", price: "$86", change: "+0.8%", up: true)
                                Divider().background(Color.white.opacity(0.2))
                                MarketRow(coin: "SPY", price: "$681.75", change: "-0.2%", up: false)
                                Divider().background(Color.white.opacity(0.2))
                                MarketRow(coin: "TSLA", price: "$417.44", change: "-1.1%", up: false)
                            }
                            .padding(20)
                            .background {
                                RoundedRectangle(cornerRadius: 20)
                                    .fill(.ultraThinMaterial)
                            }
                        }
                        .padding(.horizontal)
                        
                        // Bots
                        VStack(alignment: .leading, spacing: 15) {
                            Text("Gainium Bots")
                                .font(.system(size: 26, weight: .bold))
                                .foregroundStyle(.white)
                                .padding(.horizontal)
                            
                            VStack(spacing: 0) {
                                BotRow(name: "Moccasin Tortoise", pair: "WLFI/USDC", pnl: "+$210.51", status: "Active")
                                Divider().background(Color.white.opacity(0.2))
                                BotRow(name: "Bronze Crane", pair: "PENDLE", pnl: "+$146.36", status: "Closed")
                                Divider().background(Color.white.opacity(0.2))
                                BotRow(name: "Green Chickadee", pair: "CVX", pnl: "+$244.41", status: "Error")
                            }
                            .padding(20)
                            .background {
                                RoundedRectangle(cornerRadius: 20)
                                    .fill(.ultraThinMaterial)
                            }
                        }
                        .padding(.horizontal)
                        
                        Spacer(minLength: 100)
                    }
                    .padding(.top, 20)
                }
            }
        }
    }
}

struct MarketRow: View {
    let coin: String
    let price: String
    let change: String
    let up: Bool
    
    var body: some View {
        HStack {
            Text(coin)
                .font(.system(size: 22, weight: .semibold))
                .foregroundStyle(.white)
            Spacer()
            Text(price)
                .font(.system(size: 20))
                .foregroundStyle(.white.opacity(0.9))
            Text(change)
                .font(.system(size: 18, weight: .semibold))
                .foregroundStyle(up ? .green : .red)
                .padding(.horizontal, 14)
                .padding(.vertical, 8)
                .background {
                    Capsule()
                        .fill(up ? Color.green.opacity(0.3) : Color.red.opacity(0.3))
                }
        }
        .padding(.vertical, 10)
    }
}

struct BotRow: View {
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
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Text(name)
                    .font(.system(size: 20, weight: .semibold))
                    .foregroundStyle(.white)
                Spacer()
                Text(status)
                    .font(.system(size: 16, weight: .medium))
                    .foregroundStyle(.white)
                    .padding(.horizontal, 14)
                    .padding(.vertical, 6)
                    .background {
                        Capsule()
                            .fill(statusColor)
                    }
            }
            
            HStack {
                Text(pair)
                    .font(.system(size: 18))
                    .foregroundStyle(.white.opacity(0.7))
                Spacer()
                Text(pnl)
                    .font(.system(size: 24, weight: .bold))
                    .foregroundStyle(.green)
            }
        }
        .padding(.vertical, 10)
    }
}
