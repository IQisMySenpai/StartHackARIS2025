import datetime
from risks import get_weather_forecast, forecast_type_dict, CropRisksCalculator, get_city_name

def create_risk_report(user, target_time=None):
    forecast_type = forecast_type_dict["Daily"]
    longitude = user['longitude']
    latitude = user['latitude']
    measureLabel = [
        "TempAir_DailyMax (C)",
        "TempAir_DailyMin (C)",
        "TempAir_DailyAvg (C)",
        "Precip_DailySum (mm)",
        "Referenceevapotranspiration_DailySum (mm)",
        "Soilmoisture_0to10cm_DailyAvg (vol%)",
    ]

    if target_time is not None:  # Load from ISO 8601 format and convert to ISO 8601 date format
        start_date = target_time.split("T")[0]
        end_date = start_date
    else:
        start_date = datetime.datetime.now().strftime("%Y-%m-%d")
        end_date = start_date

    weather_forecast = get_weather_forecast(
        forecast_type=forecast_type,
        longitude=longitude,
        latitude=latitude,
        measureLabel=measureLabel,
        start_date=start_date,
        end_date=end_date
    )

    crop_name = user['plant']

    TMAX = weather_forecast["TempAir_DailyMax (C)"]  # Maximum temperature
    TMIN = weather_forecast["TempAir_DailyMin (C)"]  # Minimum temperature
    TAVG = weather_forecast["TempAir_DailyAvg (C)"]  # Average temperature
    P = weather_forecast["Precip_DailySum (mm)"]  # Cumulative rainfall
    SM = weather_forecast["Soilmoisture_0to10cm_DailyAvg (vol%)"]  # Soil moisture
    # GDD calculation is internal to the calculator
    E = weather_forecast["Referenceevapotranspiration_DailySum (mm)"] # Cumulative evaporation
    pH = 6.5  # Soil pH
    N = 0.02  # Available nitrogen

    calculator = CropRisksCalculator(crop_name, TMAX, TMIN, TAVG, P, E, SM, pH, N)

    return calculator.calculate(binarize=True)