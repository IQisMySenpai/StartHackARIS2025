import requests
import re

# Define forecast types
forecast_type_dict = {
    "Nowcast" : "Nowcast", 
    "Hourly" : "Hourly",
    "8Hourly" : "8Hourly",
    "Daily" : "Daily"
    }

# Define the dictionary with forecast types as keys and lists of measure labels as values
measureLabel_dict = {
    forecast_type_dict["Nowcast"]: [
        "Temperature_15Min (C)",
        "WindSpeed_15Min (m/s)",
        "WindDirection_15Min",
        "HumidityRel_15Min (pct)"
    ],
    forecast_type_dict["Hourly"]: [
        "Cloudcover_Hourly (pct)",
        "GlobalRadiation_HourlySum (Wh/m2)",
        "HumidityRel_Hourly (pct)",
        "Precip_HourlySum (mm)",
        "PrecipProbability_Hourly (pct)",
        "ShowerProbability_Hourly (pct)",
        "SnowFraction_Hourly",
        "SunshineDuration_Hourly (min)",
        "TempAir_Hourly (C)",
        "Visibility_Hourly (m)",
        "WindDirection_Hourly (Deg)",
        "WindGust_Hourly (m/s)",
        "WindSpeed_Hourly (m/s)",
        "Soilmoisture_0to10cm_Hourly (vol%)",
        "Soiltemperature_0to10cm_Hourly (C)",
        "Referenceevapotranspiration_HourlySum (mm)",
        "LeafWetnessProbability_Hourly (pct)"
    ],
    forecast_type_dict["Daily"]: [
        "Cloudcover_DailyAvg (pct)",
        "Evapotranspiration_DailySum (mm)",
        "GlobalRadiation_DailySum (Wh/m2)",
        "HumidityRel_DailyAvg (pct)",
        "HumidityRel_DailyMax (pct)",
        "HumidityRel_DailyMin (pct)",
        "Precip_DailySum (mm)",
        "PrecipProbability_Daily (pct)",
        "ShowerProbability_DailyMax (pct)",
        "SnowFraction_Daily (pct)",
        "SunshineDuration_DailySum (min)",
        "TempAir_DailyAvg (C)",
        "TempAir_DailyMax (C)",
        "TempAir_DailyMin (C)",
        "ThunderstormProbability_DailyMax (pct)",
        "WindDirection_DailyAvg (Deg)",
        "WindGust_DailyMax (m/s)",
        "WindSpeed_DailyAvg (m/s)",
        "WindSpeed_DailyMax (m/s)",
        "WindSpeed_DailyMin (m/s)",
        "WindDirection_DailyAvg",
        "Soilmoisture_0to10cm_DailyMax (vol%)",
        "Soilmoisture_0to10cm_DailyAvg (vol%)",
        "Soilmoisture_0to10cm_DailyMin (vol%)",
        "Soiltemperature_0to10cm_DailyMax (C)",
        "Soiltemperature_0to10cm_DailyAvg (C)",
        "Soiltemperature_0to10cm_DailyMin (C)",
        "Referenceevapotranspiration_DailySum (mm)"
    ]
}

def get_weather_forecast(
        forecast_type,
        longitude,
        latitude,
        measureLabel, 
        start_date, 
        end_date, 
        api_key="d4f087c7-7efc-41b4-9292-0f22b6199215"
        ):
    # Define the API endpoint
    url = "http://services.cehub.syngenta-ais.com/api/Forecast/ShortRangeForecast"+forecast_type

    # Format the coordinates
    formatted_coordinates = "point(" + str(longitude) + " " + str(latitude) + ")"

    # Define the parameters
    params = {
        "wkt": formatted_coordinates,  # point(lng lat)
        "measureLabel": ";".join(measureLabel), # e.g. "Temperature_15Min (C);WindSpeed_15Min (m/s)"
        "startDate": start_date,  # YYYY-MM-DD
        "endDate": end_date,  # YYYY-MM-DD
        "supplier": "Meteoblue",
        "top": 500,
        "format": "json",
        "ApiKey": api_key
    }

    # Make the request
    response = requests.get(url, params=params)

    # Check the response status
    if response.status_code == 200:
        data = response.json()
        data = {item['measureLabel']: float(item['dailyValue']) for item in data}
        return data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Class to calculate crop stress

