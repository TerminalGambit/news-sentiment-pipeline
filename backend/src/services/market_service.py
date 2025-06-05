"""
Market data and technical indicators service.
"""
from typing import Dict, Any, List, Optional
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ..utils.logger import get_logger

logger = get_logger(__name__)

class MarketService:
    """Service for handling market data and technical indicators."""
    
    def __init__(self):
        """Initialize the market service."""
        self.symbols = ["BTC-USD", "ETH-USD"]  # Add more symbols as needed
        self.timeframes = {
            "1d": "1d",
            "1w": "1w",
            "1m": "1mo",
            "3m": "3mo",
            "6m": "6mo",
            "1y": "1y",
            "5y": "5y",
            "max": "max"
        }
    
    def get_market_data(
        self,
        symbol: str,
        timeframe: str = "1mo",
        period: str = "1y"
    ) -> Optional[Dict[str, Any]]:
        """
        Get market data for a symbol.
        
        Args:
            symbol: Trading symbol
            timeframe: Data timeframe
            period: Data period
            
        Returns:
            Dict containing market data and indicators
        """
        try:
            # Get data from Yahoo Finance
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=timeframe)
            
            if df.empty:
                return None
            
            # Calculate technical indicators
            df = self._calculate_indicators(df)
            
            # Convert to dict format
            data = {
                "dates": df.index.strftime("%Y-%m-%d").tolist(),
                "prices": df["Close"].round(2).tolist(),
                "volumes": df["Volume"].round(0).tolist(),
                "sma_20": df["SMA_20"].round(2).tolist(),
                "sma_50": df["SMA_50"].round(2).tolist(),
                "rsi": df["RSI"].round(2).tolist(),
                "macd": df["MACD"].round(2).tolist(),
                "macd_signal": df["MACD_Signal"].round(2).tolist(),
                "macd_hist": df["MACD_Hist"].round(2).tolist(),
            }
            
            # Add metadata
            data["metadata"] = {
                "symbol": symbol,
                "timeframe": timeframe,
                "period": period,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "current_price": df["Close"].iloc[-1],
                "price_change_24h": self._calculate_price_change(df),
                "volume_24h": df["Volume"].iloc[-1],
            }
            
            return data
        except Exception as e:
            logger.error(f"Error getting market data for {symbol}: {str(e)}")
            raise
    
    def get_market_overview(self) -> Dict[str, Any]:
        """
        Get market overview for all symbols.
        
        Returns:
            Dict containing market overview data
        """
        try:
            overview = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "symbols": {}
            }
            
            for symbol in self.symbols:
                data = self.get_market_data(symbol, timeframe="1d", period="1mo")
                if data:
                    overview["symbols"][symbol] = {
                        "current_price": data["metadata"]["current_price"],
                        "price_change_24h": data["metadata"]["price_change_24h"],
                        "volume_24h": data["metadata"]["volume_24h"],
                        "rsi": data["rsi"][-1],
                        "macd": data["macd"][-1],
                        "macd_signal": data["macd_signal"][-1],
                        "macd_hist": data["macd_hist"][-1],
                    }
            
            return overview
        except Exception as e:
            logger.error(f"Error getting market overview: {str(e)}")
            raise
    
    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical indicators.
        
        Args:
            df: Price DataFrame
            
        Returns:
            DataFrame with added indicators
        """
        # Simple Moving Averages
        df["SMA_20"] = df["Close"].rolling(window=20).mean()
        df["SMA_50"] = df["Close"].rolling(window=50).mean()
        
        # Relative Strength Index (RSI)
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df["Close"].ewm(span=12, adjust=False).mean()
        exp2 = df["Close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = exp1 - exp2
        df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
        df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
        
        return df
    
    def _calculate_price_change(self, df: pd.DataFrame) -> float:
        """
        Calculate 24-hour price change.
        
        Args:
            df: Price DataFrame
            
        Returns:
            Price change percentage
        """
        if len(df) < 2:
            return 0.0
        
        current_price = df["Close"].iloc[-1]
        previous_price = df["Close"].iloc[-2]
        return round(((current_price - previous_price) / previous_price) * 100, 2) 