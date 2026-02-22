"""
Demand Forecaster - Predicts product demand trends using time series analysis
"""

import pandas as pd
from typing import Dict


class DemandForecaster:
    """
    Predicts product demand trends using time series analysis.
    """
    
    def forecast(self, transaction_history: pd.DataFrame, days_ahead: int = 30) -> Dict:
        """
        Analyzes demand trends and predicts future volume.
        
        Returns:
            {
                "trend": str (HIGH/MEDIUM/LOW),
                "growth_rate": float,
                "predicted_next_30_days": int,
                "seasonality": str,
                "confidence": str
            }
        """
        if transaction_history.empty:
            return self._no_data_response()
        
        # Prepare time series
        df = transaction_history.copy()
        df = df.set_index('date').resample('D')['quantity'].sum().fillna(0)
        
        # Calculate moving averages
        ma_7 = df.rolling(window=7, min_periods=1).mean()
        ma_30 = df.rolling(window=30, min_periods=1).mean()
        
        # Growth rate (compare recent vs previous period)
        current_avg = ma_7.iloc[-7:].mean() if len(ma_7) >= 7 else df.mean()
        previous_avg = ma_7.iloc[-14:-7].mean() if len(ma_7) >= 14 else current_avg
        
        growth_rate = ((current_avg - previous_avg) / previous_avg) if previous_avg > 0 else 0
        
        # Classify trend
        if growth_rate > 0.15:
            trend = "HIGH"
        elif growth_rate < -0.15:
            trend = "LOW"
        else:
            trend = "MEDIUM"
        
        # Predict next 30 days
        predicted_daily = ma_30.iloc[-1] if len(ma_30) > 0 else df.mean()
        predicted_volume = int(predicted_daily * days_ahead)
        
        # Seasonality detection
        seasonality = self._detect_seasonality(df)
        
        # Confidence
        confidence = "High" if len(df) > 60 else ("Medium" if len(df) > 30 else "Low")
        
        return {
            "trend": trend,
            "growth_rate": round(growth_rate, 3),
            "predicted_next_30_days": max(0, predicted_volume),
            "current_avg_daily_sales": round(current_avg, 2),
            "seasonality": seasonality,
            "confidence": confidence
        }
    
    def _detect_seasonality(self, series: pd.Series) -> str:
        """
        Simple seasonality detection using autocorrelation.
        Checks for weekly (7-day) patterns.
        """
        if len(series) < 28:  # Need at least 4 weeks
            return "Insufficient data"
        
        try:
            # Calculate autocorrelation at lag 7 (weekly pattern)
            try:
                from scipy.stats import pearsonr
            except ImportError:
                return "No clear pattern (scipy not available)"
            
            lag = 7
            if len(series) >= lag * 2:
                correlation, _ = pearsonr(series[:-lag], series[lag:])
                if abs(correlation) > 0.5:
                    return "Weekly pattern detected"
        except Exception as e:
            print(f"Seasonality detection error: {e}")
        
        return "No clear pattern"
    
    def _no_data_response(self) -> Dict:
        """Response when no transaction data is available"""
        return {
            "trend": "UNKNOWN",
            "growth_rate": 0.0,
            "predicted_next_30_days": 0,
            "current_avg_daily_sales": 0.0,
            "seasonality": "No data",
            "confidence": "None"
        }
