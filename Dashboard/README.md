# Pension Fund Performance Dashboard

## Power BI Dashboard Setup

This directory contains the Power BI dashboard for the Pension Fund Performance Analytics Platform.

### Dashboard Features

The Power BI dashboard includes:

1. **Performance Overview**
   - Fund performance comparison
   - Risk-adjusted return metrics
   - Rolling performance charts

2. **Risk Analysis**
   - Volatility analysis
   - Sharpe ratio trends
   - Maximum drawdown visualization
   - VaR and CVaR metrics

3. **Asset Allocation**
   - Current allocation breakdown
   - Asset class distribution
   - Diversification score
   - Optimization recommendations

4. **Anomaly Detection**
   - Anomaly alerts and notifications
   - Historical anomaly patterns
   - Risk scoring

### Setup Instructions

1. **Install Power BI Desktop**
   - Download from Microsoft Store or Power BI website
   - Install the latest version

2. **Connect to API Data Source**
   - Open Power BI Desktop
   - Go to "Get Data" → "Web"
   - Enter API endpoint: `http://localhost:8000/api/v1/fund/performance`
   - Add authentication header: `Authorization: Bearer your-token`

3. **Import Dashboard Template**
   - Open `fund_performance.pbix` (when available)
   - Update data source connections
   - Refresh data

4. **Configure Refresh Schedule**
   - Set up automatic refresh every 15 minutes
   - Configure API authentication
   - Test data connectivity

### API Endpoints for Dashboard

The dashboard connects to these API endpoints:

- `GET /api/v1/fund/performance` - Fund performance metrics
- `GET /api/v1/fund/risk-metrics` - Risk analysis
- `GET /api/v1/fund/anomalies` - Anomaly detection
- `GET /api/v1/fund/allocation` - Asset allocation data

### Dashboard Components

#### 1. Performance Metrics Cards
- Total Return
- Annualized Return
- Sharpe Ratio
- Volatility
- Maximum Drawdown

#### 2. Interactive Charts
- Performance comparison line chart
- Risk-return scatter plot
- Asset allocation pie chart
- Rolling metrics time series

#### 3. Risk Analysis Section
- VaR and CVaR metrics
- Drawdown analysis
- Volatility trends
- Correlation matrix

#### 4. Anomaly Detection Panel
- Anomaly alerts
- Risk scoring
- Historical patterns
- Alert notifications

### Customization

To customize the dashboard:

1. **Add New Metrics**
   - Modify API endpoints
   - Update Power BI data model
   - Create new visualizations

2. **Change Color Scheme**
   - Update theme settings
   - Modify conditional formatting
   - Adjust chart colors

3. **Add Filters**
   - Date range filters
   - Fund selection filters
   - Risk tolerance filters

### Troubleshooting

**Common Issues:**

1. **API Connection Failed**
   - Check if API server is running
   - Verify authentication token
   - Test endpoint connectivity

2. **Data Not Refreshing**
   - Check refresh schedule
   - Verify API response format
   - Test data source permissions

3. **Visualizations Not Loading**
   - Check data model relationships
   - Verify calculated columns
   - Test DAX formulas

### Security Considerations

- Use HTTPS for production API connections
- Implement proper authentication
- Restrict dashboard access to authorized users
- Log dashboard access and usage

### Performance Optimization

- Use incremental refresh for large datasets
- Optimize DAX queries
- Implement data compression
- Use appropriate data types

---

**Note:** The actual Power BI file (`fund_performance.pbix`) should be created using Power BI Desktop and connected to the API endpoints. This README provides the setup instructions and configuration details. 