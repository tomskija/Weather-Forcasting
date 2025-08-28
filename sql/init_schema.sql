-- Weather Forecasting Database Schema
-- Initialize database structure for weather data storage and forecasting

-- Create database (PostgreSQL syntax)
-- CREATE DATABASE weather_forecast_db;

-- Weather stations table
CREATE TABLE IF NOT EXISTS weather_stations (
    id SERIAL PRIMARY KEY,
    station_code VARCHAR(20) UNIQUE NOT NULL,
    station_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    elevation_m INTEGER,
    country VARCHAR(3) NOT NULL,
    state_province VARCHAR(100),
    city VARCHAR(100),
    timezone VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Historical weather data
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES weather_stations(id) ON DELETE CASCADE,
    recorded_at TIMESTAMP NOT NULL,
    temperature_c DECIMAL(5, 2),
    humidity_percent DECIMAL(5, 2),
    pressure_hpa DECIMAL(7, 2),
    wind_speed_ms DECIMAL(5, 2),
    wind_direction_deg INTEGER,
    precipitation_mm DECIMAL(6, 2),
    visibility_km DECIMAL(5, 2),
    cloud_cover_percent INTEGER,
    weather_condition VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(station_id, recorded_at)
);

-- Forecast predictions
CREATE TABLE IF NOT EXISTS weather_forecasts (
    id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES weather_stations(id) ON DELETE CASCADE,
    forecast_date DATE NOT NULL,
    forecast_hour INTEGER NOT NULL, -- 0-23 for hourly forecasts
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    temperature_c DECIMAL(5, 2),
    humidity_percent DECIMAL(5, 2),
    pressure_hpa DECIMAL(7, 2),
    wind_speed_ms DECIMAL(5, 2),
    wind_direction_deg INTEGER,
    precipitation_mm DECIMAL(6, 2),
    precipitation_probability DECIMAL(5, 2),
    weather_condition VARCHAR(100),
    confidence_score DECIMAL(3, 2), -- 0.00 to 1.00
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(station_id, forecast_date, forecast_hour, predicted_at)
);

-- Model performance tracking
CREATE TABLE IF NOT EXISTS forecast_accuracy (
    id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES weather_stations(id) ON DELETE CASCADE,
    forecast_date DATE NOT NULL,
    forecast_hour INTEGER NOT NULL,
    predicted_temperature DECIMAL(5, 2),
    actual_temperature DECIMAL(5, 2),
    temperature_error DECIMAL(5, 2),
    predicted_precipitation DECIMAL(6, 2),
    actual_precipitation DECIMAL(6, 2),
    precipitation_error DECIMAL(6, 2),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Weather alerts and warnings
CREATE TABLE IF NOT EXISTS weather_alerts (
    id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES weather_stations(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL, -- 'extreme_temp', 'heavy_rain', 'strong_wind', etc.
    severity VARCHAR(20) NOT NULL, -- 'low', 'medium', 'high', 'critical'
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User preferences (if supporting multiple users)
CREATE TABLE IF NOT EXISTS user_preferences (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    preferred_stations INTEGER[] DEFAULT '{}',
    temperature_unit VARCHAR(10) DEFAULT 'celsius', -- 'celsius', 'fahrenheit'
    wind_speed_unit VARCHAR(10) DEFAULT 'ms', -- 'ms', 'kmh', 'mph'
    pressure_unit VARCHAR(10) DEFAULT 'hpa', -- 'hpa', 'mmhg', 'inhg'
    timezone VARCHAR(50) DEFAULT 'UTC',
    alert_preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_weather_data_station_time ON weather_data(station_id, recorded_at);
CREATE INDEX IF NOT EXISTS idx_weather_data_recorded_at ON weather_data(recorded_at);
CREATE INDEX IF NOT EXISTS idx_weather_forecasts_station_date ON weather_forecasts(station_id, forecast_date);
CREATE INDEX IF NOT EXISTS idx_weather_forecasts_predicted_at ON weather_forecasts(predicted_at);
CREATE INDEX IF NOT EXISTS idx_weather_stations_location ON weather_stations(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_weather_alerts_active ON weather_alerts(is_active, start_time, end_time);
CREATE INDEX IF NOT EXISTS idx_forecast_accuracy_station_date ON forecast_accuracy(station_id, forecast_date);