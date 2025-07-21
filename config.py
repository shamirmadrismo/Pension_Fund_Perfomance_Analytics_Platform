"""
Configuration settings for Pension Fund Performance Analytics Platform
"""
import os
from typing import Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "5432"))
    database: str = os.getenv("DB_NAME", "pension_fund_analytics")
    username: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PASSWORD", "")
    pool_size: int = int(os.getenv("DB_POOL_SIZE", "10"))
    max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))

@dataclass
class APIConfig:
    """API configuration settings"""
    host: str = os.getenv("API_HOST", "0.0.0.0")
    port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("API_DEBUG", "False").lower() == "true"
    title: str = "Pension Fund Analytics API"
    version: str = "1.0.0"
    description: str = "REST API for Pension Fund Performance Analytics"
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Rate limiting
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))

@dataclass
class AnalyticsConfig:
    """Analytics and ML configuration settings"""
    # Risk metrics
    risk_free_rate: float = float(os.getenv("RISK_FREE_RATE", "0.02"))
    market_return: float = float(os.getenv("MARKET_RETURN", "0.08"))
    
    # Anomaly detection
    anomaly_contamination: float = float(os.getenv("ANOMALY_CONTAMINATION", "0.1"))
    anomaly_random_state: int = int(os.getenv("ANOMALY_RANDOM_STATE", "42"))
    
    # Performance calculation
    rolling_window_days: int = int(os.getenv("ROLLING_WINDOW_DAYS", "252"))
    sharpe_ratio_risk_free_rate: float = float(os.getenv("SHARPE_RATIO_RISK_FREE_RATE", "0.02"))
    
    # Asset allocation
    max_allocation_per_asset: float = float(os.getenv("MAX_ALLOCATION_PER_ASSET", "0.25"))
    min_allocation_per_asset: float = float(os.getenv("MIN_ALLOCATION_PER_ASSET", "0.05"))

@dataclass
class ETLConfig:
    """ETL pipeline configuration settings"""
    data_source_url: str = os.getenv("DATA_SOURCE_URL", "")
    data_refresh_interval_hours: int = int(os.getenv("DATA_REFRESH_INTERVAL_HOURS", "24"))
    batch_size: int = int(os.getenv("BATCH_SIZE", "1000"))
    
    # File paths
    data_directory: str = os.getenv("DATA_DIRECTORY", "data")
    processed_data_path: str = os.getenv("PROCESSED_DATA_PATH", "data/processed")
    raw_data_path: str = os.getenv("RAW_DATA_PATH", "data/raw")

@dataclass
class DashboardConfig:
    """Dashboard configuration settings"""
    refresh_interval_seconds: int = int(os.getenv("DASHBOARD_REFRESH_INTERVAL", "300"))
    max_data_points: int = int(os.getenv("MAX_DATA_POINTS", "1000"))
    
    # Power BI settings
    powerbi_workspace_id: str = os.getenv("POWERBI_WORKSPACE_ID", "")
    powerbi_client_id: str = os.getenv("POWERBI_CLIENT_ID", "")
    powerbi_client_secret: str = os.getenv("POWERBI_CLIENT_SECRET", "")

@dataclass
class LoggingConfig:
    """Logging configuration settings"""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = os.getenv("LOG_FILE_PATH", "logs/app.log")
    max_file_size_mb: int = int(os.getenv("LOG_MAX_FILE_SIZE_MB", "10"))
    backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))

class Config:
    """Main configuration class"""
    def __init__(self):
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.analytics = AnalyticsConfig()
        self.etl = ETLConfig()
        self.dashboard = DashboardConfig()
        self.logging = LoggingConfig()
    
    def get_database_url(self) -> str:
        """Generate database URL for SQLAlchemy"""
        return f"postgresql://{self.database.username}:{self.database.password}@{self.database.host}:{self.database.port}/{self.database.database}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for API responses"""
        return {
            "database": self.database.__dict__,
            "api": self.api.__dict__,
            "analytics": self.analytics.__dict__,
            "etl": self.etl.__dict__,
            "dashboard": self.dashboard.__dict__,
            "logging": self.logging.__dict__
        }

# Global config instance
config = Config() 