class CropRisksCalculator:
    def __init__(self, crop_name, TMAX, TMIN, TAVG, P, SM, E, pH, N):
        # Crop parameters
        self.crop_name = crop_name
        self.TMAX = TMAX
        self.TMIN = TMIN
        self.TAVG = TAVG
        self.P = P
        self.SM = SM
        self.E = E
        self.pH = pH
        self.N = N

        self.crop_params = {
            'Soybean': {
                'TMaxOptimum': 32,
                'TMaxLimit': 45,
                'TMinOptimum': 22,
                'TMinLimit': 28,
                'TMinNoFrost': 4,
                'TminFrost': -3,
                'TBase': 10,
                'GDD_opt': (2400, 3000),
                'P_opt': (450, 700),
                'pH_opt': (6.0, 6.8),
                'N_opt': (0, 0.026)
            },
            'Corn': {
                'TMaxOptimum': 33,
                'TMaxLimit': 44,
                'TMinOptimum': 22,
                'TMinLimit': 28,
                'TMinNoFrost': 4,
                'TminFrost': -3,
                'TBase': 10,
                'GDD_opt': (2700, 3100),
                'P_opt': (500, 800),
                'pH_opt': (6.0, 6.8),
                'N_opt': (0.077, 0.154)
            },
            'Cotton': {
                'TMaxOptimum': 32,
                'TMaxLimit': 38,
                'TMinOptimum': 20,
                'TMinLimit': 25,
                'TMinNoFrost': 4,
                'TminFrost': -3,
                'TBase': 10,
                'GDD_opt': (2200, 2600),
                'P_opt': (700, 1300),
                'pH_opt': (6.0, 6.5),
                'N_opt': (0.051, 0.092)
            },
            'Rice': {
                'TMaxOptimum': 32,
                'TMaxLimit': 38,
                'TMinOptimum': 22,
                'TMinLimit': 28,
                'TMinNoFrost': None,
                'TminFrost': None,
                'TBase': 10,
                'GDD_opt': (2000, 2500),
                'P_opt': (1000, 1500),
                'pH_opt': (5.5, 6.5),
                'N_opt': (0.051, 0.103)
            },
            'Wheat': {
                'TMaxOptimum': 25,
                'TMaxLimit': 32,
                'TMinOptimum': 15,
                'TMinLimit': 20,
                'TMinNoFrost': None,
                'TminFrost': None,
                'TBase': 10,
                'GDD_opt': (2000, 2500),
                'P_opt': (1000, 1500),
                'pH_opt': (5.5, 6.5),
                'N_opt': (0.051, 0.103)
            }
        }

        self.GDD = self.growing_degree_days()

    def growing_degree_days(self):
        return ((self.TMAX + self.TMIN) / 2) - self.crop_params[self.crop_name]['TBase']
    
    def diurnal_heat_stress(self):
        params = self.crop_params[self.crop_name]
        TMaxOptimum = params['TMaxOptimum']
        TMaxLimit = params['TMaxLimit']

        if self.TMAX <= TMaxOptimum:
            return 0
        elif TMaxOptimum < self.TMAX < TMaxLimit:
            return 9 * ((self.TMAX - TMaxOptimum) / (TMaxLimit - TMaxOptimum))
        else:
            return 9

    def nighttime_heat_stress(self):
        params = self.crop_params[self.crop_name]
        TMinOptimum = params['TMinOptimum']
        TMinLimit = params['TMinLimit']

        if self.TMIN < TMinOptimum:
            return 0
        elif TMinOptimum <= self.TMIN < TMinLimit:
            return 9 * ((self.TMIN - TMinOptimum) / (TMinLimit - TMinOptimum))
        else:
            return 9

    def frost_stress(self):
        params = self.crop_params[self.crop_name]
        TMinNoFrost = params['TMinNoFrost']
        TminFrost = params['TminFrost']

        if TMinNoFrost is None or TminFrost is None:
            return 0  # No frost stress for crops that don't have frost limits

        if self.TMIN >= TMinNoFrost:
            return 0
        elif self.TMIN < TminFrost:
            return 9
        else:
            return 9 * (abs(self.TMIN - TMinNoFrost) / abs(TminFrost - TMinNoFrost))

    def drought_risk(self):
        DI = (self.P - self.E) + (self.SM / self.TAVG)
        DIsigma = 0.1
        if DI > 1 + DIsigma:
            return 0
        elif abs(DI - 1) <= DIsigma:
            return "Medium risk"
        else:
            return "High risk"

    def yield_risk(self):
        params = self.crop_params[self.crop_name]
        GDD_opt = params['GDD_opt']
        P_opt = params['P_opt']
        pH_opt = params['pH_opt']
        N_opt = params['N_opt']

        # Weighting factors
        w1, w2, w3, w4 = 0.3, 0.3, 0.2, 0.2

        # Calculate yield risk
        yield_risk_value = (
            w1 * (self.GDD - GDD_opt[1]) ** 2 +
            w2 * (self.P - P_opt[1]) ** 2 +
            w3 * (self.pH - pH_opt[1]) ** 2 +
            w4 * (self.N - N_opt[1]) ** 2
        )
        return yield_risk_value
    
    # Function to binarize the result

    def binarize_result(self, dictionary):
        result = {}
        for key in dictionary:
            if dictionary[key] == 0:
                result[key] = 0
            else:
                result[key] = 1
        return result

    def calculate(self, binarize=False):
        result = {"diurnal_stress" : self.diurnal_heat_stress(),
                  "nighttime_stress" : self.nighttime_heat_stress(),
                  "frost_stress" : self.frost_stress(),
                  "drought_risk" : self.drought_risk(),
                  "yield_risk" : self.yield_risk()
                  }
        if binarize:
            return (self.binarize_result(result), result)
        else:
            return result

def extract_european_letters(text):
    # Define a regex pattern for standard European letters and common accents
    pattern = r"[A-Za-zÀ-ÿ]"  # This includes accented characters in the Latin-1 Supplement range

    # Use re.findall to extract all matching characters
    extracted_letters = re.findall(pattern, text)

    # Join the list into a string
    return ''.join(extracted_letters)

def get_city_name(
        longitude,
        latitude,
        api_key="d4f087c7-7efc-41b4-9292-0f22b6199215"
        ):
    # Define the API endpoint
    url = "http://services.cehub.syngenta-ais.com/api/LocationSearch/GenerateLocationByCoordinate"

    # Define the parameters
    params = {
        "longitude": longitude, 
        "latitude": latitude,
        "ApiKey": api_key
    }

    # Make the request
    response = requests.get(url, params=params)

    # Check the response status
    if response.status_code == 200:
        data = response.json()
        return data["name"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None