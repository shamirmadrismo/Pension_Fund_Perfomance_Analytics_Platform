# Pension Fund Performance Analytics Platform

🎯 **Purpose**: Pension managers need transparent, actionable insights into fund performance. This project delivers:

- Fund performance KPIs
- Advanced risk-return metrics  
- Asset allocation optimization suggestions
- Automated anomaly detection in returns

🌟 **Highlights**:

- Python ETL pipeline
- Power BI dashboard
- Anomaly detection with Isolation Forest
- SaaS-style REST API to serve fund metrics

## 🏗️ Project Structure

```
fund-analytics-platform/
├── etl/
│   └── pipeline.py
├── analytics/
│   └── risk_metrics.py
├── api/
│   └── app.py (FastAPI)
├── dashboard/
│   └── fund_performance.pbix
├── data/
│   └── fund_returns.csv
├── requirements.txt
├── config.py
└── README.md
```

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run ETL Pipeline**:
   ```bash
   python etl/pipeline.py
   ```

3. **Start API Server**:
   ```bash
   python api/app.py
   ```

4. **Access Dashboard**:
   - Open `dashboard/fund_performance.pbix` in Power BI Desktop
   - Connect to the API endpoints for live data

## 📊 Features

### ✅ Machine Learning for Anomaly Detection
- Isolation Forest algorithm for detecting unusual return patterns
- Configurable sensitivity parameters
- Real-time alerting system

### ✅ REST API for Consumption
- FastAPI-based RESTful endpoints
- JSON responses with comprehensive fund metrics
- Authentication and rate limiting
- Swagger documentation at `/docs`

### ✅ Business-Grade Visual Storytelling
- Interactive Power BI dashboards
- Real-time performance monitoring
- Risk-adjusted return visualizations
- Asset allocation heatmaps

## 🔧 Configuration

Edit `config.py` to customize:
- Database connections
- API settings
- Anomaly detection parameters
- Dashboard refresh intervals

## 📈 API Endpoints

- `GET /api/v1/fund/performance` - Fund performance metrics
- `GET /api/v1/fund/risk-metrics` - Risk analysis
- `GET /api/v1/fund/anomalies` - Anomaly detection results
- `GET /api/v1/fund/allocation` - Asset allocation data

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Quality
```bash
flake8 .
black .
```

## 📝 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ for pension fund managers worldwide** 