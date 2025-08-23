from matplotlib import pyplot as plt
from GetData import GetData
from helpers import (calculate_average_year_temperature_and_humidity, calculate_average_temperature_for_day,
                     calculate_average_temperature_for_night, check_weekend_for_rain, concat_last_next_week_data,
                     interpoliate_data_by_five_minutes)

if __name__ == '__main__':
    while True:
        print("--------------------------------------")
        print("To select historical data - 1")
        print("To select forecast data - 2")
        print("Exit program - 3")
        print("Interpolate values by 5 minutes - 4")
        choice = input("Enter choice: ")
        window, graph = plt.subplots(figsize=(16, 6))
        match choice:
            case "1":
                place_code = input("Enter place code: ")
                data = GetData(place_code).historical_data()
                avg_year_temperatute_humidity = calculate_average_year_temperature_and_humidity(data)
                avg_temperature_for_a_day = calculate_average_temperature_for_day(data)
                avg_temperature_for_a_night = calculate_average_temperature_for_night(data)
                amount_of_rainy_days = check_weekend_for_rain(data)
                x = list(avg_year_temperatute_humidity.keys())
                y = [avg_year_temperatute_humidity[row] for row in avg_year_temperatute_humidity]
                x.append(list(avg_temperature_for_a_day.keys())[0])
                y.append(avg_temperature_for_a_day['average_day_temperature'])
                x.append(list(avg_temperature_for_a_night.keys())[0])
                y.append(avg_temperature_for_a_night['average_night_temperature'])
                x.append(list(amount_of_rainy_days.keys())[0])
                y.append(amount_of_rainy_days['amount_of_rainy_days'])
                graph.bar(x, y, label="Data results")
                plt.show()
            case "2":
                place_code_historical = input("Enter place code for historical data: ")
                place_code_forecast = input("Enter place code for forecast: ")
                historical_data = GetData(place_code_historical).historical_data()
                forecast_data = GetData(place_code_forecast).get_forecast_date()
                compared_temperatures = concat_last_next_week_data(historical_data, forecast_data)
                x1 = compared_temperatures['last_week_temperatures']['date']
                x2 = compared_temperatures['next_week_temperatures']['date']
                y1 = compared_temperatures['last_week_temperatures']['airTemperature']
                y2 = compared_temperatures['next_week_temperatures']['airTemperature']
                graph.plot(x1, y1, label='Sensor A', marker='o', color='blue')
                graph.plot(x2, y2, label='Sensor B', marker='s', color='red')
                plt.show()
            case "3":
                break
            case "4":
                place_code_historical = input("Enter place code for historical data: ")
                place_code_forecast = input("Enter place code for forecast: ")
                historical_data = GetData(place_code_historical).historical_data()
                forecast_data = GetData(place_code_forecast).get_forecast_date()
                print(interpoliate_data_by_five_minutes(historical_data, forecast_data)[0])
                print(interpoliate_data_by_five_minutes(historical_data, forecast_data)[1])
