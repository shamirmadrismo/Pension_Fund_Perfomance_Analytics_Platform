#!/usr/bin/env python3
"""
Debug script to test config import and analytics initialization
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_config_import():
    """Test config import and analytics initialization"""
    print("🔍 Testing Config Import...")
    
    try:
        from config import config as global_config
        print("✅ Config imported successfully")
        print(f"📊 Config type: {type(global_config)}")
        
        if hasattr(global_config, 'analytics'):
            print("✅ Config has analytics attribute")
            print(f"📊 Analytics config type: {type(global_config.analytics)}")
            
            if global_config.analytics is not None:
                print("✅ Analytics config is not None")
                print(f"📊 Risk free rate: {global_config.analytics.sharpe_ratio_risk_free_rate}")
            else:
                print("❌ Analytics config is None")
        else:
            print("❌ Config does not have analytics attribute")
            
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    return True

def test_analytics_initialization():
    """Test analytics class initialization"""
    print("\n🔍 Testing Analytics Initialization...")
    
    try:
        from analytics.risk_metrics import PensionFundAnalytics
        from config import config as global_config
        
        analytics = PensionFundAnalytics(config=global_config)
        print("✅ Analytics initialized successfully")
        print(f"📊 Analytics config type: {type(analytics.config)}")
        
        if hasattr(analytics.config, 'analytics'):
            print("✅ Analytics config has analytics attribute")
            print(f"📊 Risk free rate: {analytics.config.analytics.sharpe_ratio_risk_free_rate}")
        else:
            print("❌ Analytics config does not have analytics attribute")
            
    except Exception as e:
        print(f"❌ Analytics initialization failed: {e}")
        return False
    
    return True

def main():
    """Main debug function"""
    print("🏦" * 50)
    print("🏦 Config Debug Script 🏦")
    print("🏦" * 50)
    print()
    
    config_ok = test_config_import()
    analytics_ok = test_analytics_initialization()
    
    print("\n" + "="*50)
    if config_ok and analytics_ok:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")

if __name__ == "__main__":
    main() 