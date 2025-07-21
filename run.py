#!/usr/bin/env python3
"""
Main startup script for Pension Fund Performance Analytics Platform

This script provides a command-line interface to run different components
of the platform including ETL pipeline, API server, and tests.
"""

import argparse
import sys
import os
import logging
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config as global_config
from etl.pipeline import PensionFundETL
from analytics.risk_metrics import PensionFundAnalytics

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, global_config.logging.level),
        format=global_config.logging.format,
        handlers=[
            logging.FileHandler(global_config.logging.file_path),
            logging.StreamHandler()
        ]
    )

def run_etl():
    """Run the ETL pipeline"""
    print("Starting ETL Pipeline...")
    setup_logging()
    
    try:
        etl = PensionFundETL()
        result = etl.run_pipeline(use_sample_data=True)
        
        if result:
            print("ETL pipeline completed successfully!")
            print(f"Data saved to: {result}")
        else:
            print("ETL pipeline failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"ETL pipeline error: {str(e)}")
        sys.exit(1)

def run_api():
    """Start the FastAPI server"""
    print("Starting API Server...")
    
    try:
        import uvicorn
        from api.app import app
        
        print(f"API will be available at: http://{global_config.api.host}:{global_config.api.port}")
        print(f"API documentation at: http://{global_config.api.host}:{global_config.api.port}/docs")
        print("Press Ctrl+C to stop the server")
        
        uvicorn.run(
            "api.app:app",
            host=global_config.api.host,
            port=global_config.api.port,
            reload=global_config.api.debug,
            log_level=global_config.logging.level.lower()
        )
        
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {str(e)}")
        print("[TIP] Run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] API server error: {str(e)}")
        sys.exit(1)

def run_tests():
    """Run the test suite"""
    print("[TEST] Running Tests...")
    
    try:
        import pytest
        
        # Run tests
        test_dir = Path(__file__).parent / "tests"
        result = pytest.main([str(test_dir), "-v"])
        
        if result == 0:
            print("[SUCCESS] All tests passed!")
        else:
            print("[ERROR] Some tests failed")
            sys.exit(1)
            
    except ImportError:
        print("[ERROR] pytest not installed. Install with: pip install pytest")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Test error: {str(e)}")
        sys.exit(1)

def run_analytics():
    """Run analytics on sample data"""
    print("[ANALYTICS] Running Analytics...")
    setup_logging()
    
    try:
        # Run ETL to get data
        etl = PensionFundETL()
        filepath = etl.run_pipeline(use_sample_data=True)
        
        if not filepath or not os.path.exists(filepath):
            print("[ERROR] No data available for analytics")
            sys.exit(1)
        
        # Load data
        import pandas as pd
        df = pd.read_csv(filepath)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Run analytics
        analytics = PensionFundAnalytics()
        report = analytics.generate_performance_report(df)
        
        print("[SUCCESS] Analytics completed!")
        print(f"[DATA] Analyzed {len(df)} data points")
        print(f"[FUNDS] Funds analyzed: {report.get('summary_statistics', {}).get('funds_analyzed', [])}")
        
        # Print key metrics
        risk_metrics = report.get('risk_metrics', {})
        if 'portfolio' in risk_metrics:
            portfolio = risk_metrics['portfolio']
            print(f"[METRICS] Portfolio Return: {portfolio.get('portfolio_return', 0):.2%}")
            print(f"[METRICS] Portfolio Volatility: {portfolio.get('portfolio_volatility', 0):.2%}")
            print(f"[METRICS] Portfolio Sharpe Ratio: {portfolio.get('portfolio_sharpe', 0):.2f}")
        
    except Exception as e:
        print(f"[ERROR] Analytics error: {str(e)}")
        sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("[CHECK] Checking Dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'scipy', 'scikit-learn',
        'fastapi', 'uvicorn', 'pydantic',
        'yfinance', 'plotly', 'matplotlib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"[OK] {package}")
        except ImportError:
            print(f"[MISSING] {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n[ERROR] Missing packages: {', '.join(missing_packages)}")
        print("[TIP] Install with: pip install -r requirements.txt")
        return False
    else:
        print("\n[SUCCESS] All dependencies are installed!")
        return True

def main():
    """Main function with command-line interface"""
    parser = argparse.ArgumentParser(
        description="Pension Fund Performance Analytics Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py etl          # Run ETL pipeline
  python run.py api          # Start API server
  python run.py test         # Run tests
  python run.py analytics    # Run analytics on sample data
  python run.py check        # Check dependencies
        """
    )
    
    parser.add_argument(
        'command',
        choices=['etl', 'api', 'test', 'analytics', 'check'],
        help='Command to run'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print("=" * 50)
    print("= Pension Fund Performance Analytics Platform =")
    print("=" * 50)
    print()
    
    # Execute command
    if args.command == 'etl':
        run_etl()
    elif args.command == 'api':
        run_api()
    elif args.command == 'test':
        run_tests()
    elif args.command == 'analytics':
        run_analytics()
    elif args.command == 'check':
        check_dependencies()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 