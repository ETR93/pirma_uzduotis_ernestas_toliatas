import time
import pandas as pd

def check_amount_of_requests(amount_of_requests):
    amount_of_requests += 1
    if amount_of_requests == 179:
        print("Maximum amount of requests per minute has been reached. Wait for 70 seconds.")
        time.sleep(70)
        amount_of_requests = 0
    return amount_of_requests

def calculate_average_year_temperature_and_humidity(data_frame):
    return {
        'average_temperature': round(data_frame['airTemperature'].mean().item(), 2),
        'average_humidity': round(data_frame['relativeHumidity'].mean().item(), 2),
    }

def calculate_average_temperature_for_day(data):
    df_splited_to_day = (data['observationTimeUtc'].dt.time >= pd.to_datetime("08:00:00").time()) & (data['observationTimeUtc'].dt.time <= pd.to_datetime("20:00:00").time())
    data_day = data[df_splited_to_day]
    return {
        'average_day_temperature': round(data_day['airTemperature'].mean().item(), 2),
    }

def calculate_average_temperature_for_night(data):
    df_splited_to_night = (data['observationTimeUtc'].dt.time >= pd.to_datetime("20:00:00").time()) | (data['observationTimeUtc'].dt.time <= pd.to_datetime("08:00:00").time())
    data_night = data[df_splited_to_night]
    return {
        'average_night_temperature': data_night['airTemperature'].mean().item(),
    }