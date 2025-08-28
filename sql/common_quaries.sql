-- Common queries for weather forecasting application
-- These queries can be used in your Python application

-- 1. Get current weather conditions for all active stations
SELECT 
    ws.station_code,
    ws.station_name,
    ws.city,
    ws.state_province,
    wd.temperature_c,
    wd.humidity_percent,
    wd.pressure_hpa,
    wd.wind_speed_ms,
    wd.wind_direction_deg,
    wd.precipitation_mm,
    wd.weather_condition,
    wd.recorded_at
FROM weather_stations ws
JOIN weather_data wd ON ws.id = wd.station_id
WHERE ws.is_active = true
    AND wd.recorded_at = (
        SELECT MAX(recorded_at) 
        FROM weather_data wd2 
        WHERE wd2.station_id = ws.id
    )
ORDER BY ws.station_name;

-- 2. Get 5-day forecast for a specific station
SELECT 
    ws.station_name,
    wf.forecast_date,
    wf.forecast_hour,
    wf.temperature_c,
    wf.humidity_percent,
    wf.precipitation_mm,
    wf.precipitation_probability,
    wf.weather_condition,
    wf.confidence_score
FROM weather_forecasts wf
JOIN weather_stations ws ON wf.station_id = ws.id
WHERE ws.station_code = 'NYC001'
    AND wf.forecast_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '5 days'
    AND wf.predicted_at = (
        SELECT MAX(predicted_at)
        FROM weather_forecasts wf2
        WHERE wf2.station_id = wf.station_id
            AND wf2.forecast_date = wf.forecast_date
            AND wf2.forecast_hour = wf.forecast_hour
    )
ORDER BY wf.forecast_date, wf.forecast_hour;

-- 3. Get historical temperature trends (last 30 days)
SELECT 
    ws.station_name,
    DATE(wd.recorded_at) as date,
    ROUND(AVG(wd.temperature_c), 2) as avg_temp,
    ROUND(MIN(wd.temperature_c), 2) as min_temp,
    ROUND(MAX(wd.temperature_c), 2) as max_temp
FROM weather_data wd
JOIN weather_stations ws ON wd.station_id = ws.id
WHERE wd.recorded_at >= CURRENT_DATE - INTERVAL '30 days'
    AND ws.station_code = 'NYC001'
GROUP BY ws.station_name, DATE(wd.recorded_at)
ORDER BY date;

-- 4. Find stations within a geographic radius (50km from a point)
-- Using Haversine formula approximation
SELECT 
    station_code,
    station_name,
    city,
    state_province,
    latitude,
    longitude,
    ROUND(
        6371 * acos(
            cos(radians(40.7589)) -- Target latitude (NYC)
            * cos(radians(latitude))
            * cos(radians(longitude) - radians(-73.9851)) -- Target longitude (NYC)
            + sin(radians(40.7589))
            * sin(radians(latitude))
        ), 2
    ) as distance_km
FROM weather_stations
WHERE is_active = true
HAVING distance_km <= 50
ORDER BY distance_km;

-- 5. Get active weather alerts for specific stations
SELECT 
    ws.station_name,
    wa.alert_type,
    wa.severity,
    wa.title,
    wa.description,
    wa.start_time,
    wa.end_time,
    CASE 
        WHEN wa.end_time < CURRENT_TIMESTAMP THEN 'Expired'
        WHEN wa.start_time > CURRENT_TIMESTAMP THEN 'Scheduled'
        ELSE 'Active'
    END as status
FROM weather_alerts wa
JOIN weather_stations ws ON wa.station_id = ws.id
WHERE wa.is_active = true
    AND ws.station_code IN ('NYC001', 'CHI001', 'LAX001')
ORDER BY wa.severity DESC, wa.start_time;

-- 6. Calculate forecast accuracy for the last month
SELECT 
    ws.station_name,
    fa.model_version,
    COUNT(*) as total_forecasts,
    ROUND(AVG(ABS(fa.temperature_error)), 2) as avg_temp_error,
    ROUND(AVG(ABS(fa.precipitation_error)), 2) as avg_precip_error,
    ROUND(
        (COUNT(CASE WHEN ABS(fa.temperature_error) <= 2.0 THEN 1 END) * 100.0) / COUNT(*), 
        2
    ) as temp_accuracy_within_2c
