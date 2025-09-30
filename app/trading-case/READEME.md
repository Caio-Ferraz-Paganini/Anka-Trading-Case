# Trading Case API

A REST API for trading backtests using FastAPI and Backtrader.

## Features

- **Moving Average Crossover Strategy**: Implement buy/sell signals based on fast and slow moving average crossovers
- **Historical Data**: Fetch historical stock data from Yahoo Finance using yfinance
- **Performance Metrics**: Calculate key metrics including P&L, drawdown, and trade statistics
- **REST API**: Clean FastAPI endpoints for executing backtests

## Quick Start

1. **Install Dependencies**:
   ```bash
   cd trading-case
   pip install -r requirements.txt
   ```

2. **Run the API**:
   ```bash
   python main.py
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/api/health

## API Endpoints

### POST /api/backtest

Execute a backtest with Moving Average Crossover strategy.

**Request Body**:
```json
{
  "symbol": "AAPL",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "initial_cash": 100000.0,
  "fast_period": 10,
  "slow_period": 30
}
```

**Response**:
```json
{
  "symbol": "AAPL",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "initial_cash": 100000.0,
  "final_cash": 105000.0,
  "profit_loss": 5000.0,
  "profit_loss_percent": 5.0,
  "total_trades": 15,
  "winning_trades": 9,
  "losing_trades": 6,
  "max_drawdown": 2500.0,
  "max_drawdown_percent": 2.5,
  "strategy": "MovingAverageCrossover",
  "fast_period": 10,
  "slow_period": 30
}
```

### GET /api/strategies

List available trading strategies and their parameters.

### GET /api/health

Health check endpoint.

## Project Structure

```
trading-case/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── app/
    ├── __init__.py     # Package initialization
    ├── api.py          # REST API endpoints
    ├── backtest.py     # Backtest execution logic
    └── strategies.py   # Trading strategies implementation
```

## Strategy Details

### Moving Average Crossover

- **Buy Signal**: When fast MA crosses above slow MA
- **Sell Signal**: When fast MA crosses below slow MA
- **Parameters**:
  - `fast_period`: Fast moving average period (default: 10)
  - `slow_period`: Slow moving average period (default: 30)

## Example Usage

```bash
# Test AAPL stock with default parameters
curl -X POST "http://localhost:8000/api/backtest" \
     -H "Content-Type: application/json" \
     -d '{
       "symbol": "AAPL",
       "start_date": "2023-01-01",
       "end_date": "2023-12-31",
       "initial_cash": 100000.0,
       "fast_period": 10,
       "slow_period": 30
     }'
```

## Future Enhancements

- [ ] Database persistence for backtest results
- [ ] Additional trading strategies (RSI, MACD, Bollinger Bands)
- [ ] Portfolio optimization
- [ ] Real-time data feeds
- [ ] Web frontend interface
- [ ] Risk management features
- [ ] Multi-asset backtesting
- [ ] Performance visualization charts
- [ ] Strategy parameter optimization

## Dependencies

- **FastAPI**: Modern web framework for APIs
- **Backtrader**: Backtesting library for trading strategies
- **yfinance**: Yahoo Finance data downloader
- **Uvicorn**: ASGI server for FastAPI
- **Pandas**: Data manipulation library
- **NumPy**: Numerical computing library