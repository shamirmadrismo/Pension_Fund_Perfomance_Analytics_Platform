#!/usr/bin/env python3
"""
Demonstration script for Pension Fund Performance Analytics Platform

This script shows how to interact with the API endpoints and demonstrates
the platform's capabilities.
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

# Demo token (in production, this would be a real authentication token)
DEMO_TOKEN = "demo-token-123"

def make_request(endpoint, params=None, method="GET"):
    """Make a request to the API with authentication"""
    headers = {
        "Authorization": f"Bearer {DEMO_TOKEN}",
        "Content-Type": "application/json"
    }
    
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API server at {BASE_URL}")
        print("💡 Make sure the API server is running: python run.py api")
        return None
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return None

def demo_health_check():
    """Demo the health check endpoint"""
    print("🏥 Testing Health Check...")
    result = make_request("/health")
    if result:
        print(f"✅ API Status: {result['status']}")
        print(f"📅 Timestamp: {result['timestamp']}")
        print(f"🔢 Version: {result['version']}")

def demo_root_endpoint():
    """Demo the root endpoint"""
    print("\n🏠 Testing Root Endpoint...")
    result = make_request("/")
    if result:
        print(f"✅ Message: {result['message']}")
        print(f"🔢 Version: {result['version']}")

def demo_fund_performance():
    """Demo the fund performance endpoint"""
    print("\n📊 Testing Fund Performance...")
    result = make_request("/api/v1/fund/performance")
    if result:
        print(f"✅ Status: {result['status']}")
        if 'metadata' in result:
            metadata = result['metadata']
            print(f"📈 Total Funds: {metadata.get('total_funds', 'N/A')}")
            print(f"📊 Total Observations: {metadata.get('total_observations', 'N/A')}")

def demo_risk_metrics():
    """Demo the risk metrics endpoint"""
    print("\n⚠️ Testing Risk Metrics...")
    result = make_request("/api/v1/fund/risk-metrics")
    if result:
        print(f"✅ Status: {result['status']}")
        if 'portfolio_metrics' in result:
            portfolio = result['portfolio_metrics']
            print(f"📊 Portfolio Return: {portfolio.get('portfolio_return', 'N/A')}")
            print(f"📊 Portfolio Volatility: {portfolio.get('portfolio_volatility', 'N/A')}")

def demo_anomaly_detection():
    """Demo the anomaly detection endpoint"""
    print("\n🔍 Testing Anomaly Detection...")
    result = make_request("/api/v1/fund/anomalies")
    if result:
        print(f"✅ Status: {result['status']}")
        if 'metadata' in result:
            metadata = result['metadata']
            print(f"🔍 Total Funds Analyzed: {metadata.get('total_funds_analyzed', 'N/A')}")

def demo_allocation_optimization():
    """Demo the allocation optimization endpoint"""
    print("\n⚖️ Testing Asset Allocation Optimization...")
    result = make_request("/api/v1/fund/allocation")
    if result:
        print(f"✅ Status: {result['status']}")
        if 'data' in result:
            data = result['data']
            print(f"📊 Diversification Score: {data.get('diversification_score', 'N/A')}")

def demo_comprehensive_report():
    """Demo the comprehensive report endpoint"""
    print("\n📋 Testing Comprehensive Report...")
    result = make_request("/api/v1/fund/report")
    if result:
        print(f"✅ Status: {result['status']}")
        if 'report' in result:
            report = result['report']
            if 'summary_statistics' in report:
                stats = report['summary_statistics']
                print(f"📊 Total Funds: {stats.get('total_funds', 'N/A')}")
                print(f"📈 Total Observations: {stats.get('total_observations', 'N/A')}")

def demo_configuration():
    """Demo the configuration endpoint"""
    print("\n⚙️ Testing Configuration...")
    result = make_request("/api/v1/config")
    if result:
        print(f"✅ Status: {result['status']}")
        if 'data' in result:
            data = result['data']
            print(f"🔧 API Host: {data.get('api', {}).get('host', 'N/A')}")
            print(f"🔧 API Port: {data.get('api', {}).get('port', 'N/A')}")

def main():
    """Main demonstration function"""
    print("🏦" * 60)
    print("🏦 Pension Fund Analytics Platform - API Demonstration 🏦")
    print("🏦" * 60)
    print()
    
    print("🚀 Starting API demonstration...")
    print(f"🌐 API Base URL: {BASE_URL}")
    print(f"🔑 Using Demo Token: {DEMO_TOKEN}")
    print()
    
    # Run all demonstrations
    demo_health_check()
    demo_root_endpoint()
    demo_fund_performance()
    demo_risk_metrics()
    demo_anomaly_detection()
    demo_allocation_optimization()
    demo_comprehensive_report()
    demo_configuration()
    
    print("\n" + "="*60)
    print("🎉 API Demonstration Complete!")
    print()
    print("📚 API Documentation available at:")
    print(f"   {BASE_URL}/docs")
    print()
    print("🔧 Available Endpoints:")
    print("   GET  /health                    - Health check")
    print("   GET  /                          - Root endpoint")
    print("   GET  /api/v1/fund/performance   - Fund performance")
    print("   GET  /api/v1/fund/risk-metrics  - Risk analysis")
    print("   GET  /api/v1/fund/anomalies     - Anomaly detection")
    print("   GET  /api/v1/fund/allocation    - Asset allocation")
    print("   GET  /api/v1/fund/report        - Comprehensive report")
    print("   GET  /api/v1/config             - Configuration")
    print()
    print("💡 To test with real data, run: python run.py etl")

if __name__ == "__main__":
    main() 