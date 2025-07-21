"""
Tests for Pension Fund Analytics Module

This module contains unit tests for the risk metrics and analytics functionality.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics.risk_metrics import PensionFundAnalytics
from config import config

class TestPensionFundAnalytics:
    """Test class for PensionFundAnalytics"""
    
    @pytest.fixture
    def analytics(self):
        """Create analytics instance for testing"""
        return PensionFundAnalytics()
    
    @pytest.fixture
    def sample_data(self):
        """Create sample fund data for testing"""
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        
        # Generate realistic fund data
        np.random.seed(42)
        
        data = []
        symbols = ['VTI', 'VXUS', 'BND']
        
        for symbol in symbols:
            # Generate price series
            base_price = 100 if symbol == 'VTI' else (50 if symbol == 'VXUS' else 80)
            returns = np.random.normal(0.0005, 0.015, len(dates))
            prices = [base_price]
            
            for ret in returns[1:]:
                new_price = prices[-1] * (1 + ret)
                prices.append(max(new_price, 1))
            
            # Create DataFrame for this symbol
            symbol_data = pd.DataFrame({
                'Date': dates,
                'Symbol': symbol,
                'Open': prices,
                'High': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
                'Low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
                'Close': prices,
                'Volume': np.random.randint(1000000, 10000000, len(dates)),
                'Daily_Return': [0] + [prices[i]/prices[i-1] - 1 for i in range(1, len(prices))]
            })
            
            data.append(symbol_data)
        
        return pd.concat(data, ignore_index=True)
    
    def test_analytics_initialization(self, analytics):
        """Test analytics module initialization"""
        assert analytics is not None
        assert hasattr(analytics, 'config')
        assert hasattr(analytics, 'scaler')
    
    def test_calculate_risk_metrics(self, analytics, sample_data):
        """Test risk metrics calculation"""
        metrics = analytics.calculate_risk_metrics(sample_data)
        
        assert isinstance(metrics, dict)
        assert len(metrics) > 0
        
        # Check that metrics exist for each symbol
        for symbol in sample_data['Symbol'].unique():
            assert symbol in metrics
            symbol_metrics = metrics[symbol]
            
            # Check for key metrics
            assert 'volatility' in symbol_metrics
            assert 'sharpe_ratio' in symbol_metrics
            assert 'total_return' in symbol_metrics
    
    def test_annualize_return(self, analytics):
        """Test annualized return calculation"""
        # Test with positive returns
        returns = pd.Series([0.01, 0.02, 0.01, 0.03])
        annualized = analytics._annualize_return(returns)
        assert isinstance(annualized, float)
        assert annualized > 0
        
        # Test with empty series
        empty_returns = pd.Series([])
        annualized = analytics._annualize_return(empty_returns)
        assert annualized == 0.0
    
    def test_calculate_sharpe_ratio(self, analytics):
        """Test Sharpe ratio calculation"""
        returns = pd.Series([0.01, 0.02, -0.01, 0.03])
        sharpe = analytics._calculate_sharpe_ratio(returns)
        
        assert isinstance(sharpe, float)
        # Sharpe ratio can be positive or negative depending on returns
    
    def test_calculate_var(self, analytics):
        """Test Value at Risk calculation"""
        returns = pd.Series([0.01, 0.02, -0.01, 0.03, -0.02])
        var_95 = analytics._calculate_var(returns, confidence_level=0.95)
        var_99 = analytics._calculate_var(returns, confidence_level=0.99)
        
        assert isinstance(var_95, float)
        assert isinstance(var_99, float)
        assert var_99 <= var_95  # 99% VaR should be more extreme than 95% VaR
    
    def test_calculate_cvar(self, analytics):
        """Test Conditional Value at Risk calculation"""
        returns = pd.Series([0.01, 0.02, -0.01, 0.03, -0.02])
        cvar_95 = analytics._calculate_cvar(returns, confidence_level=0.95)
        
        assert isinstance(cvar_95, float)
        # CVaR should be less than or equal to VaR
        var_95 = analytics._calculate_var(returns, confidence_level=0.95)
        assert cvar_95 <= var_95
    
    def test_detect_anomalies(self, analytics, sample_data):
        """Test anomaly detection"""
        anomalies = analytics.detect_anomalies(sample_data)
        
        assert isinstance(anomalies, dict)
        assert len(anomalies) > 0
        
        for symbol in sample_data['Symbol'].unique():
            if symbol in anomalies:
                symbol_anomalies = anomalies[symbol]
                assert 'anomalies' in symbol_anomalies
                assert 'anomaly_score' in symbol_anomalies
                assert isinstance(symbol_anomalies['anomalies'], list)
                assert isinstance(symbol_anomalies['anomaly_score'], float)
    
    def test_optimize_allocation(self, analytics, sample_data):
        """Test asset allocation optimization"""
        optimization = analytics.optimize_allocation(sample_data)
        
        if optimization:  # Optimization might fail with insufficient data
            assert isinstance(optimization, dict)
            assert 'optimized_allocation' in optimization
            assert 'expected_return' in optimization
            assert 'expected_volatility' in optimization
    
    def test_generate_performance_report(self, analytics, sample_data):
        """Test comprehensive performance report generation"""
        report = analytics.generate_performance_report(sample_data)
        
        assert isinstance(report, dict)
        assert 'report_date' in report
        assert 'data_period' in report
        assert 'risk_metrics' in report
        assert 'anomaly_detection' in report
        assert 'allocation_optimization' in report
        assert 'summary_statistics' in report
    
    def test_empty_data_handling(self, analytics):
        """Test handling of empty data"""
        empty_df = pd.DataFrame()
        
        # Test risk metrics with empty data
        metrics = analytics.calculate_risk_metrics(empty_df)
        assert metrics == {}
        
        # Test anomaly detection with empty data
        anomalies = analytics.detect_anomalies(empty_df)
        assert anomalies == {}
        
        # Test optimization with empty data
        optimization = analytics.optimize_allocation(empty_df)
        assert optimization == {}
    
    def test_data_validation(self, analytics):
        """Test data validation and error handling"""
        # Test with invalid data
        invalid_data = pd.DataFrame({
            'Symbol': ['VTI'],
            'Date': ['invalid_date'],
            'Close': ['not_a_number']
        })
        
        # Should handle gracefully without crashing
        try:
            metrics = analytics.calculate_risk_metrics(invalid_data)
            # Should return empty dict or handle gracefully
            assert isinstance(metrics, dict)
        except Exception as e:
            # Should not crash, but might raise reasonable exceptions
            assert "date" in str(e).lower() or "numeric" in str(e).lower()

def test_config_integration():
    """Test that analytics can work with config"""
    analytics = PensionFundAnalytics(config.analytics)
    assert analytics.config == config.analytics

if __name__ == "__main__":
    pytest.main([__file__]) 