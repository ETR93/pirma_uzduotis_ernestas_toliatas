import time

import pandas as pd
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

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
    df_splited_to_day = ((data['observationTimeUtc'].dt.time >= pd.to_datetime("08:00:00").time()) &
                         (data['observationTimeUtc'].dt.time <= pd.to_datetime("20:00:00").time()))
    data_day = data[df_splited_to_day]
    return {
        'average_day_temperature': round(data_day['airTemperature'].mean().item(), 2),
    }

def calculate_average_temperature_for_night(data):
    df_splited_to_night = ((data['observationTimeUtc'].dt.time >= pd.to_datetime("20:00:00").time()) |
                           (data['observationTimeUtc'].dt.time <= pd.to_datetime("08:00:00").time()))
    data_night = data[df_splited_to_night]
    return {
        'average_night_temperature': round(data_night['airTemperature'].mean().item(), 2),
    }

def check_weekend_for_rain(data):
    weekend_days = []
    start_date = datetime.strptime(data.iloc[0]['date'], "%Y-%m-%d")
    end_date = datetime.strptime(data.iloc[-1]['date'], "%Y-%m-%d")
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() in (5, 6):
            weekend_days.append(current_date.date().isoformat())
        current_date += timedelta(days=1)
    day_weather = data[data['date'].isin(weekend_days)]
    weekend_hours_with_rain = day_weather[day_weather["conditionCode"].str.contains("rain", na=False)]
    week_days_with_rain = weekend_hours_with_rain['date'].drop_duplicates().tolist()

    return {"amount_of_rainy_days": len(week_days_with_rain)}

def concat_last_next_week_data(historical_data, forecast_data):
    last_week_date = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    last_week_data = historical_data[historical_data['date'] >= last_week_date]
    last_week_data = last_week_data.groupby('date', as_index=False)['airTemperature'].mean()
    next_week_data = forecast_data.groupby('date', as_index=False)['airTemperature'].mean()
    return {
        'last_week_temperatures': last_week_data,
        'next_week_temperatures': next_week_data
    }

def interpoliate_data_by_five_minutes(historical_data, forecast_data):
    air_temperatures = historical_data['airTemperature'].tolist()
    first_temperature_date = historical_data.iloc[0]['date']
    first_forecast_temperature_date = forecast_data.iloc[0]['date']
    air_temperatures_forecast = forecast_data['airTemperature'].tolist()
    dates = pd.date_range(first_temperature_date, periods=len(air_temperatures), freq="h")
    dates_forecast = pd.date_range(first_forecast_temperature_date, periods=len(air_temperatures_forecast), freq="h")
    historical_data_air_temperatures_df = pd.DataFrame({'airTemperature': air_temperatures}, index=dates)
    forecast_data_air_temperatures_df = pd.DataFrame({'airTemperature': air_temperatures_forecast},
                                                     index=dates_forecast)
    historical_data_air_temperatures_df_5min = historical_data_air_temperatures_df.resample('5min').asfreq()
    forecast_data_air_temperatures_df_5min = forecast_data_air_temperatures_df.resample('5min').asfreq()
    historical_data_air_temperatures_df_5min['airTemperature'] = historical_data_air_temperatures_df_5min[
        'airTemperature'].interpolate(method='time')
    forecast_data_air_temperatures_df_5min['airTemperature'] = forecast_data_air_temperatures_df_5min[
        'airTemperature'].interpolate(method='time')
    return historical_data_air_temperatures_df_5min, forecast_data_air_temperatures_df_5min

def load_graphs_data(avg_year_temperatute_humidity, avg_temperature_for_a_day, avg_temperature_for_a_night,
                    amount_of_rainy_days):
    x = list(avg_year_temperatute_humidity.keys())
    y = [avg_year_temperatute_humidity[row] for row in avg_year_temperatute_humidity]
    x.append(list(avg_temperature_for_a_day.keys())[0])
    y.append(avg_temperature_for_a_day['average_day_temperature'])
    x.append(list(avg_temperature_for_a_night.keys())[0])
    y.append(avg_temperature_for_a_night['average_night_temperature'])
    x.append(list(amount_of_rainy_days.keys())[0])
    y.append(amount_of_rainy_days['amount_of_rainy_days'])

    return x, y

def draw_weather_analysis_graph(x, y):
    window, graph = plt.subplots(figsize=(16, 8))
    bars = graph.bar(x, y, label="Data results")
    for bar in bars:
        height = bar.get_height()
        graph.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{height}',
            ha='center', va='bottom'
        )
    graph.set_title(label='Weather analysis', fontsize=20)
    graph.set_xlabel('Results', fontsize=20)
    graph.set_ylabel('Amount', fontsize=20)
    plt.show()

def draw_temperature_forecast_graph(x1, x2, y1, y2):
    window, graph = plt.subplots(figsize=(16, 8))
    graph.plot(x1, y1, label='Sensor A', marker='o', color='blue')
    graph.plot(x2, y2, label='Sensor B', marker='s', color='red')
    plt.xticks(rotation=45)
    graph.set_title(label='Weather temperature forecast', fontsize=20)
    graph.set_xlabel('Day', fontsize=20)
    graph.set_ylabel('Temperature', fontsize=20)
    plt.show()
