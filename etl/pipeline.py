"""
ETL Pipeline for Pension Fund Performance Analytics Platform

This module handles the extraction, transformation, and loading of pension fund data
from various sources into the analytics platform.
"""

import pandas as pd
import numpy as np
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config
import yfinance as yf

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.logging.level),
    format=config.logging.format,
    handlers=[
        logging.FileHandler(config.logging.file_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PensionFundETL:
    """
    ETL pipeline for pension fund data processing
    """
    
    def __init__(self):
        self.config = config.etl
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.config.data_directory,
            self.config.raw_data_path,
            self.config.processed_data_path,
            os.path.dirname(config.logging.file_path)
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def extract_fund_data(self, symbols: List[str], start_date: str, end_date: str) -> pd.DataFrame:
        """
        Extract fund data from Yahoo Finance API
        
        Args:
            symbols: List of fund symbols
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with fund data
        """
        logger.info(f"Extracting data for {len(symbols)} funds from {start_date} to {end_date}")
        
        all_data = []
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(start=start_date, end=end_date)
                
                if not data.empty:
                    data['Symbol'] = symbol
                    data['Date'] = data.index
                    data.reset_index(drop=True, inplace=True)
                    all_data.append(data)
                    logger.info(f"Successfully extracted data for {symbol}")
                else:
                    logger.warning(f"No data found for symbol {symbol}")
                    
            except Exception as e:
                logger.error(f"Error extracting data for {symbol}: {str(e)}")
                continue
        
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            return combined_data
        else:
            logger.error("No data extracted from any symbols")
            return pd.DataFrame()
    
    def transform_fund_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform raw fund data into analytics-ready format
        
        Args:
            df: Raw fund data DataFrame
            
        Returns:
            Transformed DataFrame
        """
        logger.info("Transforming fund data")
        
        if df.empty:
            return df
        
        # Calculate daily returns
        df['Daily_Return'] = df.groupby('Symbol')['Close'].pct_change()
        
        # Calculate cumulative returns
        df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod() - 1
        
        # Calculate rolling metrics
        df['Rolling_Volatility'] = df.groupby('Symbol')['Daily_Return'].rolling(
            window=config.analytics.rolling_window_days
        ).std().reset_index(0, drop=True)
        
        # Calculate Sharpe Ratio (simplified)
        risk_free_rate_daily = (1 + config.analytics.sharpe_ratio_risk_free_rate) ** (1/252) - 1
        df['Sharpe_Ratio'] = (df['Daily_Return'] - risk_free_rate_daily) / df['Rolling_Volatility']
        
        # Calculate maximum drawdown
        df['Peak'] = df.groupby('Symbol')['Close'].expanding().max().reset_index(0, drop=True)
        df['Drawdown'] = (df['Close'] - df['Peak']) / df['Peak']
        
        # Add metadata
        df['Processed_Date'] = datetime.now()
        df['Data_Source'] = 'Yahoo_Finance'
        
        # Clean up data
        df = df.dropna(subset=['Daily_Return'])
        
        logger.info(f"Transformed data shape: {df.shape}")
        return df
    
    def load_fund_data(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Load processed fund data to storage
        
        Args:
            df: Processed DataFrame
            filename: Optional filename for saving
            
        Returns:
            Path to saved file
        """
        if df.empty:
            logger.warning("No data to load")
            return ""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fund_data_{timestamp}.csv"
        
        filepath = os.path.join(self.config.processed_data_path, filename)
        
        try:
            df.to_csv(filepath, index=False)
            logger.info(f"Data saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return ""
    
    def generate_sample_data(self) -> pd.DataFrame:
        """
        Generate sample pension fund data for demonstration
        
        Returns:
            DataFrame with sample fund data
        """
        logger.info("Generating sample pension fund data")
        
        # Sample fund symbols (real pension fund ETFs)
        symbols = ['VTI', 'VXUS', 'BND', 'VNQ', 'GLD']  # Total Market, International, Bonds, REITs, Gold
        
        # Generate date range for the last 5 years
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5*365)
        
        # Extract real data
        df = self.extract_fund_data(
            symbols=symbols,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        
        if df.empty:
            # Fallback to synthetic data if API fails
            logger.info("API data extraction failed, generating synthetic data")
            df = self._generate_synthetic_data(symbols, start_date, end_date)
        
        return df
    
    def _generate_synthetic_data(self, symbols: List[str], start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Generate synthetic fund data for testing
        
        Args:
            symbols: List of fund symbols
            start_date: Start date
            end_date: End date
            
        Returns:
            DataFrame with synthetic data
        """
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        all_data = []
        
        for symbol in symbols:
            # Generate realistic price movements
            np.random.seed(hash(symbol) % 1000)  # Consistent seed per symbol
            
            # Base prices for different asset classes
            base_prices = {
                'VTI': 200,    # Total Market
                'VXUS': 50,    # International
                'BND': 80,     # Bonds
                'VNQ': 100,    # REITs
                'GLD': 180     # Gold
            }
            
            base_price = base_prices.get(symbol, 100)
            
            # Generate price series with realistic volatility
            returns = np.random.normal(0.0005, 0.015, len(dates))  # Daily returns
            prices = [base_price]
            
            for ret in returns[1:]:
                new_price = prices[-1] * (1 + ret)
                prices.append(max(new_price, 1))  # Ensure positive prices
            
            # Create DataFrame for this symbol
            symbol_data = pd.DataFrame({
                'Date': dates,
                'Symbol': symbol,
                'Open': prices,
                'High': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
                'Low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
                'Close': prices,
                'Volume': np.random.randint(1000000, 10000000, len(dates))
            })
            
            all_data.append(symbol_data)
        
        return pd.concat(all_data, ignore_index=True)
    
    def run_pipeline(self, symbols: List[str] = None, use_sample_data: bool = True) -> str:
        """
        Run the complete ETL pipeline
        
        Args:
            symbols: List of fund symbols to process
            use_sample_data: Whether to use sample data generation
            
        Returns:
            Path to processed data file
        """
        logger.info("Starting ETL pipeline")
        
        try:
            if use_sample_data:
                df = self.generate_sample_data()
            else:
                if not symbols:
                    raise ValueError("Symbols must be provided when not using sample data")
                
                end_date = datetime.now()
                start_date = end_date - timedelta(days=2*365)  # 2 years of data
                
                df = self.extract_fund_data(
                    symbols=symbols,
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d')
                )
            
            if df.empty:
                logger.error("No data extracted from pipeline")
                return ""
            
            # Transform data
            df_transformed = self.transform_fund_data(df)
            
            # Load data
            filepath = self.load_fund_data(df_transformed)
            
            logger.info("ETL pipeline completed successfully")
            return filepath
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {str(e)}")
            return ""

def main():
    """Main function to run the ETL pipeline"""
    etl = PensionFundETL()
    
    # Run pipeline with sample data
    result = etl.run_pipeline(use_sample_data=True)
    
    if result:
        print(f"ETL pipeline completed. Data saved to: {result}")
    else:
        print("ETL pipeline failed")

if __name__ == "__main__":
    main() 