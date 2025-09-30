import backtrader as bt

class MovingAverageCrossover(bt.Strategy):
    """Moving Average Crossover Strategy
    
    Buy signal: Fast MA crosses above Slow MA
    Sell signal: Fast MA crosses below Slow MA
    """
    
    params = (
        ('fast_period', 10),
        ('slow_period', 30),
        ('printlog', False),
    )
    
    def log(self, txt, dt=None, doprint=False):
        """Logging function for this strategy"""
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')
    
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        # Add moving average indicators
        self.sma_fast = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.fast_period
        )
        self.sma_slow = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.slow_period
        )
        
        # Create crossover signal
        self.crossover = bt.indicators.CrossOver(
            self.sma_fast, self.sma_slow
        )
    
    def notify_order(self, order):
        """Notify when order is submitted/accepted/executed"""
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        
        # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'BUY EXECUTED, Price: {order.executed.price:.2f}, '
                    f'Cost: {order.executed.value:.2f}, '
                    f'Comm: {order.executed.comm:.2f}'
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log(
                    f'SELL EXECUTED, Price: {order.executed.price:.2f}, '
                    f'Cost: {order.executed.value:.2f}, '
                    f'Comm: {order.executed.comm:.2f}'
                )
            
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        
        # Write down: no pending order
        self.order = None
    
    def notify_trade(self, trade):
        """Notify when trade is closed"""
        if not trade.isclosed:
            return
        
        self.log(
            f'OPERATION PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}'
        )
    
    def next(self):
        """Main strategy logic"""
        # Simply log the closing price of the series from the reference
        self.log(f'Close, {self.dataclose[0]:.2f}')
        
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        
        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if conditions are met
            if self.crossover[0] > 0:  # Fast MA crossed above Slow MA
                self.log(f'BUY CREATE, {self.dataclose[0]:.2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        else:
            # Already in the market ... we might sell
            if self.crossover[0] < 0:  # Fast MA crossed below Slow MA
                self.log(f'SELL CREATE, {self.dataclose[0]:.2f}')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
    
    def stop(self):
        """Called when backtest ends"""
        self.log(
            f'(MA Period {self.params.fast_period}/{self.params.slow_period}) '
            f'Ending Value {self.broker.getvalue():.2f}',
            doprint=True
        )

class BuyAndHold(bt.Strategy):
    """Simple Buy and Hold Strategy for comparison"""
    
    params = (
        ('printlog', False),
    )
    
    def log(self, txt, dt=None, doprint=False):
        """Logging function for this strategy"""
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')
    
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.bought = False
    
    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'BUY EXECUTED, Price: {order.executed.price:.2f}'
                )
                self.bought = True
        self.order = None
    
    def next(self):
        if not self.bought and not self.order:
            self.log(f'BUY CREATE, {self.dataclose[0]:.2f}')
            self.order = self.buy()
    
    def stop(self):
        self.log(
            f'(Buy and Hold) Ending Value {self.broker.getvalue():.2f}',
            doprint=True
        )
