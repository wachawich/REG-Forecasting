from astral import LocationInfo
import pytz

# Golbal Variables
SERIES_ID = "EBA.CAL-ALL.D.H"  

START_DATE = "2020-01-01"
END_DATE = "2025-11-19"

FORECAST_RANGE_DAYS = 14

RENEWABLE = ["SUN", "WND"]
RESPONDENTS=["CISO"]

LAT = 36.7783
LON = -119.4179
TIME_ZONE_SEASON = 'US/Pacific'
TIME_ZONE_WATHER = "America/Los_Angeles"
CITY = LocationInfo(name="California", region="USA", timezone=TIME_ZONE_SEASON, latitude=LAT, longitude=LON)
TZINFO = pytz.timezone(TIME_ZONE_SEASON)

SOLAR = {
    2020: 34.95,
    2021: 37.75,
    2022: 42.27,
    2023: 50.48,
    2024: 56.27,
    2025: 65.43,
}

WIND = {
    2020: 2400,
    2021: 2491,
    2022: 2465,
    2023: 2514,
    2024: 2544,
    2025: 2593,
}

# Wather
HOURLY_WATHER_VARS = [
    # Solar radiation
    "shortwave_radiation", "direct_radiation", "diffuse_radiation", "direct_normal_irradiance",

    # Cloud details
    "cloudcover", "cloudcover_low", "cloudcover_mid", "cloudcover_high",

    # Atmosphere
    "temperature_2m", "relativehumidity_2m", "dewpoint_2m", "surface_pressure", "vapour_pressure_deficit",

    # Wind (turbine levels + gust)
    "windspeed_10m", "winddirection_10m", "windspeed_100m", "winddirection_100m", "windgusts_10m",

    # Precipitation
    "precipitation", "rain", "snowfall",
]

# Season
SEASON_VARS = [
    'time', 'date', 'day_of_year', 'sin_doy', 
    'cos_doy', 'season', 'solar_zenith_noon_deg', 
    'sunrise_time_h', 'sunrise_time_m', 'sunset_time_h', 'sunset_time_m'
]

# Electricity
ELECTRICITY_VARS = [
    "time", "date", "day", "month", "year", 
    "fueltype", "type-name", "solar_count", 
    "wind_turbine_count", "value"
]


ELECTIC_API_KEY = "pz0pOPI21dJbBbf8RfnUWeTk5RTxNA1FDvip8vmv"
WEATHER_API_URL = "https://archive-api.open-meteo.com/v1/archive"
WEATHER_API_URL_FORECAST = "https://api.open-meteo.com/v1/forecast"
ELECTRICITY_API_URL = "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/"