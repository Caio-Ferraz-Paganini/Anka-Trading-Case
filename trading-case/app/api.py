from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from .backtest import run_backtest
from .strategies import MovingAverageCrossover

router = APIRouter()

class BacktestRequest(BaseModel):
    symbol: str
    start_date: str  # Format: YYYY-MM-DD
    end_date: str    # Format: YYYY-MM-DD
    initial_cash: Optional[float] = 100000.0
    fast_period: Optional[int] = 10
    slow_period: Optional[int] = 30

class BacktestResponse(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    initial_cash: float
    final_cash: float
    profit_loss: float
    profit_loss_percent: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    max_drawdown: float
    max_drawdown_percent: float
    strategy: str
    fast_period: int
    slow_period: int

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "trading-case-api"}

@router.post("/backtest", response_model=BacktestResponse)
async def execute_backtest(request: BacktestRequest):
    """Execute a backtest with Moving Average Crossover strategy"""
    try:
        # Validate date format
        try:
            start_dt = datetime.strptime(request.start_date, "%Y-%m-%d").date()
            end_dt = datetime.strptime(request.end_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Invalid date format. Use YYYY-MM-DD"
            )
        
        # Validate date range
        if start_dt >= end_dt:
            raise HTTPException(
                status_code=400,
                detail="Start date must be before end date"
            )
        
        # Validate cash amount
        if request.initial_cash <= 0:
            raise HTTPException(
                status_code=400,
                detail="Initial cash must be positive"
            )
        
        # Validate moving average periods
        if request.fast_period >= request.slow_period:
            raise HTTPException(
                status_code=400,
                detail="Fast period must be less than slow period"
            )
        
        # Run backtest
        results = await run_backtest(
            symbol=request.symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_cash=request.initial_cash,
            fast_period=request.fast_period,
            slow_period=request.slow_period
        )
        
        return BacktestResponse(**results)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Backtest execution failed: {str(e)}"
        )

@router.get("/strategies")
async def list_strategies():
    """List available trading strategies"""
    return {
        "strategies": [
            {
                "name": "MovingAverageCrossover",
                "description": "Buy when fast MA crosses above slow MA, sell when fast MA crosses below slow MA",
                "parameters": {
                    "fast_period": "Fast moving average period (default: 10)",
                    "slow_period": "Slow moving average period (default: 30)"
                }
            }
        ]
    }
