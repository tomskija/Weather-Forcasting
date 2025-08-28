-- Seed data for weather forecasting application
-- Insert sample data for development and testing

-- Insert sample weather stations
INSERT INTO weather_stations (station_code, station_name, latitude, longitude, elevation_m, country, state_province, city, timezone) VALUES
('NYC001', 'New York Central Park', 40.7829, -73.9654, 42, 'USA', 'New York', 'New York', 'America/New_York'),
('LAX001', 'Los Angeles International', 33.9425, -118.4081, 38, 'USA', 'California', 'Los Angeles', 'America/Los_Angeles'),
('CHI001', 'Chicago O''Hare', 41.9742, -87.9073, 201, 'USA', 'Illinois', 'Chicago', 'America/Chicago'),
('MIA001', 'Miami International', 25.7959, -80.2870, 3, 'USA', 'Florida', 'Miami', 'America/New_York'),
('DEN001', 'Denver International', 39.8561, -104.6737, 1640, 'USA', 'Colorado', 'Denver', 'America/Denver'),
('SEA001', 'Seattle-Tacoma International', 47.4502, -122.3088, 131, 'USA', 'Washington', 'Seattle', 'America/Los_Angeles'),
('ATL001', 'Atlanta Hartsfield-Jackson', 33.6407, -84.4277, 308, 'USA', 'Georgia', 'Atlanta', 'America/New_York'),
('PHX001', 'Phoenix Sky Harbor', 33.4352, -112.0101, 337, 'USA', 'Arizona', 'Phoenix', 'America/Phoenix')
ON CONFLICT (station_code) DO NOTHING;

-- Insert sample historical weather data (last 7 days)
INSERT INTO weather_data (station_id, recorded_at, temperature_c, humidity_percent, pressure_hpa, wind_speed_ms, wind_direction_deg, precipitation_mm, visibility_km, cloud_cover_percent, weather_condition) VALUES
-- New York data
(1, CURRENT_TIMESTAMP - INTERVAL '6 days', 18.5, 65.0, 1013.25, 3.2, 180, 0.0, 10.0, 25, 'Clear'),
(1, CURRENT_TIMESTAMP - INTERVAL '5 days', 22.1, 58.0, 1015.50, 2.8, 200, 0.0, 15.0, 15, 'Clear'),
(1, CURRENT_TIMESTAMP - INTERVAL '4 days', 19.8, 72.0, 1010.75, 4.1, 220, 2.5, 8.0, 80, 'Light Rain'),
(1, CURRENT_TIMESTAMP - INTERVAL '3 days', 16.2, 85.0, 1008.25, 5.5, 240, 8.2, 5.0, 95, 'Heavy Rain'),
(1, CURRENT_TIMESTAMP - INTERVAL '2 days', 20.5, 68.0, 1012.00, 3.8, 160, 0.0, 12.0, 40, 'Partly Cloudy'),
(1, CURRENT_TIMESTAMP - INTERVAL '1 day', 23.8, 55.0, 1016.25, 2.1, 140, 0.0, 16.0, 20, 'Clear'),
(1, CURRENT_TIMESTAMP, 25.2, 52.0, 1018.50, 1.9, 120, 0.0, 18.0, 10, 'Clear'),

-- Los Angeles data
(2, CURRENT_TIMESTAMP - INTERVAL '6 days', 24.8, 45.0, 1015.00, 2.1, 270, 0.0, 20.0, 5, 'Clear'),
(2, CURRENT_TIMESTAMP - INTERVAL '5 days', 26.5, 42.0, 1016.25, 1.8, 280, 0.0, 22.0, 0, 'Clear'),
(2, CURRENT_TIMESTAMP - INTERVAL '4 days', 23.2, 55.0, 1013.75, 3.2, 250, 0.0, 18.0, 30, 'Partly Cloudy'),
(2, CURRENT_TIMESTAMP - INTERVAL '3 days', 25.8, 48.0, 1014.50, 2.5, 260, 0.0, 20.0, 15, 'Clear'),
(2, CURRENT_TIMESTAMP - INTERVAL '2 days', 27.1, 40.0, 1017.00, 1.5, 290, 0.0, 25.0, 5, 'Clear'),
(2, CURRENT_TIMESTAMP - INTERVAL '1 day', 28.5, 38.0, 1018.25, 1.2, 300, 0.0, 28.0, 0, 'Clear'),
(2, CURRENT_TIMESTAMP, 29.2, 35.0, 1019.50, 1.0, 310, 0.0, 30.0, 0, 'Clear'),

