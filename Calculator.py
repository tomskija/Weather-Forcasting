#!/usr/bin/env python3
"""
FastAPI application for Weather Forecasting Calculator
Provides REST API endpoints for the Calculator.py functionality
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import sys
from datetime import datetime
import logging

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import your Calculator module
try:
    from weatherForcastingCalculator.Calculator import *
except ImportError as e:
    print(f"Warning: Could not import Calculator module: {e}")
    print("API will run with mock responses")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Weather Forecasting Calculator API",
    description="REST API for advanced weather forecasting and climate analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for UI-Workspace integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # UI-Workspace local development
        "https://ui-workspace-tomskija.vercel.app",  # Production UI
        "https://staging-ui-workspace.tomskija.dev",  # Staging UI
        "*"  # Allow all origins for development (restrict in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class WeatherLocation(BaseModel):
    city: str
    country: str
    coordinates: List[float]  # [latitude, longitude]
    region: Optional[str] = None
    timezone: Optional[str] = None

class CurrentWeather(BaseModel):
    temperature: float  # Celsius
    humidity: float  # Percentage
    pressure: float  # hPa
    wind_speed: float  # m/s
    wind_direction: Optional[float] = None  # degrees
    conditions: str
    description: Optional[str] = None
    icon: Optional[str] = None
    visibility: Optional[float] = None  # km
    uv_index: Optional[float] = None
    feels_like: Optional[float] = None  # Celsius

class WeatherForecast(BaseModel):
    date: str  # ISO date string
    high: float  # Celsius
    low: float  # Celsius
    conditions: str
    precipitation_chance: float  # Percentage
    precipitation_mm: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    icon: Optional[str] = None

class WeatherResponse(BaseModel):
    location: WeatherLocation
    current: CurrentWeather
    forecast: Optional[List[WeatherForecast]] = None
    last_updated: str
    source: Optional[str] = "Weather-Forecasting Calculator"
    model_version: Optional[str] = "1.0.0"

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    uptime: Optional[float] = None

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Weather Forecasting Calculator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        uptime=0.0  # You can implement actual uptime tracking
    )

@app.get("/weather/current", response_model=WeatherResponse, tags=["Weather"])
async def get_current_weather(location: str = Query(..., description="City name or coordinates")):
    """Get current weather conditions for a location"""
    try:
        # This is where you'd integrate with your Calculator.py
        # For now, returning mock data structure
        
        # Example integration (adjust based on your Calculator.py):
        # weather_data = get_current_weather_from_calculator(location)
        
        # Mock response for testing
        mock_response = WeatherResponse(
            location=WeatherLocation(
                city=location,
                country="Unknown",
                coordinates=[0.0, 0.0]
            ),
            current=CurrentWeather(
                temperature=22.5,
                humidity=65.0,
                pressure=1013.25,
                wind_speed=3.2,
                conditions="partly cloudy"
            ),
            last_updated=datetime.now().isoformat()
        )
        
        logger.info(f"Current weather requested for: {location}")
        return mock_response
        
    except Exception as e:
        logger.error(f"Error getting current weather for {location}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/forecast", response_model=WeatherResponse, tags=["Weather"])
async def get_weather_forecast(
    location: str = Query(..., description="City name or coordinates"),
    days: int = Query(7, description="Number of days to forecast (1-7)", ge=1, le=7)
):
    """Get weather forecast for a location"""
    try:
        # Integrate with your Calculator.py forecast functionality
        # forecast_data = get_forecast_from_calculator(location, days)
        
        # Mock forecast data
        mock_forecasts = []
        for i in range(days):
            date = datetime.now().date()
            # Add i days to current date
            forecast_date = date.replace(day=date.day + i)
            
            mock_forecasts.append(WeatherForecast(
                date=forecast_date.isoformat(),
                high=25.0 + i,
                low=15.0 + i,
                conditions="sunny",
                precipitation_chance=10.0
            ))
        
        mock_response = WeatherResponse(
            location=WeatherLocation(
                city=location,
                country="Unknown", 
                coordinates=[0.0, 0.0]
            ),
            current=CurrentWeather(
                temperature=22.5,
                humidity=65.0,
                pressure=1013.25,
                wind_speed=3.2,
                conditions="partly cloudy"
            ),
            forecast=mock_forecasts,
            last_updated=datetime.now().isoformat()
        )
        
        logger.info(f"Weather forecast requested for: {location}, days: {days}")
        return mock_response
        
    except Exception as e:
        logger.error(f"Error getting forecast for {location}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/alerts", tags=["Weather"])
async def get_weather_alerts(location: str = Query(..., description="City name or coordinates")):
    """Get weather alerts for a location"""
    try:
        # Integrate with your Calculator.py alert functionality
        # alerts_data = get_alerts_from_calculator(location)
        
        # Mock response
        logger.info(f"Weather alerts requested for: {location}")
        return []  # No alerts for mock response
        
    except Exception as e:
        logger.error(f"Error getting alerts for {location}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENV") == "development",
        log_level="info"
    )