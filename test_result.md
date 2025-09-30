#!/usr/bin/env python3
"""
Test script for Trading Case API
Demonstrates the main functionality with various examples
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{API_BASE}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_strategies():
    """Test strategies listing endpoint"""
    print("🔍 Testing strategies endpoint...")
    response = requests.get(f"{API_BASE}/api/strategies")
    print(f"Status: {response.status_code}")
    print(f"Available strategies: {json.dumps(response.json(), indent=2)}")
    print()

def test_backtest(name, payload):
    """Test backtest endpoint with given payload"""
    print(f"🚀 Testing backtest: {name}")
    print(f"Request: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{API_BASE}/api/backtest", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Backtest Results:")
        print(f"   Symbol: {result['symbol']}")
        print(f"   Period: {result['start_date']} to {result['end_date']}")
        print(f"   Initial Cash: ${result['initial_cash']:,.2f}")
        print(f"   Final Cash: ${result['final_cash']:,.2f}")
        print(f"   Profit/Loss: ${result['profit_loss']:,.2f} ({result['profit_loss_percent']:.2f}%)")
        print(f"   Total Trades: {result['total_trades']}")
        print(f"   Winning Trades: {result['winning_trades']}")
        print(f"   Losing Trades: {result['losing_trades']}")
        print(f"   Max Drawdown: ${result['max_drawdown']:,.2f} ({result['max_drawdown_percent']:.2f}%)")
        print(f"   Strategy: {result['strategy']} (MA {result['fast_period']}/{result['slow_period']})")
    else:
        print(f"❌ Error: {response.json()}")
    print()

def test_validation_errors():
    """Test validation error handling"""
    print("🔍 Testing validation errors...")
    
    # Test invalid date range
    test_backtest("Invalid Date Range", {
        "symbol": "AAPL",
        "start_date": "2023-12-31",
        "end_date": "2023-01-01",
        "initial_cash": 100000.0
    })
    
    # Test invalid MA periods
    test_backtest("Invalid MA Periods", {
        "symbol": "AAPL",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "initial_cash": 100000.0,
        "fast_period": 30,
        "slow_period": 10
    })

def main():
    """Run all tests"""
    print("=" * 60)
    print("Trading Case API Test Suite")
    print("=" * 60)
    print()
    
    # Basic endpoint tests
    test_health()
    test_strategies()
    
    # Successful backtest examples
    test_backtest("AAPL - Default Parameters", {
        "symbol": "AAPL",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "initial_cash": 100000.0
    })
    
    test_backtest("TSLA - Custom Parameters", {
        "symbol": "TSLA",
        "start_date": "2023-06-01",
        "end_date": "2023-12-31",
        "initial_cash": 50000.0,
        "fast_period": 5,
        "slow_period": 20
    })
    
    test_backtest("GOOGL - Long-term Strategy", {
        "symbol": "GOOGL",
        "start_date": "2023-01-01",
        "end_date": "2023-06-30",
        "initial_cash": 200000.0,
        "fast_period": 20,
        "slow_period": 50
    })
    
    # Validation error tests
    test_validation_errors()
    
    print("=" * 60)
    print("🎉 Test suite completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure the server is running on http://localhost:8000")
        print("   Start the server with: python main.py")