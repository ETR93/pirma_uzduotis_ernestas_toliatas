from GetData import GetData
from helpers import (calculate_average_year_temperature_and_humidity, calculate_average_temperature_for_day,
                     calculate_average_temperature_for_night, check_weekend_for_rain, concat_last_next_week_data,
                     interpoliate_data_by_five_minutes, load_graphs_data, draw_weather_analysis_graph,
                     draw_temperature_forecast_graph)

if __name__ == '__main__':
    while True:
        print("--------------------------------------")
        print("To select historical data - 1")
        print("To select forecast data - 2")
        print("Exit program - 3")
        print("Interpolate values by 5 minutes - 4")
        choice = input("Enter choice: ")
        match choice:
            case "1":
                place_code = input("Enter place code in genetive case for example (raseiniu): ")
                data = GetData(place_code).historical_data()
                avg_year_temperatute_humidity = calculate_average_year_temperature_and_humidity(data)
                avg_temperature_for_a_day = calculate_average_temperature_for_day(data)
                avg_temperature_for_a_night = calculate_average_temperature_for_night(data)
                amount_of_rainy_days = check_weekend_for_rain(data)
                graphs_data = load_graphs_data(avg_year_temperatute_humidity, avg_temperature_for_a_day,
                                              avg_temperature_for_a_night, amount_of_rainy_days)
                x = graphs_data[0]
                y = graphs_data[1]
                draw_weather_analysis_graph(x, y)
            case "2":
                place_code_historical = input(
                    "Enter place code for historical data in genetive case for example (raseiniu): "
                )
                place_code_forecast = input(
                    "Enter place code for forecast in nominative case for example (raseiniai): "
                )
                historical_data = GetData(place_code_historical).historical_data()
                forecast_data = GetData(place_code_forecast).get_forecast_date()
                compared_temperatures = concat_last_next_week_data(historical_data, forecast_data)
                x1 = compared_temperatures['last_week_temperatures']['date']
                x2 = compared_temperatures['next_week_temperatures']['date']
                y1 = compared_temperatures['last_week_temperatures']['airTemperature']
                y2 = compared_temperatures['next_week_temperatures']['airTemperature']
                draw_temperature_forecast_graph(x1=x1, x2=x2, y1=y1, y2=y2)
            case "3":
                break
            case "4":
                place_code_historical = input(
                    "Enter place code for historical data in genetive case for example (raseiniu): "
                )
                place_code_forecast = input(
                    "Enter place code for forecast in nominative case for example (raseiniai): "
                )
                historical_data = GetData(place_code_historical).historical_data()
                forecast_data = GetData(place_code_forecast).get_forecast_date()
                print(interpoliate_data_by_five_minutes(historical_data, forecast_data)[0])
                print(interpoliate_data_by_five_minutes(historical_data, forecast_data)[1])