-- Chicago data  
(3, CURRENT_TIMESTAMP - INTERVAL '6 days', 15.2, 78.0, 1009.50, 6.2, 320, 0.5, 12.0, 70, 'Cloudy'),
(3, CURRENT_TIMESTAMP - INTERVAL '5 days', 12.8, 82.0, 1006.25, 8.1, 340, 15.2, 3.0, 100, 'Thunderstorm'),
(3, CURRENT_TIMESTAMP - INTERVAL '4 days', 18.5, 65.0, 1011.75, 4.8, 280, 0.0, 15.0, 45, 'Partly Cloudy'),
(3, CURRENT_TIMESTAMP - INTERVAL '3 days', 21.2, 58.0, 1014.00, 3.5, 250, 0.0, 18.0, 25, 'Clear'),
(3, CURRENT_TIMESTAMP - INTERVAL '2 days', 19.8, 72.0, 1012.50, 4.2, 270, 1.2, 10.0, 60, 'Light Rain'),
(3, CURRENT_TIMESTAMP - INTERVAL '1 day', 22.5, 55.0, 1015.25, 2.8, 230, 0.0, 20.0, 30, 'Partly Cloudy'),
(3, CURRENT_TIMESTAMP, 24.1, 48.0, 1017.00, 2.1, 210, 0.0, 22.0, 15, 'Clear');

-- Insert sample forecast data (next 5 days)
INSERT INTO weather_forecasts (station_id, forecast_date, forecast_hour, temperature_c, humidity_percent, pressure_hpa, wind_speed_ms, wind_direction_deg, precipitation_mm, precipitation_probability, weather_condition, confidence_score, model_version) VALUES
-- New York forecasts
(1, CURRENT_DATE + INTERVAL '1 day', 12, 26.8, 50.0, 1019.25, 2.2, 130, 0.0, 5.0, 'Clear', 0.92, 'v1.2.3'),
(1, CURRENT_DATE + INTERVAL '1 day', 18, 24.5, 58.0, 1018.50, 3.1, 145, 0.0, 10.0, 'Partly Cloudy', 0.88, 'v1.2.3'),
(1, CURRENT_DATE + INTERVAL '2 days', 12, 23.2, 65.0, 1016.75, 4.2, 160, 1.5, 35.0, 'Light Rain', 0.75, 'v1.2.3'),
(1, CURRENT_DATE + INTERVAL '2 days', 18, 21.8, 72.0, 1015.25, 3.8, 170, 3.2, 65.0, 'Light Rain', 0.78, 'v1.2.3'),
(1, CURRENT_DATE + INTERVAL '3 days', 12, 19.5, 85.0, 1011.50, 5.5, 190, 12.8, 85.0, 'Heavy Rain', 0.82, 'v1.2.3'),

-- Los Angeles forecasts
(2, CURRENT_DATE + INTERVAL '1 day', 12, 30.5, 32.0, 1020.00, 0.8, 320, 0.0, 0.0, 'Clear', 0.95, 'v1.2.3'),
(2, CURRENT_DATE + INTERVAL '1 day', 18, 28.8, 38.0, 1019.25, 1.5, 310, 0.0, 0.0, 'Clear', 0.93, 'v1.2.3'),
(2, CURRENT_DATE + INTERVAL '2 days', 12, 31.2, 30.0, 1021.50, 1.2, 330, 0.0, 0.0, 'Clear', 0.96, 'v1.2.3'),
(2, CURRENT_DATE + INTERVAL '2 days', 18, 29.5, 35.0, 1020.75, 1.8, 315, 0.0, 5.0, 'Clear', 0.91, 'v1.2.3'),
(2, CURRENT_DATE + INTERVAL '3 days', 12, 28.2, 42.0, 1018.25, 2.5, 280, 0.0, 10.0, 'Partly Cloudy', 0.85, 'v1.2.3');

-- Insert sample weather alerts
INSERT INTO weather_alerts (station_id, alert_type, severity, title, description, start_time, end_time, is_active) VALUES
(3, 'thunderstorm', 'medium', 'Thunderstorm Watch', 'Severe thunderstorms possible this evening with heavy rain and strong winds.', CURRENT_TIMESTAMP + INTERVAL '2 hours', CURRENT_TIMESTAMP + INTERVAL '8 hours', true),
(1, 'heavy_rain', 'low', 'Light Rain Expected', 'Light to moderate rain expected tomorrow afternoon.', CURRENT_TIMESTAMP + INTERVAL '1 day', CURRENT_TIMESTAMP + INTERVAL '1 day 6 hours', true),
(5, 'extreme_temp', 'high', 'Extreme Cold Warning', 'Temperatures expected to drop below -20°C tonight.', CURRENT_TIMESTAMP + INTERVAL '8 hours', CURRENT_TIMESTAMP + INTERVAL '18 hours', false);

-- Insert sample user preferences
INSERT INTO user_preferences (user_id, preferred_stations, temperature_unit, wind_speed_unit, pressure_unit, timezone, alert_preferences) VALUES
('user_001', ARRAY[1, 3], 'celsius', 'ms', 'hpa', 'America/New_York', '{"thunderstorm": true, "heavy_rain": true, "extreme_temp": true}'),
('user_002', ARRAY[2], 'fahrenheit', 'mph', 'inhg', 'America/Los_Angeles', '{"thunderstorm": false, "heavy_rain": true, "extreme_temp": true}'),
('user_003', ARRAY[1, 2, 3], 'celsius', 'kmh', 'hpa', 'UTC', '{"thunderstorm": true, "heavy_rain": false, "extreme_temp": true}')
ON CONFLICT (user_id) DO NOTHING;