FROM forecast_accuracy fa
JOIN weather_stations ws ON fa.station_id = ws.id
WHERE fa.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY ws.station_name, fa.model_version
ORDER BY avg_temp_error;

-- 7. Get weather statistics by season (last year)
SELECT 
    ws.station_name,
    CASE 
        WHEN EXTRACT(MONTH FROM wd.recorded_at) IN (12, 1, 2) THEN 'Winter'
        WHEN EXTRACT(MONTH FROM wd.recorded_at) IN (3, 4, 5) THEN 'Spring'
        WHEN EXTRACT(MONTH FROM wd.recorded_at) IN (6, 7, 8) THEN 'Summer'
        ELSE 'Fall'
    END as season,
    ROUND(AVG(wd.temperature_c), 2) as avg_temperature,
    ROUND(AVG(wd.humidity_percent), 2) as avg_humidity,
    ROUND(SUM(wd.precipitation_mm), 2) as total_precipitation,
    COUNT(*) as measurement_count
FROM weather_data wd
JOIN weather_stations ws ON wd.station_id = ws.id
WHERE wd.recorded_at >= CURRENT_DATE - INTERVAL '1 year'
    AND ws.station_code = 'NYC001'
GROUP BY ws.station_name, season
ORDER BY 
    CASE season
        WHEN 'Winter' THEN 1
        WHEN 'Spring' THEN 2
        WHEN 'Summer' THEN 3
        WHEN 'Fall' THEN 4
    END;

-- 8. Find extreme weather events
SELECT 
    ws.station_name,
    wd.recorded_at,
    wd.temperature_c,
    wd.precipitation_mm,
    wd.wind_speed_ms,
    wd.weather_condition,
    CASE
        WHEN wd.temperature_c > 40 THEN 'Extreme Heat'
        WHEN wd.temperature_c < -20 THEN 'Extreme Cold'
        WHEN wd.precipitation_mm > 50 THEN 'Heavy Precipitation'
        WHEN wd.wind_speed_ms > 20 THEN 'Strong Wind'
        ELSE 'Normal'
    END as event_type
FROM weather_data wd
JOIN weather_stations ws ON wd.station_id = ws.id
WHERE (wd.temperature_c > 40 OR wd.temperature_c < -20 
       OR wd.precipitation_mm > 50 OR wd.wind_speed_ms > 20)
    AND wd.recorded_at >= CURRENT_DATE - INTERVAL '90 days'
ORDER BY wd.recorded_at DESC;

-- 9. Get user's preferred stations current weather
SELECT 
    ws.station_name,
    ws.city,
    wd.temperature_c,
    wd.humidity_percent,
    wd.weather_condition,
    wd.recorded_at,
    up.temperature_unit,
    up.wind_speed_unit
FROM user_preferences up
CROSS JOIN UNNEST(up.preferred_stations) AS station_id
JOIN weather_stations ws ON ws.id = station_id
JOIN weather_data wd ON ws.id = wd.station_id
WHERE up.user_id = 'user_001'
    AND wd.recorded_at = (
        SELECT MAX(recorded_at) 
        FROM weather_data wd2 
        WHERE wd2.station_id = ws.id
    )
ORDER BY ws.station_name;

-- 10. Maintenance queries

-- Clean up old forecast data (older than 7 days)
DELETE FROM weather_forecasts 
WHERE predicted_at < CURRENT_TIMESTAMP - INTERVAL '7 days';

-- Update weather station last activity
UPDATE weather_stations 
SET updated_at = CURRENT_TIMESTAMP 
WHERE id IN (
    SELECT DISTINCT station_id 
    FROM weather_data 
    WHERE recorded_at > CURRENT_TIMESTAMP - INTERVAL '24 hours'
);

-- Archive old weather alerts
UPDATE weather_alerts 
SET is_active = false 
WHERE end_time < CURRENT_TIMESTAMP - INTERVAL '7 days' 
    AND is_active = true;