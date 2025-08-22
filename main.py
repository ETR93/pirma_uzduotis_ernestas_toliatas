from GetData import GetData
from helpers import (calculate_average_year_temperature_and_humidity, calculate_average_temperature_for_day,
                     calculate_average_temperature_for_night)

if __name__ == '__main__':
    while True:
        print("--------------------------------------")
        print("To select historical data - 1")
        print("To select forecast data - 2")
        print("Exit program - 3")
        choice = input("Enter choice: ")
        match choice:
            case "1":
                place_code = input("Enter place code: ")
                data = GetData(place_code).historical_data()
                print(calculate_average_year_temperature_and_humidity(data))
                print(calculate_average_temperature_for_day(data))
                print(calculate_average_temperature_for_night(data))
            case "2":
                place_code = input("Enter place code: ")
                print(GetData(place_code).get_forecast_date())
            case "3":
                break