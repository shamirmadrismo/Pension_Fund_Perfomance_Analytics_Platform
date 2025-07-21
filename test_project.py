#!/usr/bin/env python3
"""
Simple project structure test script
This script verifies that all project files are created correctly
"""

import os
import sys
from pathlib import Path

def test_project_structure():
    """Test that all required files and directories exist"""
    print("🔍 Testing Project Structure...")
    
    # Expected files and directories
    expected_structure = [
        "README.md",
        "requirements.txt", 
        "config.py",
        "run.py",
        "env_template.txt",
        "etl/pipeline.py",
        "analytics/risk_metrics.py",
        "api/app.py",
        "data/fund_returns.csv",
        "tests/test_analytics.py",
        "dashboard/README.md"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in expected_structure:
        if os.path.exists(file_path):
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    print(f"\n📊 Results:")
    print(f"✅ Found: {len(existing_files)} files")
    print(f"❌ Missing: {len(missing_files)} files")
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    else:
        print("\n🎉 All project files created successfully!")
        return True

def test_file_contents():
    """Test that key files have expected content"""
    print("\n📄 Testing File Contents...")
    
    # Test README.md
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
            if "Pension Fund Performance Analytics Platform" in content:
                print("✅ README.md - Contains project title")
            else:
                print("❌ README.md - Missing project title")
    
    # Test requirements.txt
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as f:
            content = f.read()
            if "yfinance" in content and "fastapi" in content:
                print("✅ requirements.txt - Contains key dependencies")
            else:
                print("❌ requirements.txt - Missing key dependencies")
    
    # Test config.py
    if os.path.exists("config.py"):
        with open("config.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "class Config:" in content:
                print("✅ config.py - Contains configuration class")
            else:
                print("❌ config.py - Missing configuration class")

def test_imports():
    """Test that Python modules can be imported (without external deps)"""
    print("\n🐍 Testing Python Imports...")
    
    try:
        # Test config import
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from config import config
        print("✅ config.py - Can be imported")
    except Exception as e:
        print(f"❌ config.py - Import failed: {e}")
    
    try:
        # Test ETL import (will fail without yfinance, but that's expected)
        from etl.pipeline import PensionFundETL
        print("✅ etl/pipeline.py - Can be imported")
    except ImportError as e:
        if "yfinance" in str(e):
            print("✅ etl/pipeline.py - Import structure correct (yfinance not installed)")
        else:
            print(f"❌ etl/pipeline.py - Import failed: {e}")
    except Exception as e:
        print(f"❌ etl/pipeline.py - Unexpected error: {e}")
    
    try:
        # Test analytics import
        from analytics.risk_metrics import PensionFundAnalytics
        print("✅ analytics/risk_metrics.py - Can be imported")
    except Exception as e:
        print(f"❌ analytics/risk_metrics.py - Import failed: {e}")

def test_data_files():
    """Test that data files exist and have content"""
    print("\n📊 Testing Data Files...")
    
    # Test sample data
    if os.path.exists("data/fund_returns.csv"):
        with open("data/fund_returns.csv", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) > 1:  # Has header + data
                print(f"✅ data/fund_returns.csv - Contains {len(lines)} lines")
            else:
                print("❌ data/fund_returns.csv - Empty or missing data")
    else:
        print("❌ data/fund_returns.csv - File not found")

def main():
    """Main test function"""
    print("🏦" * 50)
    print("🏦 Pension Fund Analytics Platform - Project Test 🏦")
    print("🏦" * 50)
    print()
    
    # Run all tests
    structure_ok = test_project_structure()
    test_file_contents()
    test_imports()
    test_data_files()
    
    print("\n" + "="*50)
    if structure_ok:
        print("🎉 Project structure is complete and ready for development!")
        print("\n📋 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run ETL pipeline: python run.py etl")
        print("3. Start API server: python run.py api")
        print("4. Run tests: python run.py test")
    else:
        print("❌ Some project files are missing. Please check the structure.")
    
    print("\n📚 API Documentation will be available at:")
    print("   http://localhost:8000/docs")
    print("\n📊 Dashboard setup instructions in dashboard/README.md")

if __name__ == "__main__":
    main() 